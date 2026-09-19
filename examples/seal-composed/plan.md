# SEAL composition plan

Central question: can learning to rewrite a passage improve knowledge incorporation, and does that advantage persist across adaptation regimes?

The figure must retain all five Table 2 methods and all three conditions. It must show SEAL below GPT-4.1 data in the two continued-pretraining conditions. The small Lyra example is constructed, never a reported model generation.

Three layouts are sketched in `layout-sketches.svg` before detailed rendering:

1. **Selected: vertical explanation at left, aligned experimental columns at right.** Approximately 35% explanatory width and 65% evidence width. A notebook connects original text to rewritten training data; a weight update and no-passage question explain the use of that data. Shared method rows and equal numerical scales make the three outcomes directly inspectable.
2. Horizontal adaptation ribbon above three graphs. Clear mechanism order, but leaves too little height for five method rows at readable type size.
3. Central adaptation loop surrounded by results. Suits a method figure, but divides the numerical evidence and makes cross-condition comparison harder.

The selected layout is an introduction teaser, not the full nested RL training algorithm. Its left panel explicitly shows adaptation after the rewrite policy has been learned. The existing SEAL method example documents the outer RL training loop.

Asset plan: one generated, text-free notebook illustration; vector passage and implication text; vector weight glyph and connections; Matplotlib vector result panels with exact source-linked values. No generated chart, equation, or numerical result.

Physical plan: initially 504 × 336 pt; final height 342 pt adds room for the source note. Text 8 pt or larger. Standalone graphs: 504 × 250 pt. All exports derive from the canonical specifications initialized by `build.py`; `composition.json` defines final assembly geometry and subsequent builds read it without overwriting edits.
