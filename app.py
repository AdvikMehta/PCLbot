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

# Check if there's any Firebase app already initialized, if not, initialize one.
if not firebase_admin._apps:
    cred = credentials.Certificate('ASME_key.json')
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Define a function to reset the feedback form state
def reset_feedback_form_state():
    st.session_state['feedback_text'] = ""
    st.session_state['rating'] = None
    st.session_state['feedback_submitted'] = False

# Initialize the session state variables
if 'feedback_text' not in st.session_state:
    st.session_state['feedback_text'] = ""
if 'rating' not in st.session_state:
    st.session_state['rating'] = None
if 'feedback_submitted' not in st.session_state:
    st.session_state['feedback_submitted'] = False

# ... your existing code ...

def create_feedback_form():
    with st.form(key='feedback_form'):
        st.markdown("### Your feedback:")
        st.markdown("<span style='color:grey;'>(Please drag the red dot towards right to adjust the rating)</span>",unsafe_allow_html=True)

        # Use a select slider for the smiley ratings
        smiley_ratings = {
            'Very Unsatisfied ☹️': 1,
            'Unsatisfied 🙁': 2,
            'Neutral 😐': 3,
            'Satisfied 🙂': 4,
            'Very Satisfied 😄': 5
        }
        # Display the slider only if feedback is not submitted
        if not st.session_state['feedback_submitted']:
            rating = st.select_slider("Rating:", options=list(smiley_ratings.keys()), format_func=lambda x: x)
            st.session_state['rating'] = smiley_ratings[rating]

            # Text input for additional feedback
            feedback_text = st.text_area("Feedback:", placeholder="Your feedback is valuable to us!",
                                         value=st.session_state['feedback_text'], max_chars=200)
        else:
            rating = st.empty()
            feedback_text = st.empty()

        # Submit button for the form
        submitted = st.form_submit_button("Submit Feedback")
        if submitted and not st.session_state['feedback_submitted']:
            feedback_data = {
                "feedback": feedback_text,
                "rating": st.session_state['rating'],
            }
            # Write data to Firestore
            db.collection('feedback').add(feedback_data)
            st.success("Thank you for your feedback!")
            st.write("Your Feedback:", feedback_text)
            st.write("Your Rating:", st.session_state['rating'])
            # Mark feedback as submitted
            st.session_state['feedback_submitted'] = True
            # Clearing the input fields
            reset_feedback_form_state()

# ... rest of your code ...

if user_question:
    if not st.session_state['feedback_submitted']:
        with st.spinner('Getting response...'):
            response, reference = get_response_and_reference(knowledge_store, user_question)
        st.text_area("Response:", value=response, height=300)
        st.text_area("Reference:", value=reference, height=150)
    create_feedback_form()
