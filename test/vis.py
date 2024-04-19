import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

def data_split():
    data = pd.read_csv("InnovAItors Q&A - Sheet1.csv")
    print(data.head())

    raw_Mistral_scores = data["Mistral scores"]
    Mistral_scores = [i.strip().split() for i in raw_Mistral_scores]
    Mst_score = []
    for item in Mistral_scores:
        Mst_score = []
        for i in range(0, len(item), 4):
            Mst_score.append(item[i+1: i+4])
        print(Mst_score)

def main():
    data = pd.read_csv("bar_plots.csv")
    fig = px.box(data, x=['Mistral f scores', 'Mistral + RAG f scores', 'Mistral fine-tuned f scores', 'Mistral Fine-Tuned + RAG f scores'], title="F-score across different model types")
    fig.show()

if __name__ == '__main__':
    main()
