from benchmark.benchmark import Benchmark
import pandas as pd

def read_csv(file_path):
    df = pd.read_csv(file_path)
    df.fillna('', inplace=True)
    return [(question, answer) for question, answer in zip(df.iloc[:, 0], df.iloc[:, 1]) if question and answer]

def add_column_to_csv(file_path, column_name, data_list):
    df = pd.read_csv(file_path)
    # if len(data_list) != len(df):
    #     raise ValueError('Length of new column data does not match number of rows in the existing CSV')

    df[column_name] = data_list
    df.to_csv(file_path, index=False)


benchmark = Benchmark("ftrag")
qa_pairs = read_csv("qa_pairs_with_mode_outputs.csv")[0:5]
print(qa_pairs)

outputs = benchmark.run(qa_pairs)
print(outputs)

# add_column_to_csv("qa_pairs_with_mode_outputs.csv", "base", outputs_base)
# add_column_to_csv("qa_pairs_with_mode_outputs.csv", "baserag", outputs_baserag)

