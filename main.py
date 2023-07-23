from utils import (get_env)
from embedding_cache import (search_insights, get_embedding_of)
import json
import pandas as pd

# Load the embedding model
embedding_model = get_env("EMBEDDING_MODEL")
# Load the encoder used when uploading data
encoding_name = get_env("EMBEDDING_ENCODING")
# Load the location of articles
article_json_path = get_env("ARTICLE_JSON_PATH")

# Read articles from `data/reports.insight.json` as DataFrame
# Return the DataFrame
def load_articles():
    with open(article_json_path, "r") as json_file:
        # str
        json_data = json_file.read()

    # json obj
    articles_data = json.loads(json_data)
    # Create lists to store titles and embeddings
    titles = []
    embeddings = []

    # Get embeddings for each article and store titles and embeddings
    for article in articles_data:
        title = article['title']
        # Load from cache or call api
        embedding = get_embedding_of(article['insights'])
        # Populate 2 Pandas DF columns
        titles.append(title)
        embeddings.append(embedding)

    # Create a DataFrame with titles and embeddings
    # Such structure is convinient for similarity calculation soon after.
    df_articles = pd.DataFrame({'article_title': titles, 'article_embedding': embeddings})
    return df_articles

if __name__ == "__main__":
    # Load report insights from the JSON file
    # All articles are embedded and cached upon the completion of this call.
    articles_pd = load_articles()
    
    # Let users the keywords
    user_input = input("Enter a keyword to find related articles: ")

    # Find the most related 5 articles with the input search keywords
    most_related_articles_df = search_insights(articles_pd, user_input, n=1)

    print(most_related_articles_df)