import os, sys, time, json, requests, csv, psutil
from datetime import datetime
from sparkmeasure import StageMetrics
from pyspark import StorageLevel

#things to monitor
#total time
#min/max/avg cpu
#min/max/avg main memory usage

def monitor_training(model, data, file, meta, parameters=None):

    #helper to get app id
    def get_app_id():
        response = requests.get("http://192.168.1.234:4040/api/v1/applications")
        applications = json.loads(response.text)
        app_id = applications[0]["id"]
        return app_id
    
    #helper to get executors
    def get_executors(app_id):
        response = requests.get(f"http://192.168.1.234:4040/api/v1/applications/{app_id}/executors")
        executors = json.loads(response.text)
        return executors
    
    # Calculate the average CPU usage
    def get_average_cpu_usage(executors):
        total_cpu = 0
        for executor in executors:
            print
            total_cpu += executor["totalCores"]
        average_cpu = total_cpu / len(executors)
        return average_cpu

    # Calculate the total memory usage
    def get_total_memory_usage(executors):
        total_memory = 0
        for executor in executors:
            total_memory += executor["memoryUsed"]
        return total_memory

    # get the total time
    def get_total_time(executors):
        total_time = 0
        for executor in executors:
            total_time += executor["totalDuration"]
        return total_time

    # Function to load existing data from the results.json file
    def load_results(filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            # Initialize an empty list if the file doesn't exist
            data = []
        return data

    # Function to append new experiment data to the results.json file
    def append_experiment_data(filename, experiment_data):
        # Add a timestamp to the new experiment data
        experiment_data["timestamp"] = str(datetime.now())

        # Load existing data
        data = load_results(filename)

        # Append the new experiment data
        data.append(experiment_data)

        # Write the updated data back to the file
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    # Start a process to measure the CPU and memory usage
    #process = psutil.Process()

    start_time = time.time()
    timestamp = str(datetime.now())

    model.fit(data)

    end_time = time.time()

    total_time = end_time - start_time

    app_id = get_app_id()
    executors = get_executors(app_id)

    #Get the total memory from all the executors
    memory_usage = get_total_memory_usage(executors)

    # Read the values from the data.libsvm.meta file
    with open(meta, "r") as meta_file:
        reader = csv.DictReader(meta_file, fieldnames=["key", "value"], delimiter=",")
        meta_values = {}
        for row in reader:
            meta_values[row["key"]] = row["value"]

    new_experiment = {
        "timestamp": timestamp,
        "totalTime": total_time,
        "memoryUsage": memory_usage,
    }
    append_experiment_data(file, {**new_experiment, **meta_values})

    #print(total_time, ' seconds')

