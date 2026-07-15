from datasets import load_dataset

print("Loading Banking77 Dataset...\n")

dataset = load_dataset(
    "PolyAI/banking77",
    trust_remote_code=True
)

# Display dataset information
print(dataset)

# Print available intent names
print("\nAvailable Intent Labels:\n")

labels = dataset["train"].features["label"].names

for i, label in enumerate(labels):
    print(f"{i} --> {label}")
