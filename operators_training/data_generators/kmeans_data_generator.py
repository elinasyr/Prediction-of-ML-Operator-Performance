from sklearn.datasets import make_blobs
from sklearn.datasets import dump_svmlight_file
import os
import numpy as np

def clustering_generate_data(num_samples, num_features, num_centers):
    chunk_size = 10**6

    # Create or truncate the main data file and meta file
    with open('data.libsvm', 'w') as data_file, open('data.libsvm.meta', 'w') as meta_file:
        pass

    if num_samples > chunk_size:
        num_chunks = num_samples // chunk_size

        for i in range(num_chunks):
            print(f"Creating chunk {i + 1} of {num_chunks}")
            X, y = make_blobs(n_samples=chunk_size, n_features=num_features, centers=num_centers)
            dump_svmlight_file(X, y, 'data_temp.libsvm', zero_based=False)

            # Concatenate chunks into the main data file
            os.system("cat data_temp.libsvm >> data.libsvm")

        remainder = num_samples % chunk_size
        if remainder != 0:
            print(f"Creating chunk {num_chunks + 1} of {num_chunks}")
            X, y = make_blobs(n_samples=remainder, n_features=num_features, centers=num_centers)
            dump_svmlight_file(X, y, 'data_temp.libsvm', zero_based=False)
            os.system("cat data_temp.libsvm >> data.libsvm")

    else:
        X, y = make_blobs(n_samples=num_samples, n_features=num_features, centers=num_centers)
        dump_svmlight_file(X, y, 'data.libsvm', zero_based=False)

    # Update the meta file
    with open('data.libsvm.meta', 'a') as meta_file:
        meta_file.write(f'num_samples,{num_samples}\n')
        meta_file.write(f'num_features,{num_features}\n')
        meta_file.write(f'num_classes,{len(np.unique(y))}\n')
        meta_file.write(f'dataset_size,{os.path.getsize("data.libsvm") / 10**6}\n')
        print(f"Dataset size is: {os.path.getsize('data.libsvm') / 10**6} MB")

    return num_features, num_centers, num_samples
