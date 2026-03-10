import time
import re
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Load the embedding model
print("Loading embedding model...")
embeddings = HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-base"
)

# Check the embedding dimension
test_vec = embeddings.embed_query("test")
print("Embedding dimension:", len(test_vec))

# Load the FAISS index
print("Loading FAISS index...")
db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

print(f"Total vectors in index: {db.index.ntotal}")

# Test with a Sanskrit query
query = "query: मूर्खभृत्यस्य कथा का"
print(f"\nRunning retrieval test: {query}")

# Measure how fast retrieval is
start_time = time.time()
docs_and_scores = db.similarity_search_with_score(query, k=2)
end_time = time.time()

print(f"\nRetrieval took {end_time - start_time:.4f} seconds")

# Display the results
for i, (doc, score) in enumerate(docs_and_scores):
    print(f"\nResult {i+1}  |  Score: {score:.4f}")
    
    # Clean up the text for better readability
    cleaned_text = re.sub(r'\n\s*\n+', '\n\n', doc.page_content).strip()
    
    print(cleaned_text[:600])
