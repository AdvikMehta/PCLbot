from benchmark.benchmark import Benchmark

benchmark = Benchmark("baserag")

out = benchmark.run([
    ("According to ASME B31.3, what is the minimum design metal temperature (in °F) for carbon steel without impact testing?", "-20 F")
])

print(out)

