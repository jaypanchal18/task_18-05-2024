import streamlit as st
import spacy

# Load English tokenizer, tagger, parser, NER, and word vectors
nlp = spacy.load("en_core_web_sm")

# Mock data for testing
mock_data = [
    {
        "Response": "Yes, we offer online delivery services through major platforms like Swiggy and Zomato. You can also reserve a table directly from our website if you are planning to have breakfast!",
        "Source": [
            {
                "id": "71",
                "context": "major platforms like Swiggy and Zomato",
                "link": "https://orders.brikoven.com"
            },
            {
                "id": "75",
                "context": "online delivery services",
                "link": ""
            },
            {
                "id": "8",
                "context": "reserve a table directly from our website",
                "link": "https://www.brikoven.com/reservations"
            },
            {
                "id":"159",
                "context":"Do you give franchise if the brand No, we currently don't offer franchise opportunities for BrikOven! Although do feel free to drop in an email at theteam@brikoven. com so we can get in touch with you at a later stage if we do decide to give out franchisees.",
                "link":""

            }
            
        ]
    }
]


def fetch_data_from_api(url):
    return mock_data

def identify_citations(data):
    citations = []
    for item in data:
        response_text = item['Response']
        sources = item['Source']
        
        # Process response text with spaCy
        response_doc = nlp(response_text)
        
        for source in sources:
            # Process source context with spaCy
            source_doc = nlp(source['context'])
            # Check if source context is in the response text
            if source_doc.text.lower() in response_doc.text.lower():
                citations.append({
                    'id': source['id'],
                    'link': source.get('link', '')
                })
                break
    return citations

def main():
    st.title("Response Citations")
    
    data = fetch_data_from_api("mock_api_url")
    if data:
        citations = identify_citations(data)
        st.subheader("Citations:")
        if citations:
            for citation in citations:
                st.write(f"Source ID: {citation['id']}")
                if citation['link']:
                    st.write(f"Link: {citation['link']}")
                st.write("---")
        else:
            st.write("No citations found.")

if __name__ == "__main__":
    main()
