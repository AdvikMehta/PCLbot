import os
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
from benchmark.helix_ft import invoke
from dotenv import load_dotenv
import traceback
from db.ASMEKnowledgeStore import ASMEKnowledgeStore

load_dotenv()

def add_docs(vectordb: ASMEKnowledgeStore, files: list[UploadedFile]):
    paths = []
    for file in files:
        tmp_location = os.path.join('/tmp', file.name)
        with open(tmp_location, 'wb') as f:
            f.write(file.read())
        paths.append(tmp_location)
    vectordb.add_docs(paths)

def get_response_and_reference(vectordb, question):
    # Use the similarity_search method to get the response and reference
    try:
        search_results = vectordb.similarity_search(question)
        context = search_results[0][0]  # This is the page_content of the top document
        print(f"Context results: {search_results}")
        try:
            model_response = invoke({"question": question, "context": context})
            resp = model_response['choices'][0]['message']['content'].strip()
        except Exception as e:
            return f"Failed to get model response: {e}"
        ref = search_results[0][1]  # This is the metadata of the top document
        return resp, ref
    except Exception as e:
        print(f"Failed to get response and reference: {e}. Traceback: {traceback.format_exc()}")
        return "None", "No reference available"

# setting up backend
knowledge_store = ASMEKnowledgeStore(index_name="asme-bot-knowledge")

# setting up the Streamlit UI
st.title("ASME B31.3 Piping Code Assistant")
uploaded_files: list[UploadedFile] = st.file_uploader("Upload PDF documents:", accept_multiple_files=True, type=['pdf'])

if uploaded_files:
    add_docs(knowledge_store, uploaded_files)

user_question = st.text_input("Enter your question:", "")

if user_question:
    with st.spinner('Getting response...'):
        response, reference = get_response_and_reference(knowledge_store, user_question)
    st.text_area("Response:", value=response, height=300)
    st.text_area("Reference:", value=reference, height=150)
