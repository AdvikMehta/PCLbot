import os
import traceback
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
from benchmark.helix_ft import invoke
from dotenv import load_dotenv
from db.ASMEKnowledgeStore import ASMEKnowledgeStore
import firebase_admin
from firebase_admin import credentials, firestore

# Check if there's any Firebase app already initialized, if not, initialize one.
if not firebase_admin._apps:
    cred = credentials.Certificate('ASME_key.json')
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ... rest of your Streamlit app code ...


load_dotenv()

def add_docs(vectordb: ASMEKnowledgeStore, files: list[UploadedFile]):
    paths = []
    for file in files:
        tmp_location = os.path.join('/tmp', file.name)
        with open(tmp_location, 'wb') as f:
            f.write(file.read())
        paths.append(tmp_location)
    vectordb.add_docs(paths)

def get_response_and_reference(vectordb: ASMEKnowledgeStore, question):
    try:
        search_results = vectordb.similarity_search(question, k=3)
        context = ""
        for sr in search_results:
            context += sr[0] + "\n"
        # context = search_results[0][0]  # This is the page_content of the top document
        print(context)
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

knowledge_store = ASMEKnowledgeStore(index_name="asme-bot-knowledge")

# Setting up the Streamlit UI
st.title("Piping Code Assistant")

uploaded_files: list[UploadedFile] = st.file_uploader("Upload PDF documents:", accept_multiple_files=True, type=['pdf'])

if uploaded_files:
    add_docs(knowledge_store, uploaded_files)

user_question = st.text_input("Enter your question:", "")

def create_smiley_rating():
    # Emojis for different ratings
    smiley_emojis = ['☹️', '🙁', '😐', '🙂', '😄']
    # Columns for the smiley buttons
    cols = st.columns(5, gap="small")
    # Use a session state to store the rating
    if 'rating' not in st.session_state:
        st.session_state['rating'] = None

    # Create a button in each column
    for idx, col in enumerate(cols):
        with col:
            if st.button(smiley_emojis[idx]):
                selected_index = idx + 1
                # st.session_state["rating"]
                # st.session_state['rating'] = idx + 1  # Store rating from 1 to 5
                # You can display a message or perform an action based on the rating
                print(f'You rated: {selected_index} / 5')

# def collect_feedback():
#     # Feedback text input
#     feedback = st.text_input("Feedback:", placeholder="Your feedback is valuable to us!", key='feedback', max_chars=200)
#     # Submit button
#     if st.button("Submit"):
#         # Here you can perform an action with the feedback
#         st.success("Thank you for your feedback!")
#         # For example, display the feedback and rating (for now, as we're not storing it)
#         st.write("Feedback:", feedback)
#         st.write("Rating:", st.session_state.get('rating', 'No rating given'))

def collect_feedback():
    # Feedback text input
    feedback_text = st.text_input("Feedback:", placeholder="Your feedback is valuable to us!", key='feedback', max_chars=200)
    rating = st.session_state.get('rating', 'No rating given')
    # Submit button
    if st.button("Submit"):
        # Here you can perform an action with the feedback
        feedback_data = {
            "feedback": feedback_text,
            "rating": rating,
            # Include any additional data you might need
        }
        # Write data to Firestore
        db.collection('feedback').add(feedback_data)
        st.success("Thank you for your feedback!")
        # Display the feedback and rating
        st.write("Feedback:", feedback_text)
        st.write("Rating:", rating)

if user_question:
    with st.spinner('Getting response...'):
        response, reference = get_response_and_reference(knowledge_store, user_question)
    st.text_area("Response:", value=response, height=300)
    st.text_area("Reference:", value=reference, height=150)

    create_smiley_rating()
    collect_feedback()