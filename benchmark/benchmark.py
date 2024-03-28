from langchain_mistralai.chat_models import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from db.ASMEKnowledgeStore import ASMEKnowledgeStore
from helix_ft import invoke
from dotenv import load_dotenv

class Benchmark:
    """
    Run Benchmark for the following supported variants:

    1. Mistral 7B OpenOrca Base: base
    2. Mistral 7B OpenOrca Base + RAG: baserag
    3. Mistral 7B OpenOrca Fine-tune: ft
    4. Mistral 7B OpenOrca Fine-tune + RAG: ftrag
    """

    modes = ["base", "baserag", "ft", "ftrag"]

    def __init__(self, mode: str):
        load_dotenv()
        if mode in self.modes:
            self.mode = mode
        else:
            raise Exception(f"Unsupported mode. Should be one of {self.modes}")
        self.chat = ChatMistralAI()
        self.vectordb = ASMEKnowledgeStore("asme-bot-knowledge")

    def run(self, qa_pairs: list):
        if self.mode == "base":
            return self.run_base(qa_pairs)
        elif self.mode == "baserag":
            return self.run_baserag(qa_pairs)
        elif self.mode == "ft":
            return self.run_ft(qa_pairs)
            return self.run_ft()
        elif self.mode == "ftrag":
            return self.run_ftrag(qa_pairs)

    def run_base(self, qa_pairs: list):
        prompt = ChatPromptTemplate.from_template(
            "Answer the question based on your ASME B31.3 piping code knowledge. Question: {question}")
        chain = prompt | self.chat

        outputs = []
        for qa_pair in qa_pairs:
            q, ref_a = qa_pair
            output = chain.invoke({"question": q})
            # print(f"Question: {q} \n Response: {output.content}")
            outputs.append(output.content)

        return outputs

    def run_baserag(self, qa_pairs: list):
        prompt_template = """
            INSTRUCTION: Answer the question based on your
            ASME B31.3 piping code knowledge. Here is context to help:

            {context}

            QUESTION:

            {question}
        """
        prompt = ChatPromptTemplate.from_template(prompt_template)
        chain = prompt | self.chat

        outputs = []
        for qa_pair in qa_pairs:
            q, ref_a = qa_pair
            context = self.vectordb.similarity_search(q)
            output = chain.invoke({"context": context, "question": q})
            outputs.append(output.content)

        return outputs

    def run_ft(self, qa_pairs):
        outputs = []
        for qa_pair in qa_pairs:
            q, ref_a = qa_pair
            res = invoke({"context": "None", "question": q})
            try:
                output = res['choices'][0]['message']['content'].strip()
            except Exception as e:
                output = f"Failed to get response: {e}"
            outputs.append(output)
        return outputs

    def run_ft(self):
        raise NotImplementedError("[ft] mode not implemented")

    def run_ftrag(self, qa_pairs: list):
        outputs = []
        for qa_pair in qa_pairs:
            q, ref_a = qa_pair
            context = self.vectordb.similarity_search(q)
            res = invoke({"context": context, "question": q})
            try:
                output = res['choices'][0]['message']['content'].strip()
            except Exception as e:
                output = f"Failed to get response: {e}"
            outputs.append(output)
        return outputs

    def eval(self, model_output, ref_answer):
        return 0

    def set_mode(self, mode):
        if mode in self.modes:
            self.mode = mode
        else:
            raise Exception(f"Unsupported mode. Should be one of {self.modes}")
