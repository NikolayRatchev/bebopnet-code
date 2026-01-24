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

    Rhythmic information is extracted from symbolic MusicXML scores. Rhythm is represented symbolically using quantized score divisions.
    Durations are integer multiples of a base temporal unit, with notes spanning multiple timesteps when necessary.

    Expressive timing (swing feel, microtiming) is not explicitly modeled

## 3. Input to the model
- What is a single training example? 
- What musical information is included?
- How long is a sequence?

#### A single training example (Hypothesis)
    One training example likely consists of a fixed-length sequence of musical timesteps.
    At each timestep, the input includes the current harmony and the previously generated note (or rest).
    The training target is the next note in the sequence (pitch + duration).
    The sequence length determines how much musical context the model can use.

    Hypotheticsl mental model:
    Input (timesteps 1–8)  →  Output (timestep 9)
    Input (timesteps 2–9)  →  Output (timestep 10)
    Input (timesteps 3–10) →  Output (timestep 11)


    Each training sequence is derived from MusicXML measures.

    - Melody is represented as sequences of notes with explicit pitch and duration.
    - Rhythm is quantized using score divisions; notes may span multiple timesteps.
    - Harmony is given symbolically and can change mid-measure; the model conditions on the current chord at each timestep.

#### How is musical time represented? 
    Musical time is discretized into a fixed number of timesteps per measure.
    Although MusicXML files specify different `<divisions>` values, these are normalized during preprocessing so that all examples share a common temporal grid.
    Notes span multiple timesteps according to their duration.

#### How is harmony represented?
Harmony is represented symbolically using chord roots and chord qualities.
Chord labels may change within a measure.
Each timestep is associated with the currently active harmony.

#### What counts for one sequence?
The timestep timelines constructed from MusicXML can be segmented into overlapping sequences.
Each sequence serves as one training example, where the model learns to predict the next note given the recent musical context and harmonic information.



## 4. Output of the model
- What is the model predicting?
- One note? One bar? A distribution?

    The model predicts the next melodic token at each timestep, taking into account the current chord and previous melodic state.
    Tokens may represent pitch and/or note duration, and notes that span multiple timesteps are handled with a hold-state or duration-aware encoding.


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
1. Where should command-line flags (e.g., --beam_search) be specified when running the model?
2. How is the length of a generated solo defined? How does the model know when to stop?
3. What is the format of the model’s output? Is it MusicXML, MIDI, or another representation?

Suggested by ChatGPT:
1. How exactly are MusicXML durations converted into model timesteps?
2. How does the model represent mid-measure chord changes for conditioning?
3. How does the model encode notes that span multiple timesteps?

## 10. Ideas for blues adaptation
(do not evaluate yet)
