import os
import json
import spacy
from spacy.lang.en.stop_words import STOP_WORDS


class textPreprocessor():
    def __init__(self,input_folder,output_folder):
        self.input_folder=input_folder
        self.output_folder=output_folder

        self.nlp = spacy.load("en_core_web_lg")
        self.stop_words = set(spacy.lang.en.stop_words.STOP_WORDS)

        os.makedirs(self.output_folder,exist_ok=True)



    def preprocess_tokenize(self):
        for root, _, files in os.walk(self.input_folder):
            for file in files:
                input_path = os.path.join(root, file)

                # Read the text from the input file
                with open(input_path, 'r', encoding='utf-8') as text_file:
                    text = text_file.read()

                lemmatized_tokens=[]
                doc = self.nlp(text)
                #tokens_lemma = [token.text for token in doc if not token.is_stop and not token.is_punct]
                #applyinging lemmatization and tokenization
                #tokens = [token.text for token in doc if not token.is_stop]
                #lemmatized_tokens=[token.lemma_ for token in tokens]
                #lemmatized_tokens = [token.lemma_ for token in doc if not token.is_stop]
                lemmatized_tokens = [token.lemma_ for token in doc if token.text.lower() not in self.stop_words]




                relative_path = os.path.relpath(input_path, self.input_folder).replace(os.sep, '/')
                output_folder = os.path.join(self.output_folder, os.path.dirname(relative_path))
                os.makedirs(output_folder, exist_ok=True)

                output_txt_filename = os.path.splitext(file)[0] + "_preprocessed.txt"
                output_txt_path = os.path.join(output_folder, output_txt_filename)

                with open(output_txt_path, 'w', encoding='utf-8') as txt_file:
                    txt_file.write(" ".join(lemmatized_tokens))






            




if __name__=="__main__":
    input_folder=r"C:\Users\ideapad\Desktop\ats\data\job_description_folder"
    output_folder=r"C:\Users\ideapad\Desktop\ats\data\job_desc_tokenized"

    preprocessor=textPreprocessor(input_folder,output_folder)

    preprocessor.preprocess_tokenize()