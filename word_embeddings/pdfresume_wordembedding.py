import os
import numpy as np
from transformers import DistilBertTokenizer, DistilBertModel

class WordEmbeddingExtractor():
    def __init__(self,input_folder,output_folder):
        self.input_folder=input_folder
        self.output_folder=output_folder

        os.makedirs(self.output_folder,exist_ok=True)

        self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
        self.model = DistilBertModel.from_pretrained('distilbert-base-uncased')


    def load_and_tokenize_text(self, text):
        # Tokenize and convert text to embeddings
            inputs = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True)
            outputs = self.model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()
            return embeddings



    def extract_word_embeddings(self):
            for root, _, files in os.walk(self.input_folder):
                for file in files:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as text_file:
                        text = text_file.read()
                        category = os.path.basename(root)  
                        output_category_folder = os.path.join(self.output_folder, category)
                        os.makedirs(output_category_folder, exist_ok=True)

                        embeddings = self.load_and_tokenize_text(text)

                    # Save the embeddings as a numpy array
                        output_path = os.path.join(output_category_folder, f"{os.path.splitext(file)[0]}.npy")
                        np.save(output_path, embeddings)


if __name__=="__main__":

    input_folder =r"C:\Users\ideapad\Desktop\ats\data\tokenized_pdf"
    output_folder = r"C:\Users\ideapad\Desktop\ats\data\wordembedded_resume" 


extractor=WordEmbeddingExtractor(input_folder,output_folder)

extractor.extract_word_embeddings()