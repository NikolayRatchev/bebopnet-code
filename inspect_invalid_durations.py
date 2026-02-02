import pickle
import os

pkl_dir = 'training_results/transformer/model'
with open(os.path.join(pkl_dir, 'train.pkl'), 'rb') as f:
    train_data = pickle.load(f)

with open(os.path.join(pkl_dir, 'converter_and_duration.pkl'), 'rb') as f:
    converter = pickle.load(f)

max_idx = converter.max_durations()  # this is an int

# Check for invalid durations
for song, arr in train_data.items():
    invalid = arr[:, 0] > max_idx  # duration column
    print(song, "invalid durations:", invalid.sum())
