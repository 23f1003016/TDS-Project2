# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx",                # For HTTP requests
#   "pandas",               # For data manipulation and analysis
#   "seaborn",              # For data visualization (statistical plots)
#   "matplotlib",           # For general-purpose plotting
#   "openai==0.28",         # For interacting with OpenAI API (pinned to 0.28 to avoid errors)
#   "scikit-learn",         # For machine learning algorithms
#   "tabulate",             # For pretty-printing tables
#   "numpy"                 # For numerical computations (you are using np in the code)
# ]
# ///

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import openai
import sys
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
from sklearn.svm import OneClassSVM
from sklearn.impute import SimpleImputer
from tabulate import tabulate

# Fetch AIPROXY_TOKEN from environment variables
aiproxy_token = os.environ.get("AIPROXY_TOKEN")
if not aiproxy_token:
    print("Error: AIPROXY_TOKEN is not set. Please provide the token.")
    sys.exit(1)

# Configure OpenAI to use AI Proxy
openai.api_base = "https://aiproxy.sanand.workers.dev/openai/v1"
openai.api_key = aiproxy_token

if len(sys.argv) != 2:
    print("Usage: uv run autolysis.py <dataset.csv>")
    sys.exit(1)

filename = sys.argv[1]

# List of common encodings to try
ENCODINGS_TO_TRY = ['utf-8', 'ISO-8859-1', 'latin1', 'utf-16', 'cp1252', 'windows-1252']

# Load dataset with encoding handling
def load_dataset(filename):
    for encoding in ENCODINGS_TO_TRY:
        try:
            data = pd.read_csv(filename, encoding=encoding)
            print(f"Dataset loaded successfully with {encoding} encoding, "
                  f"containing {data.shape[0]} rows and {data.shape[1]} columns.")
            return data
        except UnicodeDecodeError:
            print(f"Error: Encoding issue with {encoding}. Trying next encoding...")
        except FileNotFoundError:
            print(f"Error: The file {filename} was not found. Please check the file path.")
            sys.exit(1)
        except pd.errors.EmptyDataError:
            print(f"Error: The file {filename} is empty. Please provide a valid CSV file.")
            sys.exit(1)
        except Exception as e:
            print(f"Error: An unexpected error occurred while loading the file {filename}. {e}")
            sys.exit(1)
    
    print(f"Error: Could not read the file {filename} with any of the tried encodings.")
    sys.exit(1)

# Data Exploration: Overview of the dataset
def explore_data(data):
    print(f"Loaded data from {filename} with {data.shape[0]} rows and {data.shape[1]} columns.")
    print("Column names:", data.columns)
    print("Data types:", data.dtypes)
    print("Summary statistics:\n", data.describe())
    return data.describe(include='all')

# Generate Correlation Matrix and Heatmap (only for numeric columns)
def generate_correlation_matrix(data):
    numeric_data = data.select_dtypes(include=[np.number])
    if numeric_data.empty:
        print("No numeric columns available for correlation.")
        return
    corr_matrix = numeric_data.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title("Correlation Matrix")
    plt.savefig("correlation_matrix.png")
    plt.close()
    print("Saved correlation heatmap as 'correlation_matrix.png'")

# Generate Histograms for selected numeric columns
def generate_histograms(data):
    numeric_data = data.select_dtypes(include=[np.number])
    selected_columns = ['average_rating', 'ratings_count', 'work_ratings_count', 'work_text_reviews_count']  # Reduced to relevant columns
    for column in selected_columns:
        if column in numeric_data.columns:
            plt.figure(figsize=(8, 6))
            sns.histplot(numeric_data[column], kde=True, color='blue')
            plt.title(f"Histogram of {column}")
            plt.xlabel(column)
            plt.ylabel("Frequency")
            plt.savefig(f"histogram_{column}.png")
            plt.close()
            print(f"Histogram saved as 'histogram_{column}.png'")

# Generate Boxplots for selected numeric columns
def generate_box_plots(data):
    numeric_data = data.select_dtypes(include=[np.number])
    selected_columns = ['average_rating', 'ratings_count', 'work_ratings_count', 'work_text_reviews_count']  # Reduced to relevant columns
    for column in selected_columns:
        if column in numeric_data.columns:
            plt.figure(figsize=(8, 6))
            sns.boxplot(x=numeric_data[column], color='red')
            plt.title(f"Boxplot of {column}")
            plt.xlabel(column)
            plt.savefig(f"boxplot_{column}.png")
            plt.close()
            print(f"Boxplot saved as 'boxplot_{column}.png'")

# Anomaly Detection using Isolation Forest
def anomaly_detection(data):
    numeric_data = data.select_dtypes(include=[np.number])
    imputer = SimpleImputer(strategy='median')
    numeric_data_imputed = imputer.fit_transform(numeric_data)
    iso_forest = IsolationForest(contamination=0.05)
    anomalies = iso_forest.fit_predict(numeric_data_imputed)
    data['Anomaly'] = anomalies
    print(f"Anomalies detected: {sum(anomalies == -1)}")
    return data

# Anomaly Detection using DBSCAN
def dbscan_anomaly_detection(data):
    numeric_data = data.select_dtypes(include=[np.number])
    imputer = SimpleImputer(strategy='median')
    numeric_data_imputed = imputer.fit_transform(numeric_data)
    dbscan = DBSCAN(eps=0.5, min_samples=5)
    labels = dbscan.fit_predict(numeric_data_imputed)
    data['DBSCAN_Anomaly'] = labels
    print(f"DBSCAN Anomalies detected: {sum(labels == -1)}")
    return data

# Anomaly Detection using One-Class SVM
def one_class_svm_anomaly_detection(data):
    numeric_data = data.select_dtypes(include=[np.number])
    imputer = SimpleImputer(strategy='median')
    numeric_data_imputed = imputer.fit_transform(numeric_data)
    svm = OneClassSVM(kernel='rbf', nu=0.05, gamma='scale')
    labels = svm.fit_predict(numeric_data_imputed)
    data['SVM_Anomaly'] = labels
    print(f"One-Class SVM Anomalies detected: {sum(labels == -1)}")
    return data

def analyze_data_with_llm(data_summary):
    prompt = f"""
    You are an expert data analyst, and your task is to analyze the provided dataset summary thoroughly.

    Please provide a comprehensive analysis with the following aspects:

    1. **Correlations**: Identify any notable correlations between features. Are there any strong correlations between numeric or categorical variables? Provide the top correlations and explain their significance.

    2. **Feature Distribution and Descriptive Statistics**: For numeric features, summarize their distribution. What are the mean, median, standard deviation, and range for important numerical features? Are there any skewed distributions or outliers?

    3. **Outliers**: Identify any potential outliers in the dataset. Which data points have extreme values for numeric features? Explain why these outliers might exist (e.g., data entry errors, rare cases, etc.).

    4. **Missing Data**: Provide a detailed analysis of missing data. Which columns have the most missing values, and are there any patterns to these missing values? Could missing data impact the analysis or suggest areas to investigate further?

    5. **Categorical Data Insights**: Explore the distribution of categorical variables (e.g., categories, classes, labels). Are there any categories that are overrepresented or underrepresented in the data? How do they affect other features or target variables?

    6. **Feature Interactions**: Investigate if there are any interactions between features that influence the target variable or other features. For example, how do combinations of features (e.g., two categorical variables or numeric and categorical) affect the distribution of key metrics?

    7. **Trends Over Time**: If time-related features are available, analyze how key variables evolve over time. Are there any noticeable trends, seasonality, or time-dependent patterns that emerge in the dataset?

    8. **General Observations**: Provide any additional insights or observations that might be relevant. Are there any features that stand out as particularly impactful or interesting in terms of predicting the target variable or understanding the data?

    9. **Recommendations**: Based on your analysis, suggest any improvements to the dataset or methodology. Could adding, removing, or transforming features enhance the analysis? Are there any data quality issues that need to be addressed, such as imputation for missing values or handling outliers?

    Here is the data summary for your analysis:
    {data_summary}

    Please provide as much detail as possible in your analysis, including any actionable insights that could guide future steps or inform decisions based on the data.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini", 
            messages=[{"role": "user", "content": prompt}],
        )
        return response['choices'][0]['message']['content']
    except Exception as e: 
        print(f"Error during LLM analysis: {e}")
        return "LLM analysis failed due to an error."
    
def write_narrative(analysis_results, charts, data, filename="data.csv"):
    with open("README.md", "w") as f:
        # Report Title and General Overview
        f.write("# Data Analysis Report\n\n")
        f.write(f"## Data Overview\n")
        f.write(f"Loaded data from `{filename}` with **{data.shape[0]} rows** and **{data.shape[1]} columns**. This dataset includes various attributes about the entities being analyzed, which will be examined for trends, correlations, and anomalies.\n\n")

        # Missing Data Summary using tabulate
        missing = data.isnull().sum().reset_index()
        missing.columns = ['Column Name', 'Missing Values']
        f.write("### Missing Values Summary\n")
        f.write("The table below shows the count of missing values for each column in the dataset.\n")
        f.write(tabulate(missing, headers='keys', tablefmt='pipe', showindex=False))
        f.write("\n\n")

        # Anomalies Detected using tabulate
        anomalies = data['Anomaly'].value_counts().reset_index()
        anomalies.columns = ['Anomaly Value', 'Count']
        f.write("### Anomalies Detected\n")
        f.write(f"Anomalies detected: **{anomalies.get(-1, 0)}** out of **{data.shape[0]}** entries.\n")
        f.write("Here is the breakdown of anomalies:\n")
        f.write(tabulate(anomalies, headers='keys', tablefmt='pipe', showindex=False))
        f.write("\n\n")

        # Correlation Insights using tabulate
        corr_matrix = data.select_dtypes(include=[np.number]).corr()
        highly_correlated = corr_matrix[corr_matrix.abs() > 0.8].stack().reset_index()
        highly_correlated.columns = ['Feature 1', 'Feature 2', 'Correlation']
        
        f.write("### High Correlations\n")
        f.write("We found strong correlations between the following pairs of features in the dataset:\n")
        f.write(tabulate(highly_correlated, headers='keys', tablefmt='pipe', showindex=False))
        f.write("\n\n")

        # Analysis Results Section
        f.write("## Analysis Results\n")
        f.write("Below are the key findings and insights derived from the data analysis:\n")
        f.write(analysis_results)
        f.write("\n\n")

        # Visualizations
        f.write("## Visualizations\n")
        f.write("The following charts provide a graphical representation of key trends and insights in the data.\n")
        for chart in charts:
            f.write(f"![{chart}]({chart})\n")
        
        # Insights and Implications
        f.write("## Insights and Implications\n")
        f.write("The analysis reveals various patterns and anomalies, as well as correlations that could indicate significant relationships between certain features. The visualizations help to highlight these trends more clearly, providing actionable insights.\n")
        f.write("In particular, the strong correlations between certain features suggest that there may be underlying relationships that are important for further analysis. Anomalies detected could point to data collection issues or outliers that deserve closer scrutiny.\n")
        f.write("\n")

if __name__ == "__main__":
    # Load data and generate analysis
    data = load_dataset(filename)
    data_summary = explore_data(data)

    # Generate charts
    generate_correlation_matrix(data)
    generate_histograms(data)
    generate_box_plots(data)

    # Anomaly detection
    data = anomaly_detection(data)
    data = dbscan_anomaly_detection(data)
    data = one_class_svm_anomaly_detection(data)

    # Generate analysis using LLM
    analysis_results = analyze_data_with_llm(str(data_summary))

    # Write narrative and save charts
    charts = ["correlation_matrix.png", "histogram_average_rating.png", "boxplot_average_rating.png"]
    write_narrative(analysis_results, charts, data, filename)
    print("Analysis complete. The results have been written to README.md.")
