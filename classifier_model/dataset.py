import pandas as pd
from sklearn.model_selection import train_test_split
import torch
from torch.utils.data import Dataset, DataLoader
from gensim.models import Word2Vec
import numpy as np

class TextDataset(Dataset):
    def __init__(self, data, labels, word2vec_model, transform=None):
        self.data = data
        self.labels = labels
        self.transform = transform
        self.word2vec_model = word2vec_model
        self.vector_dim = word2vec_model.vector_size

    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        text = self.data[index]
        label = self.labels[index]
        if(self.transform):
            text = self.transform(text)
        else:
            text = self.text_to_vector(text)
        return text, label
    
    def text_to_vector(self, text):
        words = list(text)
        vectors = [self.word2vec_model.wv[word] for word in words if word in self.word2vec_model.wv]
        if len(vectors) == 0:
            return np.zeros(self.vector_dim)
        vectors = np.mean(vectors, axis=0)
        return vectors
    
def create_dataloader(data, labels, word2vec_model, batch_size, shuffle=True):
    dataset = TextDataset(data, labels, word2vec_model)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)
    return dataloader

def load_data_from_csv(file_path, text_size=0.3, random_state=13):
    df = pd.read_csv(file_path)
    data = df[' Sequence'].values
    labels = df[' Label'].values
    train_data, test_data, train_labels, test_labels = train_test_split(
        data, labels, test_size=text_size, random_state=random_state
    )
    return train_data, train_labels, test_data, test_labels