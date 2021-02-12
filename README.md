<p align="center">
  <img src="./assets/logo.png" alt="Everglades Analytics" width="512px" />
</p>
<br/><br/>

<!--
![](https://img.shields.io/static/v1?label=PHP&message=7.3.11&color=a6050d)
![](https://img.shields.io/static/v1?label=phpMyAdmin&message=5.0.1&color=orange)
![](https://img.shields.io/static/v1?label=Apache%20(Unix)&message=2.4.41&color=387f78)
![](https://img.shields.io/static/v1?label=MySQL&message=8.0.19&color=blue)
-->

_The best group out of all! (According to Rebecca)_

### Index

- [Instructions](#instructions)
- [Collaborators](#collaborators)
- [Description](#description)
- [Contents](#contents)
- [Resources](#resources)

### Instructions

1. Create the folders `data/processed/` and `data/raw/`.
1. Place all your raw `.SC2Replay` files as any structure inside `data/raw/`.
1. Use the jupyter notebook [notebooks/try_generator.ipynb](notebooks/try_generator.ipynb) to generate your datasets for Protoss, Terran, and Zerg.

### Collaborators

<p>
  <a href="https://www.github.com/elaineng21"><img src="https://avatars2.githubusercontent.com/u/65362312?s=400&v=4" alt="elaineng21" width="50px" /></a>
  <a href="https://www.github.com/Ipleau"><img src="https://avatars2.githubusercontent.com/u/46537009?s=400&v=4" alt="Ipleau" width="50px" /></a>
  <a href="https://www.github.com/vadManuel"><img src="https://avatars2.githubusercontent.com/u/7086685?s=400&u=a654bb2b5e4749953357409ed095979211e2daa6&v=4" alt="vadManuel" width="50px" /></a>
  <a href="https://www.github.com/oamer6"><img src="https://avatars2.githubusercontent.com/u/50599492?s=400&v=4" alt="oamer6" width="50px" /></a>
  <a href="https://www.github.com/tlukas23"><img src="https://avatars1.githubusercontent.com/u/55116369?s=400&v=4" alt="tlukas23" width="50px" /></a>
</p>

### Description

The goal of this project is to analyze, evaluate data, and predict match outcomes for StarCraft II, a real-time strategy game by Blizzard Entertainment. The information that we learn from this analysis can be used to set the base line for Everglades. Data will be collected and different analytics methodologies such as descriptive and diagnostic analysis will be performed. Machine learning algorithms will also be utilized for outcome prediction. The StarCraft II data will be collected as replay files from professional tournaments. It will then be parsed and prepared for analysis and modeling.

The first objective of this analysis is to find characteristics that can lead to wins in a StarCraft II match. To achieve this goal, descriptive analysis will be performed to provide basic information regarding the variables in our data set. Followed by an in-depth diagnostic analysis to find out details causing those outcomes. The second goal for this project is to find new metrics that can predict player’s performance. To achieve this goal, strategies similar to the first goal will be used, but we will be looking at different variables that can explain player’s performance such as action per minute (APM).

Map differences will be identified and studied to understand the effect it has on match outcomes with similar game strategies. This will be achieved by performing descriptive and diagnostic analysis, as well as applying machine learning algorithms. For match outcome prediction, a supervised machine learning classification algorithm will be trained using the characterized behaviors that were determined to be statistically significant to predict the outcome of a match given the current game state. Lastly, a real-time analytics engine that can run simultaneously with StarCraft II match playback will be developed. This engine shall be at a minimum able to predict odds of winning.

### Contents

```
.
├── assignments
│   ├── a2
│   │   ├── everglades_analysis_a2.tex
│   │   └── everglades_analysis_a2.pdf
│   └── final
│       ├── everglades_analysis_final.pdf
│       ├── everglades_analysis_final.tex
│       └── media
├── bin
│   ├── Tree.py
│   └── updateReadme.py
├── processing
│   └── sc2reader_test.py
├── README.md
├── readings
│   ├── tools
│   │   ├── pysc2.pdf
│   │   ├── stardata.pdf
│   │   ├── alphastar.pdf
│   │   ├── README.md
│   │   └── sc2_win_prediction.pdf
│   ├── intro
│   │   ├── deep-learning.pdf
│   │   ├── transformer.pdf
│   │   ├── README.md
│   │   ├── sparse-autoencoders.pdf
│   │   ├── useful-ml.pdf
│   │   └── first-cnns-backprop.pdf
│   └── assigner.py
├── data
│   └── functional
│       ├── races.json
│       └── units_dump.json
├── assets
│   └── logo.png
├── preparation
│   ├── playerstatsevent.md
│   ├── scrapers
│   │   └── scrape_pieces.py
│   └── generators
│       ├── WorkReplays.py
│       ├── UseReplay.py
│       └── Generator.py
└── notebooks
    ├── MapStuff.ipynb
    ├── terran
    │   └── NOTES.md
    ├── normalize.ipynb
    ├── zerg
    │   └── NOTES.md
    ├── try_generator.ipynb
    ├── protoss
    │   ├── NOTES.md
    │   ├── protoss_exploration.ipynb
    │   └── plots
    ├── initial.ipynb
    ├── plots
    ├── tryout.ipynb
    └── generator.ipynb
```

### Resources

- [Readings](/readings)
- [StarData](https://github.com/TorchCraft/StarData)
- [ESports Match Result Prediction](https://www.groundai.com/project/real-time-esports-match-result-prediction/1)
- [Replay packs](https://drive.google.com/drive/u/0/folders/1pJ1YhX--CKeL-LfHLv51RCu--aFAjj5P)
- [Generated datasets](https://drive.google.com/drive/folders/1vX-kV6igbE20wPHGDbz-XEXTmzAwSst4?usp=sharing)
