import pandas as pd
from gensim.models import Word2Vec
import os

csv_path = r'C:\Users\Liam\Desktop\Summer Research\Computer-Science-Research-Summer\Mo_full_sequence_list.csv'
train_data = pd.read_csv(csv_path)


#sq = [list(seq) for seq in train_data['Sequence'].values]

# Prepare sentences for Word2Vec
sequences = train_data[' Sequence'].apply(list).tolist()

# Train Word2Vec model
word2vec_model = Word2Vec(sequences, vector_size=100, window=5, min_count=1, sg=1, epochs=10)
model_path = r'C:\Users\Liam\Desktop\Summer Research\Computer-Science-Research-Summer\classifier_model\word2vecProtein.model'
word2vec_model.save(model_path)
print(f"Model saved to {model_path}")