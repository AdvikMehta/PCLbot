
import pandas as pd
from benchmark.benchmark import Benchmark

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


# benchmark_base = Benchmark("base")
# benchmark_baserag = Benchmark("baserag")
# benchmark_ft = Benchmark("ft")
# benchmark_ftrag = Benchmark("ftrag")
# qa_pairs = read_csv(csv_file_path)
# print(qa_pairs)

# print("Running base")
# outputs_base = benchmark_base.run(qa_pairs)
# print("Saving base results")
# add_column_to_csv(csv_file_path, "base", outputs_base)
#
# print("Running baserag")
# outputs_baserag = benchmark_baserag.run(qa_pairs)
# print("Saving baserag results")
# add_column_to_csv(csv_file_path, "baserag", outputs_baserag)
#
# print("Running ft")
# outputs_ft = benchmark_ft.run(qa_pairs)
# print("Saving ft results")
# add_column_to_csv(csv_file_path, "ft", outputs_ft)
#
# print("Running ftrag")
# outputs_ftrag = benchmark_ftrag.run(qa_pairs)
# print("Saving ftrag results")
# add_column_to_csv(csv_file_path, "ftrag", outputs_ftrag)


csv_file_path = "qa_pairs_with_mode_outputs.csv"
qa_pairs = read_csv(csv_file_path)

modes = ["base"]
for mode in modes:
    benchmark = Benchmark(mode)
    print(f"Running {mode}")
    outputs = benchmark.run(qa_pairs)
    print(f"Saving {mode} results")
    add_column_to_csv(csv_file_path, mode, outputs)

benchmark = Benchmark("ftrag")
qa_pairs = read_csv("qa_pairs_with_mode_outputs.csv")[0:5]
print(qa_pairs)

outputs = benchmark.run(qa_pairs)
print(outputs)

# add_column_to_csv("qa_pairs_with_mode_outputs.csv", "base", outputs_base)
# add_column_to_csv("qa_pairs_with_mode_outputs.csv", "baserag", outputs_baserag)


