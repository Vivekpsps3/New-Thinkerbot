from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
import numpy as np
from scipy.special import softmax
import nltk
from ekphrasis.classes.tokenizer import SocialTokenizer
import spacy
#nltk.download('punkt')

#clause splitting code
#https://subscription.packtpub.com/book/data/9781838987312/2/ch02lvl1sec13/splitting-sentences-into-clauses
'''
This function returns the root of a sentence
This is the main verb of the sentence
The main verb is the only verb that is not a child of another verb
'''

def find_root_of_sentence(doc):
    root_token = None
    for token in doc:
        if (token.dep_ == "ROOT"):
            root_token = token
    return root_token

'''
This function returns a list of all the verbs in a sentence
'''
def find_other_verbs(doc, root_token):
    other_verbs = []
    for token in doc: 
        ancestors = list(token.ancestors)
        if (token.pos_ == "VERB" and len(ancestors) == 1\
            and ancestors[0] == root_token):
            other_verbs.append(token)
    return other_verbs

"""
This function returns the token span for a clause given a verb
"""
def get_clause_token_span_for_verb(verb, doc, all_verbs):
    first_token_index = len(doc)
    last_token_index = 0
    this_verb_children = list(verb.children)
    for child in this_verb_children:
        if (child not in all_verbs):
            if (child.i < first_token_index):
                first_token_index = child.i
            if (child.i > last_token_index):
                last_token_index = child.i
    return(first_token_index, last_token_index)

#driver function for splitting into clauses
def get_clauses(text):
    #load spacy model and parse text
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    #find root of sentence, i.e. main verb
    root_token = find_root_of_sentence(doc)
    #find other verbs
    other_verbs = find_other_verbs(doc, root_token)
    token_spans = []   
    #create list of all verbs
    all_verbs = [root_token] + other_verbs
    #find token span for each verb, i.e. clause
    for other_verb in all_verbs:
        (first_token_index, last_token_index) = \
        get_clause_token_span_for_verb(other_verb, 
                                        doc, all_verbs)
        token_spans.append((first_token_index, 
                            last_token_index))
    sentence_clauses = []
    #sort clauses by first token index, i.e. order in sentence
    for token_span in token_spans:
        start = token_span[0]
        end = token_span[1]
        if (start < end):
            clause = doc[start:end]
            sentence_clauses.append(clause)
    sentence_clauses = sorted(sentence_clauses, 
                            key=lambda tup: tup[0])
    #finally, extract text from clauses and return
    clauses_text = [clause.text for clause in sentence_clauses]
    return clauses_text
#end clause splitting code

"""
preprocess text for sentiment analysis
splits the text into "words" which are separated by spaces
annonimizes usernames and links to @user and http to reduce model bias
This step is not necessary, but it helps the model generalize better, especially for short texts
"""

def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)


def get_sentiment(text):
    
    fin_output = text + "\nOverall sentiment + score: "
    if text[-1] not in ['.', '?', '!']:
        text += '.'
    fin_output += sentiment(text)
    tokenized_sent = nltk.sent_tokenize(text)
    if len(tokenized_sent) > 1:
        fin_output += "\nMore than 1 sentence detected! Sentence level sentiments + scores:\n"
        for sent in tokenized_sent:
            fin_output += sent + " - " + sentiment(sent)
            if len(get_clauses(sent)) > 1:
                fin_output += "\nMore than 1 phrase detected! Individual phrase sentiments + scores:\n"
                for word in get_clauses(sent):
                    fin_output += word + " - " + sentiment(word)
            fin_output += "\n"
    else:
        if len(get_clauses(text)) > 1:
            fin_output += "\nMore than 1 phrase detected! Individual phrase sentiments + scores:\n"
            for word in get_clauses(text):
                fin_output += word + " - " + sentiment(word)
        else:
            fin_output += "\nOnly 1 phrase/sentence detected! Phrase sentiment + score:\n"
            fin_output += text + " - " + sentiment(text)
    return fin_output


def sentiment(text):
    #load and setup model
    task='sentiment'
    MODEL = f"cardiffnlp/twitter-roberta-base-{task}"
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    labels = ["negative", "neutral", "positive"]

    #preprocess text and encode it
    text = preprocess(text)
    encoded_input = tokenizer(text, return_tensors='pt')
    #get model output
    output = model(**encoded_input)
    #get sentiment scores
    scores = output[0][0].detach().numpy()
    #softmax scores to get probabilities for each label
    scores = softmax(scores)
    #get ranking of labels based on scores
    ranking = np.argsort(scores)
    #reverse ranking to get highest score first
    ranking = ranking[::-1]
    output = ""
    #get label and score for highest score
    l = labels[ranking[0]]
    s = scores[ranking[0]]
    #format output
    output += (f"{l} {np.round(float(s), 4)}")
    output += "\n"
    #return output
    return output

#testing phrase
if __name__ == "__main__":
    text = "He dislikes cheese and he loves cats. I love veggies but I hate meat. I love you. I hate you."
    print(get_sentiment(text))




