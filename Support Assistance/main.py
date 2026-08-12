
import os
from typing import List, Literal, TypedDict
from pydantic import BaseModel
from langgraph.graph import StateGraph, END
import chromadb
from sentence_transformers import SentenceTransformer
from fastapi import FastAPI
import uvicorn
import nest_asyncio

# --- Environment Configuration ---
MOCK_LLM = os.getenv("MOCK_LLM", "1") == "1"

# --- Pydantic Models ---
class Answer(BaseModel):
    answer: str
    sources: List[str]
    confidence: float

class QueryRequest(BaseModel):
    query: str

# --- LangGraph State Definition ---
class GraphState(TypedDict):
    query: str
    classification: Literal["policy_question", "general_question"]
    context: str # Retrieved context from ChromaDB
    answer: Answer # Structured answer including sources and confidence

# --- ChromaDB and Embedding Model Initialization ---
# These should ideally be initialized once globally or passed as dependencies
# For a simple app, we initialize them here.
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="zepto_policies")

# --- Prompt Template (if needed for real LLM) ---
PROMPT_TEMPLATE = """You are an AI assistant for Zepto's customer support. Your role is to provide accurate and concise answers to customer queries based *only* on the provided context. If the answer is not explicitly available in the context, state that you cannot answer the question. Do not make up information. Do not use outside knowledge.\n\nContext:\n{context}\n\nTask: Answer the user's question based *only* on the provided context. Ensure your answer is factual, concise, and directly addresses the query. If the context does not contain the answer, respond with 'I cannot answer this question based on the provided Zepto policies.'.\n\nFormat: Provide a clear and direct answer.\n\nLength: Keep the answer as short as possible while being comprehensive.\n\nExamples:\nUser: How much does Zepto Pass+ cost and what benefits does it offer?\nAssistant: Zepto Pass+ costs INR 99 per month. It offers free priority delivery, 10% off select categories, and early access to limited-time deals 24 hours before they go live to Basic and Pass members.\n\nUser: Can I return a damaged perishable item?\nAssistant: Yes, grocery and perishable items may be reported for a return within 24 hours of delivery if damaged, spoiled, or incorrect.\n\nUser: {query}\nAssistant:"""

# --- LangGraph Nodes ---
def classify_intent(state: GraphState) -> GraphState:
    query = state["query"].lower()
    policy_keywords = [
        "delivery", "return", "refund", "membership",
        "tracking", "cancel", "gift card", "support hours"
    ]

    if MOCK_LLM:
        if any(keyword in query for keyword in policy_keywords):
            classification = "policy_question"
        else:
            classification = "general_question"
    else:
        classification = "general_question" # Placeholder for real LLM

    print(f"[classify_intent] Classified: {classification} for '{state['query']}'")
    return {"classification": classification}

def retrieve_and_answer(state: GraphState) -> GraphState:
    query = state["query"]
    query_embedding = embedding_model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3,
        include=['documents', 'metadatas', 'distances']
    )

    retrieved_documents = results['documents'][0]
    retrieved_metadatas = results['metadatas'][0]

    context_snippets = []
    source_ids = []

    for i, doc in enumerate(retrieved_documents):
        context_snippets.append(doc)
        source_ids.append(retrieved_metadatas[i]['source'].split('/')[-1].replace('.txt', ''))

    context = "\n\n".join(context_snippets)
    top_chunk_snippet = retrieved_documents[0][:200] + "..." if retrieved_documents else "No context found."

    final_answer: Answer
    if MOCK_LLM:
        answer_text = f"Based on the retrieved context: {top_chunk_snippet}"
        final_answer = Answer(
            answer=answer_text,
            sources=source_ids,
            confidence=1.0
        )
    else:
        # Placeholder for real LLM integration with PROMPT_TEMPLATE and Pydantic retry
        answer_text = "I cannot provide a real-LLM answer in this mock setup."
        final_answer = Answer(
            answer=answer_text,
            sources=[],
            confidence=0.0
        )
    print(f"[retrieve_and_answer] Answer: {final_answer.answer[:50]}...")
    return {"context": context, "answer": final_answer}

def direct_answer(state: GraphState) -> GraphState:
    final_answer: Answer
    if MOCK_LLM:
        answer_text = "I can only answer questions about Zepto policies right now."
        final_answer = Answer(
            answer=answer_text,
            sources=[],
            confidence=1.0
        )
    else:
        # Placeholder for real LLM direct answer
        answer_text = "I cannot provide a real-LLM answer in this mock setup."
        final_answer = Answer(
            answer=answer_text,
            sources=[],
            confidence=0.0
        )
    print(f"[direct_answer] Answer: {final_answer.answer[:50]}...")
    return {"answer": final_answer}

# --- Build the LangGraph Workflow ---
workflow = StateGraph(GraphState)
workflow.add_node("classify_intent", classify_intent)
workflow.add_node("retrieve_and_answer", retrieve_and_answer)
workflow.add_node("direct_answer", direct_answer)
workflow.set_entry_point("classify_intent")
workflow.add_conditional_edges(
    "classify_intent",
    lambda state: state["classification"],
    {
        "policy_question": "retrieve_and_answer",
        "general_question": "direct_answer",
    },
)
workflow.add_edge("retrieve_and_answer", END)
workflow.add_edge("direct_answer", END)
app = workflow.compile()

# --- FastAPI Application ---
app_fastapi = FastAPI(
    title="Zepto GenAI Service",
    description="A RAG-based GenAI service for Zepto's policy inquiries."
)

@app_fastapi.post("/ask", response_model=Answer)
async def ask_zepto_policy(request: QueryRequest):
    initial_state = {"query": request.query}
    final_state = app.invoke(initial_state)
    return final_state["answer"]

# For local development within Colab (not strictly needed for Docker)
nest_asyncio.apply()

# To run this file directly with uvicorn:
# if __name__ == "__main__":
#     uvicorn.run(app_fastapi, host="0.0.0.0", port=8000)
