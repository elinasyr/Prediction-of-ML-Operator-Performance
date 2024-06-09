import random
import os
import numpy as np
import nltk
from nltk.corpus import words
import pandas as pd
import csv 

def datagen_word2vec(path='datasets/', task='word2vec', num_sentences=10**5):
    file = f'{task}.csv'
    file_path = os.path.join(path, file)

    # remove the file if it exists
    if os.path.exists(file_path):
        os.remove(file_path)

    open(file_path, 'a').close()

    # get a list of english words from nltk resource
    nltk.data.path.append(path)
    nltk.download('words')
    english_words = words.words()

    # generate a synthetic dataset of random sentences
    def generate_random_sentence():
        sentence_length = random.randint(5, 15)
        sentence = ' '.join(random.choice(english_words) for _ in range(sentence_length))
        return sentence
    
    with open(file_path, 'a', newline='') as csvfile:  # Open the CSV in append mode
        csv_writer = csv.writer(csvfile)
        for _ in range(num_sentences):
            sentence = generate_random_sentence()
            csv_writer.writerow([sentence])  # Write each sentence as a list in a row
    
    return num_sentences, file_path

    # # tokenize the sentences into lists of words
    # tokenized_corpus = [sentence.split() for sentence in random_corpus]

    # # turn the corpus into a dataframe
    # sentence_data = [Row(tokens=sentence) for sentence in tokenized_corpus]
    # sentence_df = spark.createDataFrame(sentence_data)
    # # sentence_df.write.text(file_path)
    # #sentence_df = spark.createDataFrame(random_corpus, ['sentence'])
    
    # # save to a text file 
    # sentence_df.write.text(file_path)

if __name__ == "__main__":
    print("Generating a new word2vec random dataset.")
    datagen_word2vec() 

