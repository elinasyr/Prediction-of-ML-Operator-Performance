from sklearn.datasets import make_regression, make_blobs
from sklearn.datasets import dump_svmlight_file
import os

def datagen(path='datasets/', task='regression', num_samples=3* 10**5, num_features=1):
    file = f'{task}.libsvm'
    chunk_size = 3 * 10**5

    def create_and_append_chunk():
        X, y = make_regression(n_samples=chunk_size, n_features=num_features)
        dump_svmlight_file(X, y, path + 'temp_' + file, zero_based=False)
        os.system(f"cat {path + 'temp_' + file} >> {path + file}")
        os.remove(f"{path + 'temp_' + file}")

    if os.path.exists(path + file):
        os.remove(path + file)
    open(path + file, 'a').close()

    if num_samples > chunk_size:
        num_chunks = num_samples // chunk_size
        for i in range(num_chunks):
            print(f"Creating chunk {i+1} of {num_chunks+1}")
            create_and_append_chunk()

        remainder = num_samples % chunk_size
        if remainder != 0:
            print(f"Creating chunk {num_chunks+1} of {num_chunks+1}")
            create_and_append_chunk()

    else:
        X, y = make_regression(n_samples=num_samples, n_features=num_features)
        dump_svmlight_file(X, y, path + file, zero_based=False)

    dataset_size_mb = os.path.getsize(path + file) / 10**6
    with open(f'{path + file}.meta', 'w') as f:
        f.write(f'num_samples,{num_samples}\n')
        f.write(f'num_features,{num_features}\n')
        f.write(f'dataset_size,{dataset_size_mb}')
        print(f"Dataset size is: {dataset_size_mb} MB")

    return path+file

if __name__ == "__main__":
    print(datagen)