import time
import psutil
import numpy as np
from pyspark.sql import SparkSession
from pyspark.ml.feature import Word2Vec
from pyspark.ml.feature import Tokenizer
import pandas as pd
from sparksession import create_spark_session
from datagen_word2vec import datagen_word2vec
from performance_monitor import monitor_training


#initiate spark
spark = create_spark_session()

# build dataset 
# generate a random num of sentences to produce 
#num_sentences = np.random.randint(10**2,5*(10**6),size=1)
num_sentences, file = datagen_word2vec(num_sentences=1000)

#load dataset
data = spark.read.csv(file, header=False, inferSchema=True)
input_col = data.schema.fieldNames()[0]
tokenizer = Tokenizer(inputCol=input_col, outputCol="words")
tokenized_data = tokenizer.transform(data)

model = Word2Vec(vectorSize=100, minCount=1, inputCol="words", outputCol="word2vec_model")

start_time = time.time()
model.fit(tokenized_data)
end_time = time.time()
print("Fitting lasted: ", end_time - start_time)
# # tokenize them into lists of words to train the model
# tokenizer = Tokenizer(inputCol="sentence", outputCol="words")
# tokenized_sentences = tokenizer.transform(data)

# # configure Word2Vec
# model = Word2Vec(tokenized_sentences, vectorSize=100, minCount=1, inputCol="words", outputCol="word2vec_model")



