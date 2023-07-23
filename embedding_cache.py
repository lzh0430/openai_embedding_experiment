from utils import get_env
import pandas as pd
import pickle
from openai.embeddings_utils import (get_embedding, cosine_similarity)

embedding_cache_path = get_env("EMBEDDING_PICKLE_PATH")
embedding_model = get_env("EMBEDDING_MODEL")

# load the cache if it exists, and save a copy to disk
try:
    embedding_cache = pd.read_pickle(embedding_cache_path)
except FileNotFoundError:
    embedding_cache = {}

with open(embedding_cache_path, "wb") as embedding_cache_file:
    pickle.dump(embedding_cache, embedding_cache_file)

# Define a function to retrieve embeddings from the cache if present, and otherwise request via the API
# The cache is {(text, modelName) -> embedding, ...}
# The cache is saved as a python pickle file
def get_embedding_of(text):
    if (text, embedding_model) not in embedding_cache.keys():
        
        print(f"New embedding")
        # Cache miss, call api to:
        # 1) Add `text` to openAI embedding 
        # 2) Save the embedding vector to the cache
        embedding_cache[(text, embedding_model)] = get_embedding(text, embedding_model)
        with open(embedding_cache_path, "wb") as embedding_cache_file:
            pickle.dump(embedding_cache, embedding_cache_file)
    
    # o/w Cache hit
    return embedding_cache[(text, embedding_model)]

# Find the most related 5 articles of given keywords.
# Return the Pandas DataFrame with the most related 5 rows
def search_insights(articles_df, keywords, n=5, pprint=True):
    # Get the embedding vectors of the "search keywords"
    embedding = get_embedding_of(keywords)
    # Use OpenAPI `cosine_similarity` api to evaluate the similarity btw the "search keywords embedding" and "article embeddings"
    # Such quantified similarity will be added to the input `articles_df`
    articles_df['similarities'] = articles_df.article_embedding.apply(lambda x: cosine_similarity(x, embedding))
    res = articles_df.sort_values('similarities', ascending=False).head(n)
    return res