from openai import Embedding
from sklearn.metrics.pairwise import cosine_similarity
MODEL = 'text-embedding-ada-002'

def embedding(text: str):
    return Embedding.create(model=MODEL, input=text).data[0].embedding

def min_max_normalization(value, min_value, max_value):
    return (value - min_value) / (max_value - min_value)
    
def calculate_cosine_similarity(vector1, vector2):
    """
    Compute the cosine similarity between two vectors.
    Parameters:
        vector1, vector2: numpy arrays
    Returns:
        Cosine similarity score between vector1 and vector2
    """
    vector1 = vector1.reshape(1, -1)  # reshaping the vectors to 2D arrays for the function
    vector2 = vector2.reshape(1, -1)
    return cosine_similarity(vector1, vector2)[0][0]