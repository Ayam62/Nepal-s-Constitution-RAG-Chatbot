from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path

def process_all_pdfs(pdf_directory):
    all_documents=[]
    pdf_dir=Path(pdf_directory)# Now we can apply Path functions
    pdf_files=list(pdf_dir.glob("**/*.pdf"))# lists total pdf files in the directory
    
    for pdf_file in pdf_files:
        try:
            #print(type(pdf_file))# pdf_file's type is of pathlib.PosixPath class so it needs to be converted to string for further processing
           loader=PyPDFLoader(str(pdf_file))
           documents=loader.load()
        #    print(documents[2].page_content)
           for doc in documents:
               doc.metadata["source_file"]=pdf_file.name
               doc.metadata["file_type"]="pdf"
           
           all_documents.extend(documents)
            
        except Exception as e:
            print(e)
    
    return all_documents
    
process_all_pdfs("/Users/ayamkattel/Desktop/RAG/Nepal's Constitution RAG/Constitution_Document")