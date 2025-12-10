from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentSplitter:
    
    def __init__(self, chunk_size=1000, chunk_overlap=200):
      
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = [
            # 1. Major Divisions (English/Nepali) - case variations
            r"[Pp][Aa][Rr][Tt][- ]\d+",     # Matches "Part-1", "Part 1", "part-1"
            r"भाग[- ]\d+",                   # Matches "भाग-१" (Nepali Part)
            r"[Ss][Cc][Hh][Ee][Dd][Uu][Ll][Ee][- ]\d+",  # Matches "Schedule-1", "schedule-1"
            r"अनुसूची[- ]\d+",               # Matches "अनुसूची-१" (Nepali Schedule)

            # 2. Articles (The most important semantic unit)
            r"[Aa][Rr][Tt][Ii][Cc][Ll][Ee] \d+",  # Matches "Article 1", "article 1"
            r"धारा \d+",                     # Matches "धारा १" (Nepali Article)
            r"\n\d+\.\s",                    # Matches "1. ", "26. "

            # 3. Standard Text Boundaries (non-regex)
            "\n\n",
            "\n",
            " ",
            ""
         ]
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=self.separators,
            is_separator_regex=True,
            keep_separator=True
        )
    
    def split_documents(self, documents):
        split_docs = self.text_splitter.split_documents(documents)
        metadatas = [doc.metadata for doc in split_docs]
        return split_docs, metadatas