from pyspark.sql import SparkSession

# Create a Spark Session
def create_spark_session():
    spark = SparkSession.builder.master("spark://10.0.0.1:7077")\
        .config("spark.dynamicAllocation.enabled", "false")\
        .config("spark.executor.instances", "2")\
        .config("spark.driver.memory", "2g")\
        .config("spark.executor.cores", "1")\
        .config("spark.cleaner.periodicGC.interval", "1min")\
        .getOrCreate()
    print("Spark session created")
    return spark

hdfs_path = "hdfs://10.0.0.1:9000/data/"