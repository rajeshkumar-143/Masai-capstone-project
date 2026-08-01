# Data Engineering Pipeline

This project implements a data engineering pipeline to scrape book catalog data, clean and enrich it, load it into a normalized SQLite database, and then query it using both SQL and pandas.

## Project Overview

Zepto's analysts require a robust pipeline to benchmark catalog-style pricing and availability data. This module focuses on creating a raw-to-relational workflow: scrape live product data, clean it, enrich it with a fixed-rate currency conversion, and store it in a normalized relational database for querying.


### Step 1. Data Scraping

*   **Scraping Target**: `books.toscrape.com` (a public scraping-practice site).
*   **Data Volume**: Scrape all books listed across at least 3 different book categories, resulting in a dataset of **≥ 60 book rows**.
*   **Captured Fields Per Book**: `title`, `price` (as listed, in GBP), `star_rating` (as text, e.g., 'Three'), `availability` (as listed text), and `category`.
*   **Libraries Used**: `requests` and `BeautifulSoup`.

### Step 2. Data Cleaning and Enrichment

*   **`price_gbp`**: Strip currency symbol from `price` and convert to a `float`.
*   **`rating`**: Convert text `star_rating` (e.g., 'One'...'Five') into an `integer` (1-5).
*   **`in_stock`**: Parse `availability` text into a `boolean` column.
*   **Error Handling**: If any field fails to parse, median-imputation will be used for numeric fields, and rows will be dropped for critical parsing failures, ensuring the pipeline's robustness.
*   **`price_inr`**: Convert `price_gbp` to `price_inr` using a **fixed baseline conversion rate: 1 GBP = 105.50 INR**. This is a project-defined constant.

### Step 3. Database Design and Loading

*   **Database**: SQLite (`sqlite3` module or `pandas.DataFrame.to_sql`).
*   **Schema Design**: Normalized schema with at least two tables sharing a primary/foreign key relationship. Example:
    *   `categories(category_id INTEGER PRIMARY KEY, category_name TEXT UNIQUE)`
    *   `books(book_id INTEGER PRIMARY KEY, title TEXT, price_gbp REAL, price_inr REAL, rating INTEGER, in_stock INTEGER, category_id INTEGER REFERENCES categories(category_id))`
*   **Data Insertion**: Insert cleaned, converted data into this schema.

### Step 4. SQL Queries

*   **Number of Queries**: At least 5 SQL queries will be executed.
*   **Demonstrated Clauses**: Collectively demonstrate `SELECT/WHERE`, `ORDER BY`, `LIMIT`, `DISTINCT`, and (`IN` or `BETWEEN`).
*   **JOIN**: At least one `JOIN` between the two tables (e.g., "list the 10 highest-rated books per category").
*   **Output**: Each query string and its output will be saved.

### Step 5. Pandas DataFrames for Query Results

*   **`pd.read_sql`**: Read back at least two query results into pandas DataFrames.
*   **`pd.merge`**: Reproduce the join-query's result using `pd.merge()` directly on in-memory DataFrames (without SQL).
*   **Verification**: Show that both `pd.read_sql` and `pd.merge` approaches produce equivalent output for the join query.

### Step 6. Documentation and Reproducibility

*   **`README.md`**: This document outlines the install/run steps and design decisions.
*   **`requirements.txt`**: Lists all Python dependencies.
*   **SQLite Database**: The project includes the SQLite database file or the exact script to regenerate it from scratch.
*   **Fixed Rate Statement**: The exact rate `1 GBP = 105.50 INR` is explicitly stated in this README.

## Installation and Setup

To run this project, follow these steps:

1.  **Clone the Repository**:

    ```bash
    git clone <repository_url>
    cd data_pipeline
    ```

2.  **Create a Virtual Environment (Recommended)**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

## Running the Pipeline

1.  **Execute the Jupyter Notebook/Script**:

    Open and run the main notebook (e.g., `data_pipeline.ipynb`) or execute the Python script containing the scraping, cleaning, and database loading logic.

    ```bash
    jupyter notebook data_pipeline.ipynb
    ```
    or
    ```bash
    python main_script.py
    ```

    The notebook/script will perform the following:
    *   Scrape data from `books.toscrape.com`.
    *   Clean and enrich the data.
    *   Create and populate the SQLite database (`books.db`).
    *   Execute SQL queries and display their outputs.
    *   Demonstrate `pd.read_sql` and `pd.merge` comparisons.

## Design Decisions

*   **Currency Conversion Rate**: The fixed conversion rate of `1 GBP = 105.50 INR` is hardcoded as per the requirements. No external API calls are made for currency conversion.
*   **Error Handling (Cleaning)**:
    *   For `price_gbp` and `rating`, if parsing fails, median imputation will be applied. This prevents data loss for potentially recoverable issues while maintaining the dataset size.
    *   For `in_stock`, if the availability text is unexpected and cannot be mapped to a boolean, the row will be dropped. This is because `in_stock` is a critical categorical feature, and ambiguous values would lead to incorrect analysis.
*   **SQLite Schema**: The chosen schema `categories` and `books` with a `category_id` foreign key ensures normalization, avoids data redundancy for categories, and allows for efficient querying of books by category.

This `README.md` will be updated with more specific details as the implementation progresses.
