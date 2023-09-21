from transformers import AutoTokenizer, AutoModel 
import torch 
import numpy as np

# Initialize the model and tokenizer
# Using paraphrase-MiniLM because it was trained for semantic similarity
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/paraphrase-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/paraphrase-MiniLM-L6-v2")

# Function to generate unique ids
def get_unique_ids(texts):
    return [paper_name for paper_name in texts.keys()]

# Function to generate embeddings
def generate_embeddings(texts):
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt", max_length=128)
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings.detach().cpu().numpy()

# Function to generate embeddings and IDs
def get_embeddings(paper_text_map):
    texts = list(paper_text_map.values())
    embeddings = generate_embeddings(texts)
    return embeddings

# Function to generate a query embedding
def generate_query_embedding(text):
    inputs = tokenizer(text, padding=True, truncation=True, return_tensors="pt", max_length=128)
    outputs = model(**inputs)
    query_embedding = outputs.last_hidden_state.mean(dim=1)
    return query_embedding.detach().cpu().numpy()