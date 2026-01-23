# BebopNet — Guided Understanding Notes

## 1. What problem is BebopNet solving?
(Answer in plain English, no code terms yet)
    The whole framework solves 3 problems:
    1. Learns to improvise sax melodies in bebop style when provided with chord changes. 
    2. Elicitis listeners' preferences. 
    3. Adapts the improvised melodies to the listener's personal taste. 

## 2. Musical assumptions
- Style (bebop, swing, etc.)
    - Mostly bebop, hardbop, post-bop

- Form (blues? standards? free?)
    - Mostly standards, 
    - Bossa Novas (Getz)
    - Blues (but not many)

- Harmony representation

    Harmony is represented symbolically using chord objects extracted from MusicXML.
    Each chord specifies an explicit root (e.g., G) and quality/extension (e.g., dominant ninth).
    These chord symbols are provided as ground-truth conditioning information for melody generation.

    I.e:
    Harmony is represented symbolically via MusicXML chord annotations (root + chord kind), which are later encoded numerically to condition the model.

- Rhythm assumptions
    Rhythm is discretized into fixed time steps.
    The exact temporal resolution (e.g. 8th notes vs 16th notes) is not yet clear.
    Expressive timing (swing feel, microtiming) is not explicitly modeled

## 3. Input to the model
- What is a single training example? 
    - an .xml file. I opened one. MuseScore is mentioned as a relevant software. 
    Each training example consists of a melodic sequence aligned with a chord progression.
    At each time step, the model receives information about the current harmonic context and the previous melodic state.
    Melody and harmony are represented symbolically and encoded numerically for the network.
    The precise feature representation per timestep is still under inspection.


- What musical information is included?
- How long is a sequence?

## 4. Output of the model
- What is the model predicting?
- One note? One bar? A distribution?

    At each time step, the model predicts the next melodic event.
    This is likely represented as a probability distribution over possible note values (e.g., pitch classes or interval-based representations).
    During generation, notes are sampled from this distribution to produce an improvised melodic line.

## 5. Data flow (high level)
raw data → preprocessing → model → output

## 6. Model architecture (conceptual)
- Type (RNN, LSTM, Transformer, etc.)
- What information is embedded?
- What is the time axis?

## 7. Training loop (conceptual)
- Loss function
- What “correct” means here
- When does training stop?

## 8. Generation
- How generation differs from training
- What is fixed vs free

## 9. What is unclear / confusing
(write questions, not answers)
- README: where am I supposed to put these flags (e.g. `--beam_search`)?
- How do I define chorus length? 

## 10. Ideas for blues adaptation
(do not evaluate yet)
