import os, pickle

pkl_dir = 'training_results/transformer/model'
for fname in ['train.pkl', 'val.pkl', 'converter_and_duration.pkl']:
    path = os.path.join(pkl_dir, fname)
    if not os.path.exists(path):
        print(f"{fname} is missing!")
    else:
        size = os.path.getsize(path)
        print(f"{fname}: exists, size {size} bytes")

with open(os.path.join(pkl_dir, 'train.pkl'), 'rb') as f:
    train = pickle.load(f)
with open(os.path.join(pkl_dir, 'val.pkl'), 'rb') as f:
    val = pickle.load(f)

print(f"Number of training songs: {len(train)}")
print(f"Number of validation songs: {len(val)}")
for k, v in train.items():
    print(f"Train song {k}: shape {v.shape}")


with open(os.path.join(pkl_dir, 'converter_and_duration.pkl'), 'rb') as f:
    converter = pickle.load(f)

print(f"Converter type: {type(converter)}")
print(f"Max durations: {converter.max_durations()}")

for name, arr in train.items():
    invalid = arr[:, 0] >= converter.max_durations()  # duration column
    if invalid.any():
        print(f"{name} has {invalid.sum()} invalid durations")
