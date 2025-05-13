from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

import os 


class WriterAgent:
    def __init__(self):
        self.llm=ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=os.getenv("GOOGLE_API")
        )


    def write_draft(self,research:str,tone:str="professional")-> str:
        prompt = ChatPromptTemplate.from_template("""
        Create article draft using this research: {research}
        
        Requirements:
        - 600-800 words
        - {tone} tone
        - Markdown headers
        - Include sources
        
        Output format:
        # [Title]
        
        ## Introduction
        ...
        """)

        chain = prompt | self.llm
        return chain.invoke({
            "research":research,
            "tone":tone
        }).content
    

def get_writer_agent():
    return WriterAgent()