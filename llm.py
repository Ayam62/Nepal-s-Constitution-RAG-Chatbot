from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEndpoint 
from retriever import hybrid_retrieval_chain
from dotenv import load_dotenv
import json
from datetime  import datetime
import time

load_dotenv()
class LegalChatbot:
    def __init__(self,history_file="chat_history.json"):
        self.llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")
        self.history_file=history_file
        self.conversation_history=[]
        self.load_history()
    
    def load_history(self):
        try:
            with open(self.history_file,"r") as f:
                self.conversation_history=json.load(f)
        
        except FileNotFoundError:
            self.conversation_history=[]
            
    def save_history(self):
        with open(self.history_file,"w") as f:
            json.dump(self.conversation_history,f,indent=2)
    
    def contextualize_query(self,query):
        if not self.conversation_history:
            return query
        
        else:
            history_text=""
            for item in self.conversation_history[-3:]:
                history_text+=f"User:{item["query"]} \n Assistant:{item["answer"]}"
        prompt=f"""
        Given the following conversation history and a follow-up question, rephrase the follow-up question to be a standalone question that captures the full context.
        Chat History:
        {history_text}
        Follow-up input:{query}
        
        Standalone Question:
        """
        response=self.llm.invoke(prompt)
        return response.content
    
    def answer_query(self,query):
        standalone_query=self.contextualize_query(query)
        print(f"DEBUG: Rewritten Query: {standalone_query}")
        
        fused_docs, dense_docs, bm25_docs=hybrid_retrieval_chain(standalone_query )
        if not fused_docs:
            response_text="No relevent documents found to answer your query"
            
        else:
            
            doc_mapping = {}
            for doc in dense_docs + bm25_docs:
                source = doc.metadata.get("source_file", "unknown")
                page = doc.metadata.get("page", "0")
                doc_id = f"{source}_page_{page}"
                doc_mapping[doc_id] = doc
            
            context_docs = []
            for doc_id, score in fused_docs[:5]:  # Get top 5 documents
                doc = doc_mapping.get(doc_id)
                if doc:
                    context_docs.append(doc.page_content)
            context="\n\n".join(context_docs)
            
            history_text=""
            if self.conversation_history:
                history_text="Previous Conversation:\n"
                for item in self.conversation_history[-5:]:
                    history_text+=f"User:{item["query"]}\n Assistant:{item["answer"]}\n"
            
            prompt=f"""You are a contitutional expert of nepal. Anser the following question based of the provided context and conversation history. If you are not sure about the answer, directly say you don't know , don't try to anser it if you don't know.\n
            {history_text}
            Context from legal documents:
            {context}
            \n
            Question:{query}
            Answer:
            """
            
            response=self.llm.invoke(prompt)
            response_text=response.content
            
            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "query": query,
                 "answer": response_text
            })
            
            self.save_history()
            
            return response_text
    
    def get_history(self):
        return self.conversation_history
    
    def clear_history(self):
        self.conversation_history = []
        self.save_history()
        
def chat():
    chatbot = LegalChatbot()
    
    print("Type 'quit' to exit, 'history' to see chat history, 'clear' to clear history")
    print("=" * 50)
    
    while True:
        query = input("\nYou: ").strip()
        
        if query.lower() == 'quit':
            print("Goodbye!")
            break
        
        elif query.lower() == 'history':
            if chatbot.get_history():
                print("\n--- Chat History ---")
                for i, item in enumerate(chatbot.get_history(), 1):
                    print(f"\n[{i}] {item['timestamp']}")
                    print(f"Q: {item['query']}")
                    print(f"A: {item['answer'][:200]}...")
            else:
                print("No chat history yet.")
            continue
        elif query.lower() == 'clear':
            chatbot.clear_history()
            print("Chat history cleared.")
            continue
        elif not query:
            continue
        
        print("\nAssistant: ", end="", flush=True)
        answer = chatbot.answer_query(query)
        print(answer)

if __name__ == "__main__":
    chat()
        
            


