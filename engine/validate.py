import faiss

index = faiss.read_index("faiss_index/index.faiss")
print("FAISS index dimension:", index.d)
