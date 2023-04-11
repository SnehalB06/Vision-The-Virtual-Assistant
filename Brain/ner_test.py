import spacy

nlp = spacy.load('en_core_web_sm')

#This method extrats all the named entities in presented text
def getNER(text):
    doc = nlp(text)
    return doc.ents
