from langchain_mistralai.chat_models import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from db.ASMEKnowledgeStore import ASMEKnowledgeStore
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
            return self.run_ft()
        elif self.mode == "ftrag":
            return self.run_ftrag()

    def run_base(self, qa_pairs: list):
        prompt = ChatPromptTemplate.from_template(
            "Answer the question based on your ASME B31.3 piping code knowledge. Question: {question}")
        chain = prompt | self.chat

        eval_outputs = []
        for qa_pair in qa_pairs:
            q, ref_a = qa_pair
            output = chain.invoke({"question": q})
            eval_outputs.append(self.eval(output.content, ref_a))

        return eval_outputs

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

        eval_outputs = []
        for qa_pair in qa_pairs:
            q, ref_a = qa_pair
            context = self.vectordb.similarity_search(q)
            output = chain.invoke({"context": context, "question": q})
            eval_outputs.append(self.eval(output.content, ref_a))

        return eval_outputs

    def run_ft(self):
        raise NotImplementedError("[ft] mode not implemented")

    def run_ftrag(self):
        raise NotImplementedError("[ftrag] mode not implemented")

    def eval(self, model_output, ref_answer):
        return 0