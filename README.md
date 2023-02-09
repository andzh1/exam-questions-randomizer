# Randomizer
## Description
This is my pet project of a simple randomizer. I thought of it as of something that can help me to prepare for my exams. You can interact with it using scalable QT window, which has few fields: 
- It displays you number of qestion you should answer. Color of window depends on how hard is this question for you: white -> green -> yellow -> orange -> red in order from easiest to hardest. View code for details.
- `Yes`, `No` buttons -- you press `Yes` if you've answered given question and `No` otherwise.
- You can also `Skip` question.

## Usage
1. Clone this repository. For example, using SSH: type in terminal `git clone git@github.com:andzh1/randomizer.git`.
2. Go to directory `./randomizer`, and type in terminal `poetry install`. That will install dependencies for project. You can read more about poetry [here](https://python-poetry.org/).
3. Just run `qt-randomizer.py`!

## Technologies used
- **QT**
- **SQL** - used for storing data
- **Poetry** - package manager

Feedback is welcome!