from langchain_community.retrievers import AmazonKnowledgeBasesRetriever

from models.bedrock_client import BedrockClient

class KnowledgeBaseService:
    """Service for knowledge base operations"""
    
    def __init__(self, knowledge_base_id="KS3NLF2KU6"):
        self.knowledge_base_id = knowledge_base_id
        self.bedrock_client = BedrockClient()

    def search(self, prompt):
        retriever = AmazonKnowledgeBasesRetriever(
        knowledge_base_id = self.knowledge_base_id, 
        top_k = 3,
        retrieval_config = {
            "vectorSearchConfiguration": {
                "numberOfResults": 5, 
                'overrideSearchType': "SEMANTIC"
            }
        })
    
        retrieved_docs = retriever.get_relevant_documents(prompt + " 2024")
        context = "\n".join([doc.page_content for doc in retrieved_docs])
        system_prompt = f"""
        Based on the provided context, provide the answer to the question in the input languages:
        <context>{context}</context>
        <question>{prompt} </question>
        """
        print (system_prompt)
        return self.bedrock_client.call_stream(system_prompt)
