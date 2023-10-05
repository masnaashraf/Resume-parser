import spacy
from spacy.lang.en.stop_words import STOP_WORDS
nlp = spacy.load("en_core_web_sm")

text="planning schedulling activity,scgooling analysis"
doc = nlp(text)

# Get the lemma of the word
lemma = doc[0].lemma_
print(lemma)


text = "planning scheduling activity, schooling analysis"
doc = nlp(text)

# Get the lemma of each word in the document
lemmas = [token.lemma_ for token in doc]

print(lemmas)