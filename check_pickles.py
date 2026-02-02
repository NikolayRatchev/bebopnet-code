import os
import pickle

# === Paths ===
pkl_dir = "training_results/transformer/model"
train_pkl = os.path.join(pkl_dir, "train.pkl")
val_pkl = os.path.join(pkl_dir, "val.pkl")
converter_pkl = os.path.join(pkl_dir, "converter_and_duration.pkl")

# === Helper to print pickle info ===
def inspect_pickle(pkl_path, name):
    if not os.path.exists(pkl_path):
        print(f"{name} does not exist!")
        return None
    with open(pkl_path, "rb") as f:
        data = pickle.load(f)
    print(f"{name}: {len(data)} songs")
    for k, v in data.items():
        print(f"  {k}: shape {v.shape}")
    return data

# === Inspect train and val ===
train_data = inspect_pickle(train_pkl, "train.pkl")
val_data = inspect_pickle(val_pkl, "val.pkl")

# === Load converter ===
if not os.path.exists(converter_pkl):
    print("Converter file does not exist!")
    converter = None
else:
    with open(converter_pkl, "rb") as f:
        converter = pickle.load(f)

if converter:
    print("\nConverter type:", type(converter))

    # get number of durations
    num_durations = converter.max_durations()  # returns an int
    print("Number of durations:", num_durations)

    print("\nIndex -> Duration mapping:")

    # durations might be stored in 'durations' or can reconstruct as 1..num_durations
    # safest approach:
    try:
        durations_list = converter.durations  # may exist
    except AttributeError:
        # fallback: just enumerate indices
        durations_list = list(range(num_durations))

    for i, d in enumerate(durations_list):
        print(f"  {i} -> {d}")


