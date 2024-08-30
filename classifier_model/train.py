import torch
import torch.nn as nn
import torch.optim as optim
from dataset import create_dataloader, load_data_from_csv
from model import ProteinClassificationModel
from gensim.models import Word2Vec
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def train_model(model, dataloader, criterion, optimizer, num_epochs):
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        for texts, labels in dataloader:
            texts = torch.tensor(texts, dtype=torch.float32)
            labels = torch.tensor(labels, dtype=torch.float32)
            optimizer.zero_grad()
            outputs = model(texts)
            outputs = outputs.squeeze(1)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(dataloader)}')

def predict(input_text, model, word2vec_model):
    model.eval()
    words = list(input_text) 
    vectors = [word2vec_model.wv[word] for word in words if word in word2vec_model.wv]
    if len(vectors) == 0:
        text_vector = np.zeros(word2vec_model.vector_size)
    else:
        text_vector = np.mean(vectors, axis=0)
    text_vector = torch.tensor(text_vector, dtype=torch.float32).unsqueeze(0)
    with torch.no_grad():
        outputs = model(text_vector)
        probabilities = torch.sigmoid(outputs)
        prediction = (probabilities >= 0.5).long()
    return 'positive' if prediction.item() == 1 else 'negative'

def evaluate_model(model, dataloader):
    model.eval()
    all_labels = []
    all_predictions = []
    with torch.no_grad():
        for texts, labels in dataloader:
            texts = torch.tensor(texts, dtype=torch.float32)
            outputs = model(texts)
            outputs = torch.sigmoid(outputs.squeeze(1))
            predictions = (outputs > 0.5).float()
            all_labels.extend(labels.numpy())
            all_predictions.extend(predictions.numpy())

    # Calculate evaluation metrics
    accuracy = accuracy_score(all_labels, all_predictions)
    precision = precision_score(all_labels, all_predictions)
    recall = recall_score(all_labels, all_predictions)
    f1 = f1_score(all_labels, all_predictions)

    print(f'Accuracy: {accuracy:.4f}')
    print(f'Precision: {precision:.4f}')
    print(f'Recall: {recall:.4f}')
    print(f'F1 Score: {f1:.4f}')

def main():
    file_path = r'C:\Users\Liam\Desktop\Summer Research\Computer-Science-Research-Summer\classifier_model\training_labels.csv'
    word2vec_path = r'C:\Users\Liam\Desktop\Summer Research\Computer-Science-Research-Summer\classifier_model\word2vec_training.py'
    batch_size = 2
    num_epochs = 100
    learning_rate = 0.001

    word2vec_model = Word2Vec.load(r'C:\Users\Liam\Desktop\Summer Research\Computer-Science-Research-Summer\classifier_model\word2vecProtein.model')
    input_dim = word2vec_model.vector_size
    num_classes = 2

    train_data, train_labels, test_data, test_labels = load_data_from_csv(file_path)
    train_dataloader = create_dataloader(train_data, train_labels, word2vec_model, batch_size)
    test_dataloader = create_dataloader(test_data, test_labels, word2vec_model, batch_size, shuffle=False)

    model = ProteinClassificationModel(input_dim)
    criterion = torch.nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    train_model(model, train_dataloader, criterion, optimizer, num_epochs)
    print("Model Training Success")

    print("Evaluating on Test Data:")
    evaluate_model(model, test_dataloader)

    test_input = "MQRNGVLECSVCHSKVAVPSPRSVSRAYDKHRSKISSKYRALNVLLVSGDCILVGLQPILVFMSKVDGKFQFSPISVNFLTEVAKVIFAIVMLVIESRKQKVGEKPLLSLSTFVQAARNNVLLAVPALLYAINNYLKFIMQLYFNPSTVKMLSNLKVLVIAVLLKVIMRRKFSIIQWEALALLLIGISVNQLRSIPEGTNAFGLPVTAIAYAYTLIFVSVPSFASVYNEYALKSQFDTSIYLQNLFLYGYGAIFNFLGILGTVIFQGPESFDIFRGHSRATLFLICNNAAQGILSSFFFKYADTILKKYSSTVATIFTGLASAAFLGQPLTVNFLLGISIVFISMHQFFSPLAKVKDEKPAGTVELGDSQNHRSSESSFVNMTAGATDDARHLNATDERKPLLPI"
    prediction = predict(test_input, model, word2vec_model)
    print(f'The predicted sentiment for "{test_input}" is {prediction}.')

if __name__ == "__main__":
    main()
