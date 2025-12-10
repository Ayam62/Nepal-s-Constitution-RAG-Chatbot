from sentence_transformers import SentenceTransformer
import numpy as np
from langchain_community.vectorstores import Chroma

VECTOR_DB_PATH = "./chroma_db_constitution"
COLLECTION_NAME = "nepal_constitution_db"

class EmbeddingManager:
    def __init__(self,model_name="sentence-transformers/all-mpnet-base-v2"):
        self.model=SentenceTransformer(model_name)
        
    def embed_documents(self,texts):
        all_embeddings=[]
        
        for i,text in enumerate(texts):
            embedding=self.model.encode(text,convert_to_numpy=True)
            all_embeddings.append(embedding)
            
        embedding_array=np.array(all_embeddings)
        return embedding_array.tolist()
        



def put_in_vector_store(chunks=None):
    
    if chunks:
        embedding_func=EmbeddingManager()
        vector_store=Chroma.from_documents(
            documents=chunks,
            embedding=embedding_func,
            collection_name=COLLECTION_NAME,
            persist_directory=VECTOR_DB_PATH
        )
    return vector_store


        
    
    
