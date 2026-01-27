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

### What is the model predicting?

- At each timestep, BebopNet predicts the **next note event** in the sequence.
- Each note event is represented as a **structured vector** which includes:
  - **Pitch** (MIDI index)
  - **Duration** (discretized value, mapped via `VectorXmlConverter`)
  - **Tie / continuation information** (to represent notes spanning multiple timesteps)
  - **Measure-related metadata** used during generation
- An **EOS-like vector** exists in the representation, but is not the primary mechanism used to control solo length.

- The prediction is conditioned on:
  - The **current chord** (provided externally from the lead sheet)
  - A **fixed-length window of previous note events** (autoregressive generation with limited context)

- Notes that span multiple timesteps are handled via duration- and tie-aware encoding, allowing the model to distinguish between note continuation and new note onset.

---


### Prediction type

- The model outputs a **probability distribution over possible next note vectors**, rather than separate independent distributions for pitch and duration.
- During training:
  - The loss is computed as a cross-entropy objective on the predicted next-note vector.
- During generation:
  - The next note is selected using greedy decoding, stochastic sampling (temperature / top-p), or beam search.


### Key points

- Output is **symbolic** (note-level), not audio.
- Melody generation is **conditioned on fixed harmony** and recent musical context.
- Although an EOS vector exists, **solo length is primarily controlled externally** during generation (e.g., fixed to two choruses in the paper).

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

### Model types
- BebopNet implements **two architectures**:
  1. **LSTM-based model** – classical recurrent model, maintains hidden state across sequence.
  2. **Transformer-based model** – uses self-attention to capture long-range dependencies in the sequence.

### Time axis
- The model is **autoregressive**: each timestep corresponds to a single note event (pitch + duration + offset + harmonic context).
- Global time is implicit in the sequence order; each event advances the model’s internal state.

### Embedded information
At each timestep, the input vector includes:
- **Melody**: previous note’s pitch
- **Rhythm**: duration, bar-relative offset
- **Harmony**: current chord (root, chord mask, scale mask, chord type)
- Optionally, a **label or reward signal** if using reinforcement learning for personalization

### Output
- Next note event prediction (pitch, duration, EOS)
- For Transformer: input sequence is fed with positional encodings corresponding to event order
- For LSTM: input sequence is fed step by step; hidden state carries musical context

### Key concepts
- **Autoregressive generation**: the model predicts one event at a time
- **Conditioning on harmony**: chord information guides melodic choices
- **Duration-aware encoding**: model can generate notes that span multiple timesteps
- **EOS token**: allows variable-length outputs


---

## 7. Training loop (conceptual)
- Loss function
- What “correct” means here
- When does training stop?

BebopNet is trained autoregressively on sequences of symbolic musical events extracted from real jazz solos. Each training sequence consists of a variable-length list of note-event vectors terminated by an end-of-sequence (EOS) token.

At each training step, the model receives a prefix of the sequence and is trained to predict the next event. This includes predicting the EOS token at the appropriate point, allowing the model to learn when a solo should end.

The prediction task is formulated as classification over discrete vocabularies, including pitch, duration, and other symbolic attributes. Note durations and offsets are discretized during preprocessing to enable stable categorical prediction.

The training objective minimizes cross-entropy loss between the model’s predicted distributions and the ground-truth next event. Musical quality is not evaluated during training; the model learns by matching the statistical structure of the dataset.

Training terminates based on standard criteria such as validation loss convergence or a fixed number of epochs.


---


## 8. Generation
- How generation differs from training
- What is fixed vs free

During generation, BebopNet operates autoregressively without access to ground-truth future events. At each step, the model conditions on a fixed-length window of its previously generated note events together with the externally provided harmonic context to predict the next symbolic musical event.

The generation process proceeds by repeatedly sampling or selecting the next note vector from the model’s output distribution, appending it to the sequence, and advancing time implicitly via event order and bar-relative offsets rather than an explicit temporal grid.

While the model includes an end-of-sequence (EOS) token and is capable of predicting when a solo should terminate, musical form is typically enforced externally during generation. In the experiments reported by Hakimi et al., generated solos are constrained to a fixed length of two choruses by stopping generation after a predetermined number of bars or beats, rather than relying on EOS predictions.

Decoding decoding strategies—such as greedy decoding, stochastic sampling with temperature or nucleus (top-p) sampling, and beam search—can be used to select the next event at each step. hese choices significantly influence the balance between coherence and diversity in the generated improvisation.


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

- How are different predictions synced into one output? 

---

## 10. Ideas for blues adaptation
(do not evaluate yet)
