## Moving to Object Oriented

We need an Enemy class

What can an Enemy do?

- can shoot
- can die
- should have a point value
- can move
- is a Rect

how to do this?
while creating grid, we need to create new Enemy and based on the current row we define a different point value?

should movement be a separate class? No, cause the movement is not constant throughout the game.

sep 7

- need barriers - just decrease size of barrier
- I'm buront out of this honestly
- increase speed as less enemies on screen - done
- maybe add levels
  - funciton called increase level
  - if all enemies die increase level
  - increase level changes attributes of Enemy objects and re passes them to the game
    - more enemies?
    - enemies closer to player?
    - faster shooting?
    - etc

player class

- actions
- shooting
- movement
- attributes
- lives
- x position
- y position

what needs to be done now

- player shooting and killing enemies and increase player score
- enemy movement and reversal
- increasing speed as fewer enemies
- draw sprites

current problems - sep 10

- still need to draw sprites
- only bottom row of enemies is shooting
- speed of enemies is not increasing as more die
- levels
