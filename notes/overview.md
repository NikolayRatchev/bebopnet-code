# BebopNet — Guided Understanding Notes

## 1. What problem is BebopNet solving?
The framework addresses three related problems:
1. Learning to improvise bebop-style jazz melodies conditioned on chord changes.
2. Eliciting listener preferences through interactive feedback.
3. Adapting generated improvisations to individual listener tastes via reward induction.

*Note*. 2. & 3. are extensions beyon the base model; the core contribution of BebopNet is the conditional jazz improvisation system.

---

## 2. Musical assumptions
### Style (bebop, swing, etc.)
- Primarily bebop, hardbop, post-bop jazz styles

### Form (blues? standards? free?)
- Mostly jazz standards, 
- Bossa Novas (e.g., Stan Getz)
- Fewer blues forms

### Harmony representation
- Harmony is represented symbolically via MusicXML chord annotations (root + chord kind). 
- Chord symbols are treated as ground-truth conditioning information and encoded numerically for the model.

### Rhythm & time representation
- Rhythm is represented symbolically using note durations and bar-relative offsets extracted from MusicXML.
- Durations are discretized into a finite vocabulary of observed note lengths.
- Time does not advance on a fixed grid; instead, each musical event encodes its own duration and position within the bar. 
- Expressive timing (swing feel, microtiming) is not explicitly modeled

### Update 2026-01-24
BebopNet models jazz improvisation as a sequence of event-based timesteps, where each timestep is a vector containing melodic, rhythmic, temporal, and harmonic information.

### Update 2026-01-26
BebopNet does not advance time by ticks.
It advances time by musical events, and each event describes its own timing.

---

## 3. Input to the model

### What is a single training example? 
- In BebopNet, one training example is a **variable-length sequence of note-event vectors** extracted from a single MusicXML solo 
- Each sequence is terminated by a special end-of-sequence (EOS) token. 
- Each event encodes pitch, duration, bar-relative offset, and harmonic context (see below).
- The model is trained autoregressively to predict the next musical event in the sequence, including the EOS symbol.


### What musical information is included?
Internal representation (from gather_data_from_xml.py)
Each musical event is represented as a fixed-length vector containing:
- pitch (MIDI)
- duration (quarter-note units)
- offset within the bar (quantized)
- explicit harmonic context:
    - chord root 
    - scale pitch mask 
    - chord pitch mask
    - chord type index


#### How conditioning
- Harmony is represented symbolically using chord roots and chord qualities.
- Chord labels may change within a measure.
- Each timestep is associated with the currently active harmony.


#### Parsing library
- MusicXML files are parsed using the Music21 library, which is imported indirectly via vectorXmlConverter.py. 
- Objects such as notes, rests, chord symbols, offsets, durations, and ties follow Music21’s semantics during preprocessing

#### Offset representation
- BebopNet uses Music21’s absolute offset only temporarily. 
- During preprocessing, the offset is reduced modulo the bar length (4 beats) and quantized into a fixed 48-step grid per bar. 
- The model therefore encodes where a note starts within the bar, but not the bar index itself. 
- Global time progression is represented implicitly by sequence order.

#### Duration encoding
- Note durations are discretized into a finite vocabulary using `VectorXmlConverter`. 
- Each unique duration observed in the dataset is mapped to an integer index. 
- Duration prediction is treated as a classification task rather than regression, ensuring stable training and stable symbolic decoding during generation.


### How long is a sequence?
Each training sequence ends with an explicit EOS vector.
During generation, the model predicts EOS as a classification target and signals termination of the solo. 
- EOS is represented as a dedicated vector outside the normal pitch, duration, offset, and chord ranges.
- Although BebopNet includes an explicit end-of-sequence (EOS) token and is capable of learning when to terminate a solo, in the experiments reported by Hakimi et al. the solo length is externally constrained to a fixed duration of two choruses. 
- Thus, EOS serves primarily as a modeling and training mechanism, while musical form is enforced at generation time.

---


## 4. Output of the model

- BebopNet outputs a sequence of symbolic musical events. 
- At each step, the model predicts the next pitch-duration token or an EOS toekn.
- Generation is autoregressive, conditioned on harmonic context and prior events.

---


## 5. Data flow (high level)

``` scss
MusicXML files
   ↓
gather_data_from_xml.py
   ↓
Python objects (lists / dicts / arrays)
   ↓
pickle (.pkl)
```

- Preprocessing is performed by the script `gather_data_from_xml.py`
- The script parses MusicXML files, converts them into a numerical sequence representation, and serializes the resulting datasets using pickle. 
- The resulting pickle files contain variable-length sequences of event vectors, suitable for autoregressive training.

---


## 6. Model architecture (conceptual)
- Type (RNN, LSTM, Transformer, etc.)
- What information is embedded?
- What is the time axis?

---

## 7. Training loop (conceptual)
- Loss function
- What “correct” means here
- When does training stop?

---


## 8. Generation
- How generation differs from training
- What is fixed vs free

---


## 9. What is unclear / confusing

1. Where should command-line flags (e.g., --beam_search) be specified when running the model?
2. How is the length of a generated solo defined in practice during inference?
3. What is the format of the model’s output (event vectors, MusicXML, MIDI, etc.)? 


### 2025-01-24
From README.md
1. The README mentions pickling XML files:
> Collect the dataset from xml files into a network-friendly format and pickle it
 but it is unclear where XML parsing and numerical encoding are implemented in this repository.

2. The README mentions configuration via YAML files, but no example config
   or loading mechanism is provided in the repository.


### Questions for Day 4 (Models)

- What exactly differs between the LSTM and Transformer inputs?
- Are pitch, duration, and offset predicted jointly or separately?
- How does chord information enter the model (concatenated? embedded?)

---

## 10. Ideas for blues adaptation
(do not evaluate yet)
