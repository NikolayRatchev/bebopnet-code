import pickle
import os
from fractions import Fraction
from jazz_rnn.utils.music.vectorXmlConverter import VectorXmlConverter

# Path to your model folder
MODEL_DIR = 'training_results/transformer/model'
OLD_PKL = os.path.join(MODEL_DIR, 'converter_and_duration.pkl')
NEW_PKL = os.path.join(MODEL_DIR, 'converter_and_duration_short.pkl')

# Load old converter
with open(OLD_PKL, 'rb') as f:
    old_converter = pickle.load(f)

# Current durations
old_durs = old_converter.durations if hasattr(old_converter, 'durations') else [
    Fraction(1,6), Fraction(1,4), Fraction(1,3), Fraction(1,2), Fraction(2,3),
    Fraction(1,1), Fraction(7,6), Fraction(4,3), Fraction(3,2), Fraction(2,1),
    Fraction(5,2), Fraction(3,1), Fraction(7,2), Fraction(4,1), Fraction(9,2),
    Fraction(5,1), Fraction(6,1), Fraction(7,1), Fraction(17,2)
]

# Add shorter durations: 1/32, 1/16, 3/32, 1/8, 3/16, etc.
short_durations = [Fraction(1,32), Fraction(1,24), Fraction(1,16), Fraction(3,32),
                   Fraction(1,12), Fraction(1,8), Fraction(3,16)]

# Merge and remove duplicates, sort ascending
new_durations = sorted(set(short_durations + old_durs))

# Create a new converter
new_converter = VectorXmlConverter(new_durations)

# Save new converter
with open(NEW_PKL, 'wb') as f:
    pickle.dump(new_converter, f)

print(f"New converter saved to {NEW_PKL}")
# print("Durations:")
# for i, d in enumerate(new_converter.durations):
#     print(f"  {i} -> {d}")
print("Durations:")
for i in range(new_converter.max_durations()):
    dur = new_converter.ind_2_dur(i)   # get duration by index
    print(f"  {i} -> {dur}")