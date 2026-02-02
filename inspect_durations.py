import pickle
import os

# Path to your model folder
pkl_dir = 'training_results/transformer/model'
converter_path = os.path.join(pkl_dir, 'converter_and_duration.pkl')

# Load the converter
with open(converter_path, 'rb') as f:
    converter = pickle.load(f)

print("Converter type:", type(converter))
print("Number of durations:", converter.max_durations())

# List all valid durations
print("\nIndex -> Duration mapping:")
for idx in range(converter.max_durations()):
    dur_value = converter.ind_2_dur(idx)
    print(f"  {idx} -> {dur_value}")

# Optional: see the max duration
max_idx = converter.max_durations() - 1
print(f"\nMaximum duration index: {max_idx}, value: {converter.ind_2_dur(max_idx)}")
