# Uno Basic
Recreation of the classic Uno card game with modified rules, text-based graphics, and computer-controlled AI players. 
Created during my Sophomore year at DePaul university, my goals with this project was to create a text-based game in 
python that included colors, effects, intelligent computer players, and an attractive user-interface without the use of 
external modules.

## Getting Started
__Language Version:__ Python 3.5

__Usage:__
```
python3 app.py
```
The Uno Basic repository includes the following python modules:
* app.py
* card.py
* computer_player.py
* deck.py
* game_settings.py
* hand.py
* match.py
* player.py

Uno Basic does not require the download of any third-party modules and only uses standard Python library modules.

## How To Play

Uno Basic is a close recreation to the classic Uno Game and includes many of the same rules, however some rules have
been modified to add to a more competitive experience.

### Rules
* 2-4 Players.
* First turn is selected at random.
* Players place cards onto the pile that match either the color or value of the piles topmost card.
* First player to empty hand of all cards wins.
* Winning player gets points based on the values of the remaining cards in the opponents hands
* Draw Four cards may only be used when no other card can be legally placed.
* Reverse Cards act as skips during games with only two players.
* If deck is empty and player has no usuable cards, the player may pass their own turn.

### Controls
* __p -__ Pause Game
* __d -__ Draw Card
* __0-9 -__ Place card from hand
* __<, > -__ Scroll through hand
* __s -__ Pass turn
