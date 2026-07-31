# Zepto GenAI Service

This project implements a small but complete Generative AI (GenAI) service for Zepto, designed to answer policy-related customer inquiries. It leverages a RAG (Retrieval Augmented Generation) pipeline orchestrated by LangGraph, with a FastAPI application serving the API. The service is runnable locally and includes a Dockerfile for containerization.

## Architecture Description

The Zepto GenAI service follows a RAG architecture, divided into several key stages:

1.  **Ingestion & Embedding**: This stage involves processing the raw policy documents and converting them into numerical vector representations (embeddings). The `all-MiniLM-L6-v2` sentence transformer model is used for embedding, and these embeddings, along with the original document text, are stored in `ChromaDB` for efficient retrieval. Each policy document is treated as a single chunk.

2.  **FastAPI Application**: A `FastAPI` application exposes a `POST /ask` endpoint. This endpoint receives user queries, passes them to the LangGraph workflow, and returns a structured JSON response (`Answer` Pydantic model) containing the generated answer, source documents, and a confidence score.

3.  **LangGraph Orchestration**: The core logic of the RAG pipeline is orchestrated using `LangGraph`. It defines a `StateGraph` with a `TypedDict` (`GraphState`) to manage the conversational flow. The workflow consists of three main nodes and conditional edges:
    *   **`classify_intent`**: This node analyzes the incoming user query to determine its intent. It classifies queries as either `policy_question` or `general_question`. This node's behavior is gated by the `MOCK_LLM` environment variable.
    *   **`retrieve_and_answer`**: If the intent is `policy_question`, this node is activated. It takes the user's query, embeds it, and retrieves the top-k most relevant policy documents from `ChromaDB`. It then constructs an answer based on the retrieved context. This node's answer generation is also gated by `MOCK_LLM`.
    *   **`direct_answer`**: If the intent is `general_question`, this node is activated. It provides a canned, generic response, indicating that it can only answer policy-related questions. This node's behavior is also gated by `MOCK_LLM`.

    The `LangGraph` dynamically routes queries from `classify_intent` to either `retrieve_and_answer` or `direct_answer` based on the classification. Finally, both `retrieve_and_answer` and `direct_answer` nodes lead to the `END` state, returning the structured `Answer`.

4.  **MOCK_LLM Gating**: A critical aspect of this service is its support for a fully deterministic, rule-based mock mode. This is controlled by the `MOCK_LLM` environment variable:
    *   When `MOCK_LLM` is unset or `1` (default), the service operates in **mock mode**. `classify_intent` uses keyword heuristics, `retrieve_and_answer` returns a templated response based on retrieved snippets, and `direct_answer` returns a fixed string. No actual LLM calls are made, and no API keys are required.
    *   When `MOCK_LLM` is `0` (optional extension), the service is configured for **real LLM integration**. In this mode, `classify_intent` and `retrieve_and_answer` would ideally integrate with an external LLM (e.g., Groq) using the `PROMPT_TEMPLATE` for generation and Pydantic for structured output validation with retry logic. (Note: The real LLM paths are currently placeholders in the provided code).

### Data Flow

User Query --> FastAPI (`/ask` endpoint) --> LangGraph (`classify_intent`) --("policy_question")--> LangGraph (`retrieve_and_answer`) --> ChromaDB (retrieval) --> LangGraph (`retrieve_and_answer` generates answer) --> FastAPI (returns structured JSON) 

User Query --> FastAPI (`/ask` endpoint) --> LangGraph (`classify_intent`) --("general_question")--> LangGraph (`direct_answer` generates answer) --> FastAPI (returns structured JSON)

## Local Development Setup

### Prerequisites

*   Python 3.9+
*   Docker (for containerized deployment)
*   `pip` for package installation

### Steps to Run

1.  **Clone the repository (or set up the files from the notebook):** Ensure you have `main.py`, `Dockerfile`, and the `docs` directory (containing `doc_01.txt` to `doc_08.txt`) in your working directory.

2.  **Build the Docker image:**

    ```bash
    docker build -t zepto-genai-service .
    ```

3.  **Run the Docker container:**

    The service will be accessible on `http://localhost:8000`. By default, it runs in `MOCK_LLM=1` mode.

    ```bash
    docker run -p 8000:8000 -e MOCK_LLM=1 zepto-genai-service
    ```

    *(Optional: To simulate the real LLM path (which is a placeholder), you could run with `-e MOCK_LLM=0`, but no actual LLM integration is active in the provided code.)*

4.  **Make API requests:**

    You can use `curl` or any HTTP client to interact with the service.

### Example API Calls (Mock Mode `MOCK_LLM=1`)

#### Example 1: Policy Question

**Query:** `What are the delivery charges for Zepto?`

**Request:**

```bash
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"query": "What are the delivery charges for Zepto?"}'
```

**Response:**

```json
{
  "answer": "Based on the retrieved context: Zepto delivers grocery and household essentials to serviceable pin codes within 10 to 30 minutes of order confirmation, depending on the customer's delivery zone and current order volume. Standard del...",
  "sources": [
    "doc_01",
    "doc_03",
    "doc_05"
  ],
  "confidence": 1.0
}
```

#### Example 2: General Question

**Query:** `What is the weather like in Mumbai today?`

**Request:**

```bash
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"query": "What is the weather like in Mumbai today?"}'
```

**Response:**

```json
{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 1.0
}
```

## Further Extensions (Ungraded)

*   **Real LLM Integration**: Implement actual LLM calls (e.g., using Groq, OpenAI, or other providers) in `classify_intent` and `retrieve_and_answer` when `MOCK_LLM=0`.
*   **Live Cloud Deployment**: Deploy the FastAPI application to a cloud platform (e.g., Hugging Face Spaces, Google Cloud Run, AWS Fargate).
*   **Advanced RAG**: Implement chunking strategies, more sophisticated retrieval, or re-ranking for better context quality.
*   **Error Handling**: Add more robust error handling and logging.

