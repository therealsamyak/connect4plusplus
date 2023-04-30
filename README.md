# Connect4plusplus

## Inspirations
Connect 4 is a simple board game rulewise, yet the theory behind it is very interesting. That is why we wanted to try our hands at both understanding this theory, and adding our own modifications based on it. 

## What It Does
We have multiple game modes available to play:

**1. Player vs Player** - Classic Connect 4 Experience with both Place and Pop options!

**2. Player vs Easy AI** - Single Player Connect 4 against Random Robbie!

**3. Player vs Medium AI** - Single Player Connect 4 against Mediocre Matthew!

In addition, the board size can be changed for any of the game modes above, from 4 x 4 up to 20 x 20

## How We Built It
We built a scalable matrix with filler values to serve as our base board. Next, we determined the "coin" physics by accounting for gravity. After that, we accounted for edge cases, like how it is impossible to place a coin on a column that is already full. Most importantly, we had to code the win conditions (4-in-a-row alongside the vertical, horizontal, positive-sloped, and negative-sloped axis). Finally, we coded our own miniature AIs, using both random number generators and a "score" system.  

## Challenges We Ran Into
Implementing the score system for the Medium AI was the hardest part of the challenge. It took forever to get it to work somewhat decently. 

## Accomplishments that we're proud of
Adding "voicelines" to the AIs was one of the best decisions we made, because it was really funny and added more personality to the AI and the game. 

## What We Learned
We learned the importance of time-management. In addition, we learned how to implement the concepts we learned in C++ to Python, and make them work effectively.

## What's Next for Connect4++
We are thinking of potentially adding a game mode where the board starts full, and you keep "popping". In addition, adding multi-language support either through an API or just manually having multiple files depending on the language would also be nice. 
