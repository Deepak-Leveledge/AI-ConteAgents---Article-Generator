from langchain_community.utilities import SerpAPIWrapper

def get_serp_result(query:str,num_results:int=5)->str:
    search = SerpAPIWrapper()
    results= search.results(query,num_results)



    processed= []


    for result in results.get("organic_results",[])[:num_results]:
        processed.append(f"Title: {result['title']}\n"
                         f"Description: {result['snippet']}\n"
                         f"URL: {result['link']}\n"
                         f"Snippet: {result['snippet']}\n" 
        )

    return "\n".join(processed)