from langchain_mistralai.chat_models import ChatMistralAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from db.ASMEKnowledgeStore import ASMEKnowledgeStore
from langchain_core.messages.ai import AIMessage

load_dotenv()

chat = ChatMistralAI()
vectordb = ASMEKnowledgeStore("asme-bot-knowledge")

question = "According to ASME B31.3, what is the minimum design metal temperature (in °F) for carbon steel without impact testing?"
# messages = [HumanMessage(content="knock knock")]
# print(chat.invoke(messages))
context = vectordb.similarity_search(question)
print(f"Context: {context}")

prompt_template = """
INSTRUCTION: Answer the question based on your
ASME B31.3 piping code knowledge. Here is context to help:

{context}

QUESTION:

{question}
"""

prompt = ChatPromptTemplate.from_template(prompt_template)
chain = prompt | chat

output = chain.invoke({"context": context, "question": question})
print(f"Reponse: {output}")
print(output.content)