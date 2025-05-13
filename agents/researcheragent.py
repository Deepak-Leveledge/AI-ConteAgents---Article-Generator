from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import Tool
from langchain_community.utilities import SerpAPIWrapper
from serp import get_serp_result
import os



class ResearcherAgent:
    def __init__(self):
        self.llm=ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",google_api_key=os.getenv("GOOGLE_API")
        )
        self.search = SerpAPIWrapper(serpapi_api_key=os.getenv("SERP_API"))


    def _get_web_results(self, query: str) -> str:
        """Get structured web results from SerpAPI"""
        results = self.search.results(query)  # Get all results
        top_5_results = results.get("organic_results", [])[:5]  # Extract top 5 organic results
        return top_5_results


    def research_pipeline(self, topic: str) -> str:

        # Step 1: Get live web data
        web_data = self._get_web_results(topic)
        
        # Step 2: Process with Gemini
        prompt = ChatPromptTemplate.from_template("""
        Analyze this topic using LIVE web results:
        Topic: {topic}
        
        Web Results:
        {web_data}
        
        Generate:
        1. 5 key bullet points (mark with •)
        2. 3 verified sources ([Title](URL))
        3. 2 statistics with sources
        4. 1 counter-argument
        
        Format:
        ### Key Insights
        • Point 1...
        ### Verified Sources
        - [Title](URL)
        ### Statistics
        1. Stat 1 (Source)
        ### Counter-Arguments
        - Argument...
        """)

        chain = prompt | self.llm
        return chain.invoke({
            "topic":topic,
            "web_data":web_data
        }
        ).content
    

def get_researcher_agent():
    return ResearcherAgent()