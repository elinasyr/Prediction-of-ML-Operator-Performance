from sparksession import create_spark_session
from datagen import datagen
from performance_monitor import monitor_training
from experiments.experiment_params import random_forest_params

from pyspark.sql import functions as F
from pyspark.sql.functions import count_distinct, col, when
from pyspark.storagelevel import StorageLevel
from pyspark import pandas as pd
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.sql.types import *
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml import Pipeline
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
from pyspark.ml.regression import RandomForestRegressor
#import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#initiate spark
spark = create_spark_session()

#decide parameters
num_samples, num_features = random_forest_params()

#build dataset
file = datagen(task='regression', num_samples=num_samples, num_features=num_features)

#load dataset
data = spark.read.format("libsvm").option("numFeatures", str(num_features)).load(file)
data.persist(StorageLevel.MEMORY_AND_DISK)


#call the performance watcher

#model
model = RandomForestRegressor()

'''paramGrid = ParamGridBuilder() \
    .addGrid(rf.numTrees, [int(x) for x in np.linspace(start = 10, stop = 10, num = 1)]) \
    .addGrid(rf.maxDepth, [int(x) for x in np.linspace(start = 5, stop = 5, num = 1)]) \
    .build()'''

#build model
#pipeline = Pipeline(stages=[rf])

#(trainingData, testData) = data.randomSplit([0.8, 0.2], seed=42)

#evaluator = RegressionEvaluator(labelCol="label", predictionCol="prediction", metricName="rmse")
# Create the cross-validator
#cross_validator = CrossValidator(estimator=pipeline,estimatorParamMaps=paramGrid, evaluator=evaluator, numFolds=3, seed=42)
try:
    monitor_training(model, data, "results/random_forest.json", file+".meta")
except Exception as e:
    print('EXCEPTION!!!!')
    print(e)

spark.stop()
