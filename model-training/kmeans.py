from pyspark.ml.clustering import KMeans
from operators_training.data_generators.kmeans_data_generator import generate_cluster_data 
from .. import performance_monitor as pm
from pyspark.storagelevel import StorageLevel
from .. import sparrksession as ss
import numpy as np

# define the clustering dimensions

def kmeans_dataset_dimensions():
    num_samples = np.random.randint(10**2, 10**7)
    num_features = np.random.randint(2, 100)
    num_centers = np.random.randint(2, 20)
    
    return {"num_samples": num_samples, "num_features": num_features, "num_centers": num_centers}

def log_results(log_filename, num_samples, num_features, num_centers, success=True):
    with open(log_filename, "a") as file:
        status = "DONE" if success else "ERROR"
        output = f"{status}: samples: {num_samples}, features: {num_features}, centers: {num_centers}\n"
        file.write(output)

# Create Spark session
spark = ss.create_spark_session()

# Generate dataset dimensions
kmeans_dimensions = kmeans_dataset_dimensions()

try:
    # Generate cluster data
    num_samples, num_features, num_centers = generate_cluster_data(
        kmeans_dimensions['num_samples'], kmeans_dimensions['num_features'], kmeans_dimensions['num_centers']
    )

    # Load the dataset
    dataset = spark.read.format("libsvm").option("numFeatures", str(num_features)).load("data.libsvm")
    dataset.persist(StorageLevel.MEMORY_AND_DISK)

    # Define the k-means clustering model
    kmeans = KMeans().setK(num_centers).setSeed(1).setInitMode("k-means").setMaxIter(10)

    # Monitor training and log results
    pm.monitor_training(kmeans, dataset, "./results/kmeans.csv")
    log_results("exec_log_kmeans.txt", num_samples, num_features, num_centers)

except Exception as e:
    log_results("exec_log_kmeans.txt", num_samples, num_features, num_centers, success=False)
    print(f"Error: {str(e)}")

finally:
    # Unpersist the dataset and clean up resources
    if 'dataset' in locals():
        dataset.unpersist()
    if 'kmeans' in locals():
        del kmeans

# Free the memory
del num_features
del num_centers

# Stop the Spark session
# spark.stop()