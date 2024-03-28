import streamlit as st
from benchmark.helix_ft import invoke
from dotenv import load_dotenv

from db.ASMEKnowledgeStore import ASMEKnowledgeStore

load_dotenv()

# def get_response(question):
#     context = ""
#     res = invoke({"question": question, "context": context})
#     try:
#         output = res['choices'][0]['message']['content'].strip()
#         return output
#     except Exception as e:
#         print(f"Failed to get response: {e}")
#         return "None"

# def get_response_and_reference(question):
#     # This is a placeholder for the integration of the similarity search that returns response and metadata
#     # The actual implementation will depend on how the similarity_search method is updated
#     response = "This is the response from the chatbot"
#     reference = "Reference material from ASME B31.3, Section XYZ, Page 123"
#     return response, reference
#     def get_response(question):
#     context = ""
#     res = invoke({"question": question, "context": context})
#     try:
#         output = res['choices'][0]['message']['content'].strip()
#         return output
#     except Exception as e:
#         print(f"Failed to get response: {e}")
#         return "None"

# def get_response_and_reference(question):
#     # This is a placeholder for the integration of the similarity search that returns response and metadata
#     # The actual implementation will depend on how the similarity_search method is updated
#     response = "This is the response from the chatbot"
#     reference = "Reference material from ASME B31.3, Section XYZ, Page 123"
#     return response, reference
#
#     def get_response(question):
#         context = ""
#
#     res = invoke({"question": question, "context": context})
#     try:
#         output = res['choices'][0]['message']['content'].strip()
#         return output
#     except Exception as e:
#         print(f"Failed to get response: {e}")
#         return "None"

def get_response_and_reference(question):
    # Create an instance of ASMEKnowledgeStore or use an existing one if you have it in scope
    knowledge_store = ASMEKnowledgeStore(index_name="asme-bot-knowledge")

    # Use the similarity_search method to get the response and reference
    try:
        search_results = knowledge_store.similarity_search(question)[0][0]
        context = search_results[0][0]  # This is the page_content of the top document
        try:
            res = invoke({"question": question, "context": context})
            response = res['choices'][0]['message']['content'].strip()
        except Exception as e:
            return f"Failed to get model response: {e}"
        reference = search_results[0][1]  # This is the metadata of the top document
        return response, reference
    except Exception as e:
        print(f"Failed to get response and reference: {e}")
        return "None", "No reference available"


# Setting up the Streamlit UI
st.title("ASME B31.3 Piping Code Assistant")

user_question = st.text_input("Enter your question:", "")


if user_question:
    with st.spinner('Getting response...'):
        response, reference = get_response_and_reference(user_question)
    st.text_area("Response:", value=response, height=300)
    st.text_area("Reference:", value=reference, height=150)

    st.write("Rate the response:")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button('⭐', key='1'):
            st.write("You rated this response 1 star")
    with col2:
        if st.button('⭐⭐', key='2'):
            st.write("You rated this response 2 stars")
    with col3:
        if st.button('⭐⭐⭐', key='3'):
            st.write("You rated this response 3 stars")
    with col4:
        if st.button('⭐⭐⭐⭐', key='4'):
            st.write("You rated this response 4 stars")
    with col5:
        if st.button('⭐⭐⭐⭐⭐', key='5'):
            st.write("You rated this response 5 stars")