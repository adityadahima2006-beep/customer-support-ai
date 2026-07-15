from datasets import load_dataset

print("Downloading Banking77 dataset...")

dataset = load_dataset("PolyAI/banking77")

print(dataset)

print("\nFirst training example:")
print(dataset["train"][0])