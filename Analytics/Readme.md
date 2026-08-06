# Titanic Survival Prediction and Fare Prediction Project

This notebook demonstrates a comprehensive data science workflow, from exploratory data analysis and cleaning to predictive modeling, using the classic Titanic dataset. It covers both classification (survived/not survived) and regression (predicting fare) tasks, along with advanced topics like imbalance handling and hyperparameter tuning.

## Table of Contents

1.  [Part A — Profiling, Cleaning, and the Data Story](#part-a---profiling-cleaning-and-the-data-story)
    *   [Task 1: Load the dataset and profile it](#task-1-load-the-dataset-and-profile-it)
    *   [Missing Value Analysis](#missing-value-analysis)
    *   [Task 2: Apply missing-value handling](#task-2-apply-missing-value-handling)
    *   [Task 3: Univariate Analysis](#task-3-univariate-analysis)
    *   [Task 4: Bivariate Analysis](#task-4-bivariate-analysis)
    *   [Task 5: Multivariate 'Data Story' and Exploratory Standardization Check](#task-5-multivariate-data-story-and-exploratory-standardization-check)
    *   [Task 6: Exploratory Standardization Check (Age and Fare)](#task-6-exploratory-standardization-check-age-and-fare)
2.  [Part B — Predictive Modeling](#part-b---predictive-modeling)
    *   [Task 7: Split the data into train/test sets with stratification](#task-7-split-the-data-into-traintest-sets-with-stratification)
    *   [Task 8: Preprocessing (fit on training data only)](#task-8-preprocessing-fit-on-training-data-only)
    *   [Task 9: Train three classifiers](#task-9-train-three-classifiers)
    *   [Task 10: Evaluate all three models](#task-10-evaluate-all-three-models)
    *   [Task 11: Imbalance handling comparison](#task-11-imbalance-handling-comparison)
    *   [Task 12: Hyperparameter tuning](#task-12-hyperparameter-tuning)
    *   [Task 13: Regression side-task - Predict `fare` using multivariate linear regression](#task-13-regression-side-task---predict-fare-using-multivariate-linear-regression)
    *   [Task 14: Create the Classification Model Comparison Table and Regression Metrics](#task-14-create-the-classification-model-comparison-table-and-regression-metrics)
    *   [Task 15: Saving and reloading the best-performing complete pipeline](#task-15-saving-and-reloading-the-best-performing-complete-pipeline)

## Part A — Profiling, Cleaning, and the Data Story

### Task 1: Load the dataset and profile it

The project begins by loading the Titanic dataset using `seaborn.load_dataset`. Basic profiling (`df.info()`, `df.describe()`, `df.shape`) is performed to understand the dataset's structure, data types, and initial statistics. The dataset is also saved locally as `titanic.csv` for offline access.

### Missing Value Analysis

Identified columns with missing values and their respective percentages, specifically 'deck', 'age', 'embarked', and 'embark_town'.

### Task 2: Apply missing-value handling

Different strategies were applied for handling missing values:
*   **'deck'**: Dropped due to a high percentage of missing values (77.22%).
*   **'age'**: Imputed with the median value (28.0) to preserve the distribution.
*   **'embarked'** and **'embark_town'**: Rows with missing values were dropped as they constituted a very small percentage (0.22%) of the dataset.

The DataFrame's info and shape were re-checked to confirm the changes.

### Task 3: Univariate Analysis

Univariate analysis was performed on 'age' and 'fare' to understand their distributions. Histograms and box plots were generated. Outliers were identified using the Interquartile Range (IQR) method. Descriptive statistics (mean, median, mode) for 'fare' were calculated, and its skewness was determined, revealing a right-skewed distribution.

### Task 4: Bivariate Analysis

This section explored relationships between pairs of variables:
*   **Survival Rate by Sex**: Females had a significantly higher survival rate.
*   **Survival Rate by Pclass**: Survival rate decreased with lower passenger class (3rd class had the lowest).
*   **Survival Rate by Sex and Pclass**: Combined analysis showed 1st class females had the highest survival rate, and 3rd class males the lowest.
*   **Correlation Matrix**: A heatmap of correlations between numeric features (`survived`, `pclass`, `age`, `sibsp`, `parch`, `fare`) was generated. The strongest negative correlation was found between `pclass` and `fare` (-0.55), indicating that higher class passengers paid higher fares.

### Task 5: Multivariate 'Data Story' and Exploratory Standardization Check

Several multivariate charts were created to tell a data story:
*   **Survival Rate by Pclass and Sex (Bar Plot)**: Reinforced that females in higher classes had much better survival chances.
*   **Age Distribution by Survival Status (Violin Plot)**: Suggested younger individuals (children) had higher survival rates.
*   **Fare Distribution by Passenger Class and Survival Status (Box Plot)**: Showed that survivors generally paid higher fares within each class.
*   **Age, Fare, Pclass and Survival (Scatter Plot)**: Illustrated that survival was a complex interplay of these factors, with clusters of survivors among higher-paying, 1st-class passengers, and younger individuals.

### Task 6: Exploratory Standardization Check (Age and Fare)

An exploratory check on standardization was performed using `StandardScaler` on 'age' and 'fare'. This confirmed that these features could be successfully transformed to have a mean of approximately 0 and a standard deviation of 1, which is often a crucial step for many machine learning algorithms.

## Part B — Predictive Modeling

### Task 7: Split the data into train/test sets with stratification

The data was split into training (80%) and testing (20%) sets using `train_test_split`. Stratification by the 'survived' target variable was applied to ensure similar proportions of survivors/non-survivors in both sets, addressing class imbalance.

### Task 8: Preprocessing (fit on training data only)

A `ColumnTransformer` and `Pipeline` were used to create a robust preprocessing workflow:
*   **Numerical Features** (`age`, `sibsp`, `parch`, `fare`): Imputed with median and scaled using `StandardScaler`.
*   **Categorical Features** (`sex`, `pclass`, `embark_town`): Imputed with the most frequent value and one-hot encoded using `OneHotEncoder`.

The preprocessor was fit *only* on the training data (`X_train`) and then applied to both training (`X_train_processed`) and testing (`X_test_processed`) sets. Feature names after one-hot encoding were also extracted.

### Task 9: Train three classifiers

Three classification models were trained on the preprocessed training data:
*   **Logistic Regression**
*   **Decision Tree Classifier** (with a visualization of the tree)
*   **Random Forest Classifier**

### Task 10: Evaluate all three models

Each trained classifier was evaluated on the preprocessed test set using several metrics:
*   Accuracy
*   Precision
*   Recall
*   F1 Score
*   ROC AUC Score
*   Confusion Matrix

A comparison table of these metrics was displayed, and ROC curves for all models were plotted to visually assess their performance.

### Task 11: Imbalance handling comparison

To address the imbalance in the 'survived' class (38.26% survived), three strategies were compared using Logistic Regression:
*   **Baseline**: No specific imbalance handling.
*   **`class_weight='balanced'`**: Automatically adjusts weights inversely proportional to class frequencies.
*   **SMOTE (Synthetic Minority Over-sampling Technique)**: Oversamples the minority class in the training data.

Evaluation metrics (Precision, Recall, F1 Score) were compared for each strategy. SMOTE showed a good balance between precision and recall, leading to an improved F1-score.

### Task 12: Hyperparameter tuning

Hyperparameter tuning for the Random Forest Classifier was performed using `GridSearchCV` with 5-fold cross-validation. The F1-score was used as the scoring metric. The best parameters (`n_estimators`, `max_depth`, `max_features`) were identified, and the corresponding Out-of-Bag (OOB) score and F1-score on the test set were reported.

### Task 13: Regression side-task - Predict `fare` using multivariate linear regression

A separate regression task was conducted to predict the `fare` using a multivariate linear regression model. The process involved:
1.  Defining `X_reg` and `y_reg` (dropping 'fare', 'survived', 'alive' from features).
2.  Creating a preprocessing pipeline similar to the classification task for numerical and categorical features.
3.  Splitting the regression data into training and testing sets.
4.  Training a `LinearRegression` model within a pipeline.
5.  Reporting key regression metrics: Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), R-squared (R²), and Adjusted R².
6.  Generating a residual plot to visually inspect the model's errors.
7.  Providing an analysis of the residual plot to assess for heteroscedasticity.

### Task 14: Create the Classification Model Comparison Table and Regression Metrics

This task consolidates the evaluation results into two clear tables:
*   **Classification Model Comparison Table**: Summarizes Accuracy, Precision, Recall, F1 Score, and ROC AUC for Logistic Regression, Decision Tree, and Random Forest models.
*   **Regression Model Metrics**: Presents MAE, RMSE, R², and Adjusted R² for the fare prediction model.

Finally, a written recommendation is provided, identifying Logistic Regression as the most robust choice for deployment in the classification task due to its strong overall performance and balance between interpretability and predictive power.

### Task 15: Saving and reloading the best-performing complete pipeline

The best-performing classification pipeline (Logistic Regression with its associated preprocessing steps) was saved to disk using `joblib`. A script was included to demonstrate reloading the saved pipeline and making a prediction on a sample from the raw test data, confirming its functionality for future deployment.


