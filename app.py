import streamlit as st
from benchmark.helix_ft import invoke
import traceback
from db.ASMEKnowledgeStore import ASMEKnowledgeStore
from dotenv import load_dotenv
load_dotenv()


def get_response_and_reference(question):
    # Create an instance of ASMEKnowledgeStore or use an existing one if you have it in scope
    knowledge_store = ASMEKnowledgeStore(index_name="asme-bot-knowledge")

    # Use the similarity_search method to get the response and reference
    try:
        search_results = knowledge_store.similarity_search(question)
        context = search_results[0][0]  # This is the page_content of the top document
        print(f"Context results: {search_results}")
        try:
            res = invoke({"question": question, "context": context})
            response = res['choices'][0]['message']['content'].strip()
        except Exception as e:
            print(f"Failed to get model response: {e}. Traceback: {traceback.format_exc()}")
            return None, None
        reference = search_results[0][1]  # This is the metadata of the top document
        return response, reference
    except Exception as e:
        print(f"Failed to get response and reference: {e}. Traceback: {traceback.format_exc()}")
        return "None", "No reference available"


# Setting up the Streamlit UI
st.title("ASME B31.3 Piping Code Assistant")
user_question = st.text_input("Enter your question:", "")
if user_question:
    with st.spinner('Getting response...'):
        response, reference = get_response_and_reference(user_question)
    st.text_area("Response:", value=response, height=300)
    st.text_area("Reference:", value=reference, height=150)