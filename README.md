## Summary
Simulation software for Counter-Strike: Global Offensive professional matches. This software parses player information from https://www.hltv.org/

## Required software
* Python 3  
https://www.python.org/downloads/

## How to use
`python simulation.py`

Note that some operating system will require you to run Python as `python3`

The program will ask for a match URL from the HLTV website and begin parsing the site for player stats. It will simulate three different simulations:

* Kill-Death Ratio Simulation
* Kill Per Round Simulation
* HLTV Rating Simulation

In my experience, the kill per round simulation is the most accurate simulation.

At the end of the simulation, the user will be prompted to export the match data to an OpenDocument Spreadsheet (.ods)

## How it works
*simulation.py* will spend time parsing the HTML of the HLTV stats website and simulate a game played based on their statistics.

## Potential features to be added
* GUI interface with tkinter
