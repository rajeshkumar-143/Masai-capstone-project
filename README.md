# Python Projects Portfolio

Welcome to my Python project portfolio! This repository contains three distinct projects showcasing my skills in Exploratory Data Analysis (EDA), Data Engineering (Web Scraping & SQL), and Generative AI (RAG & APIs).

---

## 📊 Project 1: Titanic Data Analysis & Profiling

A comprehensive exploratory data analysis and cleaning pipeline focused on the classic Titanic dataset. 

### Key Features:
* **Data Profiling & Cleaning:** Automatically calculates missing value percentages and applies targeted handling strategies (e.g., dropping the heavily missing `deck` column, imputing `age` with median values, and dropping rows with missing embarkation data).
* **Univariate Analysis:** Generates histograms and box plots to visualize distributions for features like `age` and `fare`, while calculating Interquartile Ranges (IQR) to identify outliers.
* **Bivariate Analysis:** Compares survival rates across different demographics (sex and passenger class) using Seaborn bar plots, and generates a correlation matrix heatmap to uncover relationships between numerical features.

**Technologies Used:** `pandas`, `seaborn`, `matplotlib`, `numpy`

---

## 🕸️ Project 2: Book Web Scraper & SQLite Database

An automated web scraping script that extracts product data from [Books to Scrape](http://books.toscrape.com/) and stores it in a relational database.

### Key Features:
* **Automated Scraping:** Navigates through multiple categories and paginated results using `requests` and `BeautifulSoup`.
* **Data Cleaning & Enrichment:** Converts string prices to floats, translates GBP to INR, maps text-based star ratings to integers, and parses availability status into booleans. 
* **Database Management:** Dynamically creates an SQLite database (`books.db`) with normalized `categories` and `books` tables, utilizing Foreign Keys for data integrity.
* **SQL Queries:** Executes complex SQL queries via Pandas (e.g., `JOIN` operations, sorting, and filtering by price and rating) to verify and analyze the scraped data.

**Technologies Used:** `requests`, `BeautifulSoup`, `pandas`, `sqlite3`, `re`

---

## 🤖 Project 3: Zepto RAG GenAI Service 

A Retrieval-Augmented Generation (RAG) backend service designed to answer customer support queries about Zepto's delivery, return, and account policies.

### Key Features:
* **Vector Database Integration:** Embeds Zepto policy documents using `SentenceTransformers` (`all-MiniLM-L6-v2`) and stores them in `ChromaDB` for rapid semantic search.
* **LangGraph Orchestration:** Uses a state graph to classify user intent. Policy-related queries trigger a vector retrieval sequence, while general queries are routed to a direct fallback answer.
* **FastAPI Backend:** Wraps the LangGraph workflow in a modern, fast web API with a `POST /ask` endpoint.
* **Structured Responses:** Returns rigorously typed JSON responses using `Pydantic` models, including the generated answer, source document references, and confidence scores.

**Technologies Used:** `langgraph`, `FastAPI`, `chromadb`, `sentence-transformers`, `pydantic`, `uvicorn`

---

## 🚀 How to Run

### Prerequisites
Make sure you have Python 3.9+ installed. Install the required dependencies for all projects by running:

```bash
pip install pandas seaborn matplotlib requests beautifulsoup4 chromadb sentence-transformers langgraph fastapi uvicorn pydantic nest-asyncio
