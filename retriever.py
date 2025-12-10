from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import CrossEncoder
from dotenv import load_dotenv
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
import os

# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.runnables import RunnablePassthrough, RunnableLambda
# from langchain_core.output_parsers import StrOutputParser
# from langchain_weaviate import WeaviateVectorStore

import numpy as np

load_dotenv()


persistent_directory="./chroma_db_constitution"
collection_name="nepal_constitution_db"

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

db=Chroma(
    persist_directory=persistent_directory,
    embedding_function=embedding_model,
    collection_name=collection_name
)

dense_retriever=db.as_retriever(search_kwargs={"k":5})




chroma_data=db.get()#everything including ids,embeddings,documents,metadatas
doc_texts=chroma_data["documents"]
doc_metadatas=chroma_data["metadatas"]

docs_with_metadata = []
for text, meta in zip(doc_texts, doc_metadatas):
    # Optional: Simple filter to skip "garbage" chunks like page numbers
    if len(text) > 40:  
        docs_with_metadata.append(Document(page_content=text, metadata=meta))

# Initialize BM25 with full documents, not just text
bm25_retriever = BM25Retriever.from_documents(docs_with_metadata)
bm25_retriever.k = 5


#mannual reciprocal_rank fusion function
def reciprocal_rank_fusion(doc_lists,k=60):
    fused_scores={}
    
    for doc_list in doc_lists:
        for rank,doc in enumerate(doc_list,1):
            source=doc.metadata.get("source_file","unknown") #unknown for fallback
            page=doc.metadata.get("page","0")#0 for fallback
            doc_id=f"{source}_page_{page}"
            
            fused_scores[doc_id]=fused_scores.get(doc_id,0)+1/(k+rank) #.get retrives old score, if exists
    
    sorted_docs=sorted(fused_scores.items(),key=lambda x:x[1],reverse=True)    #.items() converts the dictionary into listo fo key value pairs[(k,v),(k,v)...]   and key to be sorted is  x, where  x is x[1] means the numeric part  of the tuple ("doc1_page_2", 0.03199)
    return sorted_docs

def hybrid_retrieval_chain(query):
    dense_docs=dense_retriever.invoke(query)
    bm25_docs=bm25_retriever.invoke(query)
    
    
    fused_docs=reciprocal_rank_fusion([dense_docs,bm25_docs],k=60)
    
    return fused_docs, dense_docs, bm25_docs


# if __name__=="__main__":
#     query="What are the laws of crime under age 18?"
#     final_docs=hybrid_retrieval_chain(query)
#     for i ,doc in enumerate(final_docs[:5]):
#         print(doc)


if __name__=="__main__":
    query="Laws for  elderly(aged) people. "
    fused_docs, dense_docs, bm25_docs = hybrid_retrieval_chain(query)
    
    # Create a mapping of doc_id to actual document
    doc_mapping = {}
    for doc in dense_docs + bm25_docs:
        source = doc.metadata.get("source_file", "unknown")
        page = doc.metadata.get("page", "0")
        doc_id = f"{source}_page_{page}"
        doc_mapping[doc_id] = doc
    
    # Print top 5 results with actual content
    print("\n=== TOP 5 RESULTS ===\n")
    for i, (doc_id, score) in enumerate(fused_docs[:5], 1):
        doc = doc_mapping.get(doc_id)
        if doc:
            print(f"Result #{i} (Score: {score:.4f})")
            print(f"Source: {doc.metadata.get('source_file')}")
            print(f"Page: {doc.metadata.get('page')}")
            print(f"Content:\n{doc.page_content}")
            print("-" * 80 + "\n")
    
    
