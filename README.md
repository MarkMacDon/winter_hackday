# winter python hackathon

## Getting Started
You'll need:
- Python 3.9
https://www.python.org/downloads/release/python-390/

- An IDE or text editor in order to write some python code.
I use PyCharm (the community edition is free), or I hear vscode is good.

- Git, for downloading and uploading this codebase.
  - On windows: https://git-scm.com/download/win
  - Linux / Mac: I don't know, maybe its already installed?


Move into a folder you want to work in and run the command to download this codebase:

```
git clone https://github.com/ElliotSalisbury/winter_hackday.git
```

and then to install the required libraries (matplotlib, numpy, etc)

```
cd winter_hackday
pip install -r requirements.txt
```

On the day, there may need to be a reason to pull changes to this repository, if there are bug fixes.
```
git pull 
```

## Important files
#### animations/start_here.py

This will be the main file you will be working on. make a copy of this file, name it something sensible, and start writing your code

In order to run your code, the working directory needs to be the project root (in order to find the coordinates file)
IDE's can usually handle this fine, but if you are running from a terminal, try this:

```
python -m animations.my_animation_file
```

#### animations/exploding_lights.py
#### animations/spinning_lights.py
#### animations/moving_object.py

I have written a few examples of animations, hopefully these will give you an idea of how you can interact with the data being passed into the calculate_colors() function, and how to return sensible colors

```
python -m animations.spinning_lights
```


#### demo_cycle.py
This will be used on the raspberry pi to cycle through the animations in the animations directory.
We are


#### anything else
No real need to dive too deep into these, you should be able to work without them. They just handle the direct communication with the lights, or matplotlib. Feel to explore if you wish. 