import streamlit as st
from categorize_prompt import ReplicateAPI
from web_scrape_nyt import NYTimesAPI
from get_summary import TextSummarizationPipeline
from chromadb.utils import embedding_functions
import chromadb

def get_linksDB(collection_name, prompt) -> list:
    client = chromadb.PersistentClient(path="D:/Holidays-2/News Lens/DataBase/data")
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="sentence-transformers/sentence-t5-base")
    collection_name = collection_name.capitalize()

    db_collection = client.get_collection(name=f"{collection_name}", embedding_function=sentence_transformer_ef)

    result = db_collection.query(
        query_texts=[prompt],
        n_results=1
    )

    related_links = [metadata['link'] for metadata in result['metadatas'][0]]
    return related_links

def categorize(prompt: str, model: str) -> str:
    api = ReplicateAPI(model_name=model)
    output = api.run_model(prompt)
    categorized_output = output.lower().strip()
    categories = ['technology', 'science', 'health', 'sports']

    return categorized_output if categorized_output in categories else ""

def get_news(url: str) -> list:
    if 'www.nytimes.com' in url:
        scraper = NYTimesAPI()
        news_topic = url.split("/")[-1]
        return scraper.get_response(news_topic)
    return []

def main():
    st.title("News Summarization App")
    
    user_prompt = st.text_input("Enter a keyword to find related news:")

    if user_prompt:
        model_name = 'meta/meta-llama-3-70b-instruct'
        prompt_category = categorize(user_prompt, model_name)
        st.write(f"Your prompt was categorized under: {prompt_category}")

        if not prompt_category:
            st.write("No valid category found. Exiting.")
            return

        links = get_linksDB(prompt_category, user_prompt)
        st.write(f"Links retrieved: {links}")

        summarizer = TextSummarizationPipeline()
        outputs = []

        for link in links:
            info = get_news(link)
            if info:
                summary = summarizer.generate_summary(info)
                outputs.append(summary[0]['summary_text'])
        
        if outputs:
            st.write("Here are AI-generated summaries of some related news articles:")
            for out in outputs:
                st.write(out)
                st.write("-" * 50)
        else:
            st.write("No news content found to summarize.")

if __name__ == "__main__":
    main()














# import sys
# from categorize_prompt import ReplicateAPI
# from web_scrape_nyt import NYTimesAPI
# from get_summary import TextSummarizationPipeline
# from chromadb.utils import embedding_functions
# import chromadb


# def get_linksDB(collection_name, prompt) -> list:
#     """
#     Fetches related news document links from ChromaDB after performing a semantic search.
#     :param collection_name: Name of the related collection
#     :param prompt: User prompt to perform semantic search with chromadb
#     :return: List of related links
#     """
#     client = chromadb.PersistentClient(path="D:/Holidays-2/News Lens/DataBase/data")
    
#     sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="sentence-transformers/sentence-t5-base")
#     collection_name = collection_name.capitalize()

#     # Get the collection for the specified news category
#     db_collection = client.get_collection(name=f"{collection_name}", embedding_function=sentence_transformer_ef)

#     # Perform a semantic search
#     result = db_collection.query(
#         query_texts=[prompt],
#         n_results=1
#     )

#     # Extract related links
#     related_links = []
#     for i in result['metadatas'][0]:
#         related_links.append(i['link'])

#     return related_links


# def categorize(prompt: str, model: str) -> str:
#     """
#     Categorizes the user prompt using the specified LLM from ReplicateAI API.
#     :param model: Name of the LLM model to use
#     :param prompt: User's input prompt
#     :return: The relevant category (e.g., technology, science, health, sports)
#     """
#     api = ReplicateAPI(model_name=model)
#     output = api.run_model(prompt)
    
#     # Ensure that the output is processed as a string, not a list
#     categorized_output = output.lower().strip()  # Directly process the output as a string

#     # Define categories
#     categories = ['technology', 'science', 'health', 'sports']

#     # Check if the categorized output is one of the valid categories
#     if categorized_output in categories:
#         return categorized_output
#     else:
#         return ""



# def get_news(url: str) -> list:
#     """
#     Fetches news data from the provided URL.
#     :param url: URL of the news article
#     :return: News content
#     """
#     if 'www.nytimes.com' in url:
#         scraper = NYTimesAPI()
#         # Extract news topic from the URL or prompt (depending on implementation)
#         news_topic = url.split("/")[-1]  # You may extract it differently if your logic differs
#         news = scraper.get_response(news_topic)
#         return news

#     # Uncomment for additional scraping functionality
#     # else:
#     #     scraper = WebScraper(url)
#     #     par = scraper.fetch_and_extract_p()
#     #     return par


# if __name__ == '__main__':
#     # Get user input prompt
#     user_prompt = input("Please enter keywords to find related news: ")

#     # Categorize the prompt using an LLM model
#     model_name = 'meta/meta-llama-3-70b-instruct'
#     prompt_category = categorize(user_prompt, model_name)
#     print(f"Your prompt was categorized under: {prompt_category}")

#     # Handle case where no category is found
#     if not prompt_category:
#         print("Exiting program because no valid category was found for the prompt.")
#         sys.exit()

#     # Fetch relevant links from ChromaDB based on the category
#     outputs = []
#     links = get_linksDB(prompt_category, user_prompt)
#     print(f"Links retrieved: {links}")  # Debugging line

#     # Summarize the Text
#     summarizer = TextSummarizationPipeline()
#     for link in links:
#         # Fetch the news content
#         info = get_news(link)
#         print(f"News content from {link}: {info}")  # Debugging line

#         # Generate summary
#         outputs.append(summarizer.generate_summary(info))
#         print(f"Summary generated for {link}: {outputs[-1]}")  # Debugging line


#     # Print the outputs (summaries)
#     print("\nHere are AI-generated summaries of some related news articles:")
#     for out in outputs:
#         print(out[0]['summary_text'])
#         print("-----------------------")
