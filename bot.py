import re
import pickle
import numpy as np
import pandas as pd

from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('stsb-mpnet-base-v2')

def get_response(req):
    words = []

    # Pre-processing
    req = re.sub(r'[^A-Za-z0-9\\s]', ' ', req.lower())
    
    if req in ["hi", "hello", "hey", "helloo", "hellooo", "g morining", "gmorning", "good morning", "morning", "good day", "good afternoon", "good evening", "greetings", "greeting", "good to see you", "its good seeing you", "how are you", "how're you", "how are you doing", "how ya doin'", "how ya doin", "how is everything", "how is everything going", "how's everything going", "how is you", "how's you", "how are things", "how're things", "how is it going", "how's it going", "how's it goin'", "how's it goin", "how is life been treating you", "how's life been treating you", "how have you been", "how've you been", "what is up", "what's up", "what is cracking", "what's cracking", "what is good", "what's good", "what is happening", "what's happening", "what is new", "what's new", "what is neww", "g’day", "howdy"]:
        return 'Hello, I hope you are fine and safe'

    # Encode the text to get embeddings
    req_embeddings = model.encode(req).reshape(1, -1)

    # Compute similarity
    qn_embeddings = pickle.load(open('stsb-embedding.pkl', 'rb'))
    cosine_sim = cosine_similarity(qn_embeddings, req_embeddings) 
    cosine_sim = [(idx, item) for idx,item in enumerate(cosine_sim)]
    sim_scores = sorted(cosine_sim, key=lambda x: x[1], reverse=True) 
    # Return response of the top most similar question
    top_score = sim_scores[0]
    qn_indice = top_score[0]

    df = pd.read_csv('cleaned_df.csv')

    if top_score[1][0] > .60 or word in df['Answers'].iloc[qn_indice]:
      return df['Answers'].iloc[qn_indice]
    return "Could you please elaborate your situation more? I don't really understand."