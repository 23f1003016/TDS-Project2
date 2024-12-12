# Data Analysis and Anomaly Detection

## Overview

This project provides a comprehensive analysis of datasets using various statistical and machine learning techniques. The primary goal of this project is to explore data, generate insightful visualizations, detect anomalies, and create a detailed narrative report based on the dataset.

The core functionalities of the script include:
- **Data exploration**: Summary statistics, correlation matrix, and data types.
- **Visualization**: Histograms, boxplots, and correlation heatmaps for better understanding of data distributions and relationships.
- **Anomaly detection**: Application of various algorithms (Isolation Forest, DBSCAN, One-Class SVM) to detect and label anomalies in the data.
- **LLM-powered analysis**: Integration of large language models for deep insights and recommendations on dataset features, correlations, and trends.

## Project Structure

- `autolysis.py`: The main script that performs data analysis, visualization, and anomaly detection.
- `goodreads/`: Directory containing results (charts, reports) for the `goodreads.csv` dataset.
- `happiness/`: Directory containing results for the `happiness.csv` dataset.
- `media/`: Directory containing generated media files (charts, reports).

## Features

- **Dynamic Visualizations**: Histograms and boxplots are dynamically generated based on user-selected columns.
- **Comprehensive Anomaly Detection**: Multiple algorithms for robust anomaly detection.
- **In-depth Insights**: Detailed data analysis using large language models for further insights.

## Requirements

- Python 3.11 or higher
- Libraries: `httpx`, `pandas`, `seaborn`, `matplotlib`, `openai`, `scikit-learn`, `tabulate`, `numpy`

## Usage

To run the script on any dataset, simply execute the following command:

```bash
python autolysis.py <dataset.csv>
```

The script will generate visualizations and reports, and output them in the corresponding directory. 

### Example:

```bash
python autolysis.py goodreads.csv
```

This will generate analysis for the `goodreads.csv` dataset and store the results in the `goodreads/` directory.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
