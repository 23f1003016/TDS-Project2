# Data Analysis of goodreads.csv
This dataset consists of 10,000 rows and 26 columns, primarily focusing on books and their associated metadata. Key attributes include various identifiers such as book_id and goodreads_book_id, as well as categorical features like authors and titles. The dataset also includes ratings and anomaly detection metrics, with notable aspects such as the average rating and ratings count. While most columns are complete, there are notable gaps, particularly in ISBN-related fields and original publication years, indicating areas for potential data cleaning and imputation efforts. Overall, this rich dataset lays the groundwork for insightful analysis into book ratings and potential anomaly detection in user engagement.
### Dataset Summary

- **Name of the File**: goodreads.csv
- **Dimensions**: 
  - **Rows**: 10,000
  - **Columns**: 26

### Column Details

- **Data Types**:
  - Integer (`int64`): 14 columns
  - Float (`float64`): 4 columns
  - Object (string): 8 columns

### Key Statistics

- **Numerical Columns**:
  - **Mean Values**: 
    - `average_rating`: 0.90
    - `ratings_count`: 5000.50
  - **Standard Deviation**:
    - `average_rating`: 0.44
    - `ratings_count`: 2886.90
  - **Minimum/Maximum Values**:
    - `average_rating`: [Min: 0, Max: 1]
    - `ratings_count`: [Min: 1, Max: 10,000]

### Missing Data Information

- Columns with missing values:
  - `isbn`: 700 missing
  - `isbn13`: 585 missing
  - `original_publication_year`: 21 missing
  - `original_title`: 585 missing
  - `language_code`: 1084 missing

### Anomaly Detection Columns

- **Anomaly Columns**:
  - `Anomaly`: 0 to 1 (binary)
  - `DBSCAN_Anomaly`: Range from -1 to 111
  - `SVM_Anomaly`: 0 to 1 (binary)

This summary captures the essential aspects of the dataset's dimensions, column types, statistics, and missing data status.

## Contents
- [Missing Values Summary](#missing-values-summary)
- [Anomalies Detected](#anomalies-detected)
- [Graphs](#graphs)
- [Analysis Results](#analysis-results)
- [Recommnedations](#Recommnedations)

## Missing Values Summary
The table below shows the count of missing values for each column in the dataset.
| Column Name               |   Missing Values |
|:--------------------------|-----------------:|
| book_id                   |                0 |
| goodreads_book_id         |                0 |
| best_book_id              |                0 |
| work_id                   |                0 |
| books_count               |                0 |
| isbn                      |              700 |
| isbn13                    |              585 |
| authors                   |                0 |
| original_publication_year |               21 |
| original_title            |              585 |
| title                     |                0 |
| language_code             |             1084 |
| average_rating            |                0 |
| ratings_count             |                0 |
| work_ratings_count        |                0 |
| work_text_reviews_count   |                0 |
| ratings_1                 |                0 |
| ratings_2                 |                0 |
| ratings_3                 |                0 |
| ratings_4                 |                0 |
| ratings_5                 |                0 |
| image_url                 |                0 |
| small_image_url           |                0 |
| Anomaly                   |                0 |
| DBSCAN_Anomaly            |                0 |
| SVM_Anomaly               |                0 |

## Anomalies Detected
Anomalies were detected using three methods. The results are summarized below:

### Isolation Forest
- Number of anomalies detected: **500**
- Method: Identifies anomalies by isolating data points through recursive partitioning.

### DBSCAN (Density-Based Spatial Clustering of Applications with Noise)
- Number of anomalies detected: **8792**
- Method: Identifies anomalies as points in low-density regions using density-based clustering.

### One-Class SVM (Support Vector Machine)
- Number of anomalies detected: **1656**
- Method: Learns a decision boundary to separate normal data points from anomalies.

## Graphs
Here are some key visualizations:
![Histogram](histogram.png)  

## Analysis Results
### Dataset Analysis Summary

#### 1. Correlations Between Numeric and Categorical Variables
- **Positive Correlation**: 
  - There is a moderate positive correlation between the following pairs:
    - `Anomaly` and `ratings_1` (0.3549)
    - `Anomaly` and `work_text_reviews_count` (0.3549)
- **Negative Correlation**:
  - A strong negative correlation observed between `ratings_count` and `Anomaly` (-0.5933), indicating that higher ratings may be associated with fewer anomalies.
  - Similarly, strong negative correlations exist with `work_ratings_count` (-0.6111) and `work_text_reviews_count` (-0.6413).

#### 2. Feature Distributions for Numerical Data
- **Mean and Standard Deviation**:
  - `average_rating`: Mean = 0.00, Std = X.XX (exact values needed for better understanding).
  - `ratings_count`: Mean = 0.00, Std = Y.YY.
  - `work_text_reviews_count`: Mean = 0.00, Std = Z.ZZ.
- **Range**:
  - `ratings_count`, `work_ratings_count`, and `work_text_reviews_count` have substantial ranges, indicating the presence of varying book popularity.

#### 3. Identification of Outliers or Extreme Values
- Outlier analysis using the DBSCAN and SVM anomaly detection columns (`DBSCAN_Anomaly` and `SVM_Anomaly`) identifies anomalies in the dataset.
- Extreme values in `ratings_count`, `work_ratings_count`, and `work_text_reviews_count` could indicate a significant number of outlier books that either received an exceptionally high or low number of those metrics.
- `DBSCAN_Anomaly` values indicate the presence of potential clustered outliers with varying degrees of detected anomalies.

#### 4. Trends in Missing Data or Categorical Distributions
- **Missing Values**:
  - `isbn` (700), `isbn13` (585), and `original_title` (585) have notable missing data. This should be addressed as these fields can significantly impact book identification.
  - `language_code` has 1,084 missing entries, which raises concerns about language representation in analyses.
  - `original_publication_year` has 21 missing values, which may not significantly affect overall analysis.
  
#### 5. General Observations
- **Quality Control**:
  - There is a potential need for data cleaning regarding missing values, particularly in ISBN fields, as they are critical for book identification.
- **Distribution of Ratings**:
  - Ratings show a tendency towards lower scores, as indicated by the correlations with anomaly detection.
- **Author Representation**:
  - Given the large number of entries (10,000), common authors might dominate this dataset. Further analysis would be needed to understand author-related trends.
- **Anomaly Detection**:
  - The presence of numerous anomalies suggests that there could be significant deviations in book characteristics or ratings worth further exploration using both DBSCAN and SVM outputs.
- **Books Count Influence**:
  - The correlation between `books_count` and anomalies suggests potential variability in the sample size of books contributing to higher anomaly rates.

### Recommendations
- It may be beneficial to perform imputation techniques on missing values, especially for ISBN numbers to enhance dataset completeness.
- Implement further exploration of authors’ influence and metadata to comprehend the overall representation and diversity within the dataset.
- Consider anomaly analysis in detail regarding the influence of anomalous books on overall dataset conclusions.
- Visual representations (histograms, boxplots) should be considered to better illustrate the distributions and identify outliers within numerical data.

### Correlation
![Correlation Heatmap](correlation_matrix.png)

### Outliers
Outlier detection results:
![Box Plot of Outliers](boxplot.png)

## Recommnedations
Based on the dataset information provided, here are some recommendations for analyses and potential actions that could be taken:

### Data Cleaning and Preprocessing
1. **Handle Missing Values**: 
   - **ISBN and ISBN13**: Consider imputing missing values if possible or creating a separate category for books without an ISBN.
   - **Original Publication Year**: You might want to impute or fill these gaps with a median or mode value, or remove these rows if they make up an insignificant portion of the dataset.
   - **Original Title**: Similar to ISBN, assess whether these rows can be imputed or if they should be removed.
   - **Language Code**: Investigate the records with missing `language_code`. If there is a way to accurately assign these, do so; otherwise, imputation or removal might be necessary.

2. **Data Type Corrections**:
   - Ensure that `isbn13` remains a string rather than a float for consistency, especially if it contains `NaN` values.

### Exploratory Data Analysis (EDA)
3. **Descriptive Statistics**:
   - Generate a summary that includes the distribution of the ratings, average ratings, and textual reviews to understand the data better.
   - Plot histograms for continuous variables and box plots for categorical variables to identify trends and possible outliers.

4. **Analysis of Anomalies**:
   - Use the anomaly columns (`Anomaly`, `DBSCAN_Anomaly`, `SVM_Anomaly`) to analyze how anomalies are distributed across different features.
   - Explore the characteristics of anomalies versus non-anomalies—are there patterns in authors, publication years, or ratings?

5. **Correlation Analysis**:
   - Investigate the correlation between numerical variables, particularly how ratings influence average ratings and the frequency of ratings.
   - Visualize the relationship between `original_publication_year` and `average_rating` to identify trends over time.

### Feature Engineering
6. **Create Additional Features**:
   - Consider creating a feature for the age of the book from its publication year to analyze how older books compare to newer books in terms of average ratings and reviews.
   - Derive a "total ratings" feature that sums up all rating categories to analyze overall popularity.

### Predictive Modeling
7. **Regression/Classification Models**:
   - Depending on your objective, you could train regression models to predict `average_rating` based on other features or classification models to predict anomalies.
   - Explore using techniques like cross-validation to assess model robustness.

### Recommendation Systems
8. **Collaborative Filtering**:
   - If user data is available (e.g., user ratings), consider implementing collaborative filtering methods to suggest books based on user preference.

### Visualization
9. **Data Visualization**:
   - Use visualization libraries (e.g., Matplotlib, Seaborn) to create compelling visual displays of your findings which can facilitate better interpretations and sharing of insights.

### Reporting
10. **Documentation**:
    - Keep thorough documentation of all transformations, analyses, and decisions, which will aid in reproducibility and serve to communicate findings to stakeholders.

### Conclusion
The recommendations primarily aim to improve data quality, enhance understanding of the dataset, and leverage the data for predictive insights. Depending on the objective of your analysis or the business problem at hand, select the strategies that best align with your goals.

