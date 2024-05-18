import requests
import nltk
import streamlit as st
from nltk.tokenize import word_tokenize

# Download NLTK data for tokenization
nltk.download('punkt')

def fetch_data(api_url):
    """
    Fetch data from the paginated API.

    Args:
        api_url (str): The URL of the API endpoint.

    Returns:
        list: A list of data objects fetched from the API.
    """
    data = []
    page = 1
    while True:
        response = requests.get(f"{api_url}?page={page}")
        if response.status_code != 200:
            st.error("Failed to fetch data from API.")
            break
        response_json = response.json()
        if 'data' in response_json:
            page_data = response_json['data']
        else:
            break
        if not page_data:
            break
        data.extend(page_data)
        page += 1
    return data

def match_response_with_sources(response, sources):
    """
    Match the response text with the sources and identify citations.

    Args:
        response (str): The response text.
        sources (list): A list of source objects.

    Returns:
        list: A list of citations where each citation contains an id and an optional link.
    """
    citations = []
    response_tokens = set(word_tokenize(response.lower()))
    for source in sources:
        context_tokens = set(word_tokenize(source['context'].lower()))
        if response_tokens & context_tokens:
            citations.append({"id": source['id'], "link": source.get('link', '')})
    return citations

def process_data(data):
    """
    Process the fetched data to find citations for each response.

    Args:
        data (list): A list of data objects each containing a response and sources.

    Returns:
        list: A list of processed data with responses and their corresponding citations.
    """
    result = []
    for item in data:
        if 'response' not in item or 'sources' not in item:
            st.error(f"Missing 'response' or 'sources' in item: {item}")
            continue
        response = item['response']
        sources = item['sources']
        citations = match_response_with_sources(response, sources)
        result.append({"response": response, "citations": citations})
    return result

def main():
    """
    Main function to run the Streamlit app.
    """
    st.title("Response and Citation Matcher")
    api_url = "https://devapi.beyondchats.com/api/get_message_with_sources"
    
    if st.button("Fetch and Process Data"):
        st.write("Fetching data from API...")
        data = fetch_data(api_url)
        st.write("Processing data...")
        processed_data = process_data(data)
        st.write("Data processed successfully!")
        
        for item in processed_data:
            st.subheader("Response")
            st.write(item['response'])
            st.subheader("Citations")
            if item['citations']:
                for citation in item['citations']:
                    st.write(f"ID: {citation['id']}, Link: {citation['link']}")
            else:
                st.write("No citations found")

if __name__ == '__main__':
    main()
