import pickle
from jazz_rnn.utils.music.vectorXmlConverter import VectorXmlConverter
from bidict import bidict

OLD_PKL = "training_results/transformer/model/converter_and_duration_OLD.pkl"
NEW_PKL = "training_results/transformer/model/converter_and_duration.pkl"
MERGED_PKL = "training_results/transformer/model/merged_converter_and_duration.pkl"

class SkipConverterUnpickler(pickle.Unpickler):
    """Skip unpickling the old converter (bidict) to avoid errors."""
    def find_class(self, module, name):
        if module.startswith("bidict") or name == "bidict":
            return lambda *args, **kwargs: None
        return super().find_class(module, name)

def load_old_durations(old_pkl):
    with open(old_pkl, "rb") as f:
        unpickler = SkipConverterUnpickler(f)
        _ = unpickler.load()  # skip old converter
        old_durations = unpickler.load()  # get durations
    return old_durations

def load_new_converter_and_durations(new_pkl):
    with open(new_pkl, "rb") as f:
        new_converter = pickle.load(f)
        new_durations = pickle.load(f)
    return new_converter, new_durations

def merge_converters(old_pkl, new_pkl, merged_pkl):
    print("Loading old durations...")
    old_durations = load_old_durations(old_pkl)

    print("Loading new converter and durations...")
    new_converter, new_durations = load_new_converter_and_durations(new_pkl)

    print("Merging durations...")
    merged_durations = sorted(set(old_durations) | set(new_durations))

    print("Creating merged converter...")
    merged_converter = VectorXmlConverter(merged_durations)

    print(f"Saving merged converter and durations to {merged_pkl} ...")
    with open(merged_pkl, "wb") as f:
        pickle.dump(merged_converter, f)
        pickle.dump(merged_durations, f)

    print("Done!")

if __name__ == "__main__":
    merge_converters(OLD_PKL, NEW_PKL, MERGED_PKL)
