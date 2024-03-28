import streamlit as st
from benchmark.helix_ft import invoke
from dotenv import load_dotenv
import traceback
from db.ASMEKnowledgeStore import ASMEKnowledgeStore

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
            return f"Failed to get model response: {e}"
        reference = search_results[0][1]  # This is the metadata of the top document
        return response, reference
    except Exception as e:
        print(f"Failed to get response and reference: {e}. Traceback: {traceback.format_exc()}")
        return "None", "No reference available"


# Setting up the Streamlit UI
st.title("ASME B31.3 Piping Code Assistant")

user_question = st.text_input("Enter your question:", "")

<<<<<<< HEAD
=======
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
                st.session_state['rating'] = idx + 1  # Store rating from 1 to 5
                # You can display a message or perform an action based on the rating
                st.info(f'You rated: {st.session_state["rating"]}', key=f'info_{idx}')

def collect_feedback():
    # Feedback text input
    feedback = st.text_input("Feedback:", placeholder="Your feedback is valuable to us!", key='feedback', max_chars=200)
    # Submit button
    if st.button("Submit"):
        # Here you can perform an action with the feedback
        st.success("Thank you for your feedback!")
        # For example, display the feedback and rating (for now, as we're not storing it)
        st.write("Feedback:", feedback)
        st.write("Rating:", st.session_state.get('rating', 'No rating given'))

>>>>>>> 1ac4411 (Improving feedback, added input column)
if user_question:
    with st.spinner('Getting response...'):
        response, reference = get_response_and_reference(user_question)
    st.text_area("Response:", value=response, height=300)
    st.text_area("Reference:", value=reference, height=150)

<<<<<<< HEAD

=======
    create_smiley_rating()
    collect_feedback()
>>>>>>> 1ac4411 (Improving feedback, added input column)
