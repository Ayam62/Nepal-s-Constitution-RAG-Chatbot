from document_loader import process_all_pdfs
from document_splitter import DocumentSplitter
from langchain_core.documents import Document
from generate_embedding_and_store import EmbeddingManager,put_in_vector_store




# def log_chunks_to_file(splitted_docs, output_file="chunks_log.txt"):
#     """Log all chunks' content to a file"""
#     with open(output_file, "w", encoding="utf-8") as f:
#         for idx, doc in enumerate(splitted_docs, 1):
#             f.write(f"{'='*80}\n")
#             f.write(f"CHUNK #{idx}\n")
#             f.write(f"{'='*80}\n")
#             f.write(f"Source: {doc.metadata.get('source_file', 'Unknown')}\n")
#             f.write(f"Page: {doc.metadata.get('page', 'Unknown')}\n")
#             f.write(f"\n{doc.page_content}\n\n")
#     print(f"Logged {len(splitted_docs)} chunks to {output_file}")


def main():
    
    all_documents=process_all_pdfs("/Users/ayamkattel/Desktop/RAG/Nepal's Constitution RAG/Constitution_Document")
    # print(len(all_documents))
    splitter=DocumentSplitter()
 
    splitted_doc,metadatas=splitter.split_documents(all_documents)
    # texts=[chunk.page_content for chunk in  splitted_doc]
    vector_db=put_in_vector_store(splitted_doc)
    print("Ingestion Completed!")
    

    
if __name__== "__main__":
    main()
    
