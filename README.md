# 🏗️ InnovAiTors: AI-Powered Assistant for Engineers in the AEC Industry

## 📘 Overview
InnovAiTors is a domain-specific AI solution built to streamline how engineers in the Architecture, Engineering, and Construction (AEC) industry access and interact with technical documentation. Focused on standards like **ASME B31.3**, this digital assistant answers complex engineering queries with precise, referenced, and well-structured responses.

---

## ❓ Problem Statement
Engineers often spend excessive time sifting through bulky binders and PDFs to locate relevant clauses in technical standards. This:
- Delays decision-making on site
- Increases risk of human error
- Impacts efficiency and safety

---

## 💡 Our Solution
A 24/7 intelligent assistant that enables:
- 📥 Natural language input from engineers
- 📌 Accurate, summarized responses
- 🔗 Direct references to standard clauses
- ⚡ Rapid access to critical information

---

## 🧪 Technical Approach

### 🔹 Base Model
- **Mistral-7B OpenOrca** — a powerful open-source LLM chosen for its strong performance on QA and summarization tasks.

### 🔹 Enhancements
1. **Retrieval Augmented Generation (RAG)**
   - Embeds documentation into a vector database
   - Uses similarity search to inject relevant context
2. **Fine-Tuning with LoRA (PEFT)**
   - Fine-tuned on ASME B31.3 to improve domain relevance
   - Customized model responses to match the style and structure expected by engineers

### 🔹 Final Architecture: RAFT
- **RAG + Fine-Tuned Model** = RAFT
- Improved factual accuracy, precision, recall, and style
- Reduced hallucinations and irrelevant information

---

## 📊 Evaluation

- **ROUGE**: Evaluates text overlap with reference answers
- **Cosine Similarity**: Measures semantic closeness
- **F-Score**: Combines both for a balanced metric

Weighted F = `w1*ROUGE + w2*CosSim`  
Example Weights: `[0.15, 0.15, 0.15, 0.15, 0.15, 0.25]`

---

## ⚙️ Limitations

- RAG struggles with tables unless preprocessed into readable text
- PEFT changes style more than raw accuracy
- No real-time integration with site-specific data yet

---

## 🚀 Next Steps

- Improve RAG table handling
- Deploy the app for domain expert testing
- Use feedback for another iteration of fine-tuning

---

## 👨‍💻 Demo

👉 [Click here for the Demo](https://docs.google.com/file/d/1aZoHrxFjo9OZCCWkMZBUVcW8ct-9I6J8/preview)

---

## 👥 Team Members

- Advik Mehta  
- Anant Bhide  
- Falak Sethi  
- Hanzhe Ye  
- Shreyank Hebbar  

**Domain Expert:** Brian Gue (PCL Industrial, Data Science)

---

## 📜 License
This project is for academic purposes and may be adapted or extended with proper attribution.
