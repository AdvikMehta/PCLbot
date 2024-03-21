import streamlit as st
from benchmark.helix_ft import invoke
from dotenv import load_dotenv

load_dotenv()

def get_response(question):
    context = ""
    res = invoke({"question": question, "context": context})
    try:
        output = res['choices'][0]['message']['content'].strip()
        return output
    except Exception as e:
        print(f"Failed to get response: {e}")
        return "None"


# Setting up the Streamlit UI
st.title("ASME B31.3 Piping Code Assistant")

user_question = st.text_input("Enter your question:", "")

if user_question:
    with st.spinner('Getting response...'):
        response = get_response(user_question)
    st.text_area("Response:", value=response, height=300)
