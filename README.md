# Prediction of ML Operator Performance

This project was undertaken as part of my engineering studies at the School of Electrical and Computer Engineering, National Technical University of Athens. The aim of the project is to predict the performance of Machine Learning (ML) operators executed in big data analytics runtimes (such as Apache Spark or Apache Flink) without actually executing them. This involves measuring the execution progress of these operators over time and utilizing a learning algorithm to create a predictive model. We also wrote a [report](https://github.com/elinasyr/Prediction-of-ML-Operator-Performance/blob/main/D4a__Prediction_of_ML_Operator_Performance.pdf) about this.


## Project Overview

The main aspects tackled in this project are:

1. **Installation and Setup**: 
   - Successfully installed and set up an open-source, distributed analytics engine (Apache Spark) on local or Okeanos-based resources.

2. **Selection of Operators**: 
   - Chose a minimum of three diverse operators from the same family for performance modeling. In this project, we used the following Spark MLlib operators:
     - K-means
     - Random Forest Regression
     - Word2Vec

3. **Data Generation and Loading**:
   - Generated artificial data of varying sizes and structures using a data generator. The data was:
     - Of different sizes (small/medium to large, beyond main memory capacity)
     - Of different structures (e.g., graphs of various types, data points of different dimensions)

4. **Performance Measurement and Modeling**:
   - Executed multiple combinations of data and operators, monitored the execution metrics, and collected data such as:
     - Total running time
     - Min/Max/Avg CPU usage
     - Main memory usage
     - Other useful statistics

   - Fed the collected data into a suitable learning algorithm (e.g., neural network, regression, random forest) to create a performance prediction model with minimal error for unseen data inputs.

## Project Steps

### 1. Installation and Setup

- Installed Apache Spark, an open-source, distributed analytics engine.
- Configured the environment for optimal performance using local or Okeanos-based resources.

### 2. Selection of Operators

- Selected three diverse operators from Apache Spark MLlib:
  - **K-means**: Clustering algorithm
  - **Random Forest Regression**: Ensemble learning method for regression
  - **Word2Vec**: Neural network model for learning word embeddings

### 3. Data Generation and Loading

- Created synthetic datasets using a data generator:
  - Ensured data varied in size from small to large, beyond main memory capacity.
  - Ensured data had different structures to test the versatility of the operators.

### 4. Performance Measurement and Modeling

- Executed the selected operators on the generated datasets.
- Collected performance metrics:
  - Total running time
  - CPU usage (min, max, average)
  - Main memory usage
- Utilized the collected data to train a machine learning model to predict the performance of the operators:
  - Experimented with different learning algorithms (neural networks, regression, random forests) to find the most accurate model.

## Conclusion

By the end of the project, a predictive model was developed to accurately forecast the performance of ML operators in Apache Spark. This project provided valuable insights into ML processing in big data environments and enhanced understanding of performance modeling and prediction.

## References

- Apache Spark MLlib Guide: [https://spark.apache.org/docs/latest/ml-guide.html](https://spark.apache.org/docs/latest/ml-guide.html)


**Institution**: National Technical University of Athens, School of Electrical and Computer Engineering
