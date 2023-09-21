import pinecone
import os
from dotenv import load_dotenv
import streamlit as st
from generate_embeddings import get_embeddings, get_unique_ids, generate_query_embedding
from text_extract import get_all_text

load_dotenv()

api_key = os.getenv('PINECONE_API_KEY')

pinecone.init(api_key=api_key, environment="gcp-starter")

def create_index():
    if not pinecone.list_indexes():
        pinecone.create_index(name='research-papers', dimension=384, metric="euclidean")

def upsert_embeddings():
    # get all the text from the pdfs, stored as KV pair:
    # ex. {'paper1': 'lorum ipsum...'}
    paper_text_map = get_all_text()

    # generate embeddings using all the research paper text in the map
    embeddings = get_embeddings(paper_text_map)

    # generate unique ids for each paper – currently just the name of the paper itself
    # should maybe make this a uuid in the future
    unique_ids = get_unique_ids(paper_text_map)

    # creates formatted list to upsert into Pinecone for each research paper id, embedding pair 
    # ex. ['paper1', [0.87, -0.331, ...] ]
    formatted_data = [(unique_ids[i], embeddings[i].tolist()) for i in range(len(unique_ids))]

    # adds the vectors into Pinecone
    index.upsert(formatted_data)

def filtered_results(query_result):
    # # will need to add filter by sensitivity score here 
    # extract the 'matches' list from the query_result
    matches = query_result['matches']

    # sort the matches by the 'score' field in descending order
    sorted_matches = sorted(matches, key=lambda x: x['score'], reverse=True)

    # extract the 'id' field for each sorted match
    sorted_ids = [match['id'] for match in sorted_matches]

    # return the sorted IDs
    return sorted_ids

@st.cache_data
def query_db(prompt, num_results):
    # generates a query embedding for a sample text
    query_text = prompt
    query_embedding = generate_query_embedding(query_text)

    # flattens the numpy array to a list
    query_embedding_list = query_embedding.flatten().tolist()

    # query the Pinecone index with embedded query, returns top 3 values
    query_result = index.query(
        vector=query_embedding_list,
        top_k=num_results,
        include_values=True
    )

    results = filtered_results(query_result)
    return results




# initialize index (if it doesn't already exist)
create_index()

# get instance for Pinecone index
index = pinecone.Index("research-papers")

vector_count = index.describe_index_stats().total_vector_count

# only add embeddings to the DB if we haven't already added them
# definitely a better way to do this in the future – don't want repeats for right now
if vector_count == 0:
    upsert_embeddings()


# parsing the query into id, scores, and values 
# id: vector's unique id 
# score: measure of similarity: higher = more similar 
# values: list of vectors
# ids = [match['id'] for match in query_result['matches']]
# scores = [match['score'] for match in query_result['matches']]
# values = [match['values'] for match in query_result['matches']]

