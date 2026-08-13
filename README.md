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

# Data Pipeline

**Data Scraping and Cleaning**

* The data pipeline uses `requests` and `BeautifulSoup` to scrape book data from `[http://books.toscrape.com/](http://books.toscrape.com/)`.


* The script navigates through category pages to collect raw data, including the book title, raw price, text-based star rating, availability status, and category.


* The raw price is cleaned by stripping non-numeric characters and converting the string into a float.


* A mapping dictionary converts the text star rating (e.g., 'One', 'Two') into an integer between 1 and 5.


* The availability text is parsed into a boolean integer column named `in_stock`.


* To handle parsing failures, missing values in the `price_gbp` and `rating` fields are imputed using their respective medians to prevent data loss.


* Rows with unparseable `in_stock` values are dropped entirely, as this is a critical categorical feature where ambiguity would compromise the analysis.


* The cleaned `price_gbp` is converted to a `price_inr` column using a project-defined fixed baseline conversion rate of 1 GBP = 105.50 INR.



**Database Design and Querying**

* The cleaned data is loaded into a normalized SQLite database (`books.db`) using `pandas.to_sql`.


* The database schema consists of two linked tables: `categories` (with a unique `category_name` and primary key) and `books` (with a `category_id` foreign key).


* A series of SQL queries demonstrate the use of `SELECT/WHERE`, `ORDER BY`, `LIMIT`, `DISTINCT`, and `BETWEEN` operators.


* An SQL `JOIN` query is executed to combine book titles, ratings, and prices with their corresponding category names.


* The SQL `JOIN` logic is successfully reproduced in-memory using `pandas.merge`, and the outputs are verified to be equivalent.



---

## 🕸️ Project 2: Book Web Scraper & SQLite Database

An automated web scraping script that extracts product data from [Books to Scrape](http://books.toscrape.com/) and stores it in a relational database.

### Key Features:
* **Automated Scraping:** Navigates through multiple categories and paginated results using `requests` and `BeautifulSoup`.
* **Data Cleaning & Enrichment:** Converts string prices to floats, translates GBP to INR, maps text-based star ratings to integers, and parses availability status into booleans. 
* **Database Management:** Dynamically creates an SQLite database (`books.db`) with normalized `categories` and `books` tables, utilizing Foreign Keys for data integrity.
* **SQL Queries:** Executes complex SQL queries via Pandas (e.g., `JOIN` operations, sorting, and filtering by price and rating) to verify and analyze the scraped data.

**Technologies Used:** `requests`, `BeautifulSoup`, `pandas`, `sqlite3`, `re`

# Analytics Pipeline

**Part A — Profiling, Cleaning, and Data Story**

* The Titanic dataset is loaded via Seaborn and saved as a committed offline fallback file named `titanic.csv`.


* Initial data profiling identifies missing values in the 'deck' (77.22%), 'age' (19.87%), 'embarked' (0.22%), and 'embark_town' (0.22%) columns.


* The 'deck' column is dropped from the dataset due to its high percentage of missing data.


* The 'age' column is imputed using the median value of 28.0.


* Rows missing 'embarked' and 'embark_town' values are dropped.


* Univariate analysis shows 65 outliers in the 'age' column and 114 outliers in the 'fare' column.


* The 'fare' distribution is right-skewed, characterized by a mean of 32.10 and a median of 14.45.


* Bivariate analysis demonstrates that females (0.74 survival rate) had a significantly higher survival rate than males (0.18 survival rate).


* Survival rates decrease across passenger classes, with 1st class passengers having the highest survival rate (0.62) and 3rd class passengers having the lowest (0.24).


* A correlation matrix reveals a strong negative relationship (-0.55) between passenger class (`pclass`) and `fare`.


* An exploratory standardization check using `StandardScaler` confirms that the 'age' and 'fare' features can be successfully scaled.



**Part B — Predictive Modeling**

* The dataset is split into training (80%) and testing (20%) sets using stratification to address class imbalance in the target variable.


* A preprocessing pipeline is constructed utilizing a `ColumnTransformer` to apply median imputation and standard scaling to numerical features, and frequent-value imputation with one-hot encoding to categorical features.


* Three classification models (Logistic Regression, Decision Tree, and Random Forest) are trained on the preprocessed data.


* Class imbalance handling is tested by comparing a baseline model against a `class_weight='balanced'` approach and a SMOTE oversampling technique.


* Applying SMOTE oversampling significantly improves the model's Recall and overall F1 score.


* Hyperparameter tuning is performed on the Random Forest classifier using `GridSearchCV` to optimize `n_estimators`, `max_depth`, and `max_features`.


* A regression side-task predicts the `fare` using multivariate linear regression and generates a residual plot.


* The residual plot indicates heteroscedasticity due to a funnel shape, meaning the model struggles with larger fare predictions.


* The best-performing classification pipeline is saved to disk using `joblib` and reloaded to test predictions on raw input samples.

---

## 🤖 Project 3: Zepto RAG GenAI Service 

A Retrieval-Augmented Generation (RAG) backend service designed to answer customer support queries about Zepto's delivery, return, and account policies.

### Key Features:
* **Vector Database Integration:** Embeds Zepto policy documents using `SentenceTransformers` (`all-MiniLM-L6-v2`) and stores them in `ChromaDB` for rapid semantic search.
* **LangGraph Orchestration:** Uses a state graph to classify user intent. Policy-related queries trigger a vector retrieval sequence, while general queries are routed to a direct fallback answer.
* **FastAPI Backend:** Wraps the LangGraph workflow in a modern, fast web API with a `POST /ask` endpoint.
* **Structured Responses:** Returns rigorously typed JSON responses using `Pydantic` models, including the generated answer, source document references, and confidence scores.

**Technologies Used:** `langgraph`, `FastAPI`, `chromadb`, `sentence-transformers`, `pydantic`, `uvicorn`

# Support Assistant

**Ingestion and Orchestration**

* A document corpus containing eight text files detailing Zepto's specific policies (e.g., Delivery, Returns, Memberships, Order Tracking) is generated.


* The policy documents are embedded locally using the `all-MiniLM-L6-v2` model from the `sentence-transformers` library.


* The embeddings and document metadata are stored in a persistent `ChromaDB` collection named `zepto_policies`.


* A structured prompt template is defined, featuring a role-context-task-format-length structure and few-shot examples.


* The conversational flow is orchestrated using a `LangGraph` StateGraph that relies on a `GraphState` TypedDict containing the query, classification intent, context, and a structured answer.


* The workflow contains a `classify_intent` node that dynamically routes the query to either a `retrieve_and_answer` node or a `direct_answer` node.

---

## 🚀 How to Run

### Prerequisites
Make sure you have Python 3.9+ installed. Install the required dependencies for all projects by running:

```bash
pip install pandas seaborn matplotlib requests beautifulsoup4 chromadb sentence-transformers langgraph fastapi uvicorn pydantic nest-asyncio

