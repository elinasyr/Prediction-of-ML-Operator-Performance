import sys
import numpy as np
import json

def read_config(filename):
    try:
        with open(filename, 'r') as file:
            config = json.load(file)
        return config
    except Exception as e:
        print("Failed reading config file")
        exit()

def random_forest_params():
    config = read_config('./experiments/config.json')["random_forest"]
    num_samples = np.random.randint(eval(config["num_samples_min"]), eval(config["num_samples_max"]))
    num_features = np.random.randint(eval(config["num_features_min"]), eval(config["num_features_max"]))
    return num_samples, num_features

def clustering_dataset_dimensions():
    rows = np.random.randint(10**2,10**7,size=1)
    cols = np.random.randint(2,100,size=1)
    centers = np.random.randint(2,20,size=1)
    return {"num_samples": int(rows), "num_features": int(cols), "num_centers": int(centers)}