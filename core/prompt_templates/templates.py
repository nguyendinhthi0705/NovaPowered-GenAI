class PromptTemplates:
    """Manages prompt templates"""
    
    def __init__(self):
        self.templates = {
            "chat": """You are chatter. You need to anwser the question: 
            \n\nHuman: here is the content
            <text>{content}</text>
            \n\nAssistant: """,

            "rewrite": """Your name is good writer. You need to rewrite content use stronger words to hight: 
            \n\nHuman: here is the content
            <text>{content}</text>
            \n\nAssistant: """,
            
            "summary": """Based on the provided context, create summary the lecture
            \n\nHuman: here is the content
            <text>{content}</text>
            \n\nAssistant: """,
            
            "star_report": """Your name is good writer. You need to rewrite content use stronger words to and format in STAR format: 
            \n\Content:
            <text>{content}</text>""",
            
            "improve_writing": """Your name is good writer. You need to suggest and correct mistake in the essay: 
            \n\nHuman: here is the content
            <text>{content}</text>
            \n\nAssistant: """,
            
            "query_document": """Human: here is the content:
            <text>{content}</text>
            Question: {question} 
            \n\nAssistant: """
        }
    
    def get_template(self, template_name: str) -> str:
        """Get template by name"""
        return self.templates.get(template_name, "")
        
    def add_template(self, name: str, template: str) -> None:
        """Add new template"""
        self.templates[name] = template