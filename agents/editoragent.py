from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os 


class EditorAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash",google_api_key=os.getenv("GOOGLE_API"))
        
    def edit_content(self, draft: str) -> str:
        prompt = ChatPromptTemplate.from_template("""
        Improve this draft: {draft}
        
        Edits should:
        1. Fix grammar/spelling
        2. Improve flow
        3. Verify facts
        4. Add transition phrases
        
        Output format:
        ## Edited Version
        ...
        
        ## Changes Made
        - ...
        """)
        
        chain = prompt | self.llm
        return chain.invoke({"draft": draft}).content

def get_editor_agent():
    return EditorAgent()