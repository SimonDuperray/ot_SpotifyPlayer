# -*- coding: utf-8 -*-
"""
Spotify Player
"""

import pandas as pd
import requests
import json
from datetime import datetime
import datetime
from IPython.display import display
from tkinter import *

USER_ID = ""
TOKEN = ""

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Bearer {token}".format(token=TOKEN)
}

requests_kinds = {
    'play': 'https://api.spotify.com/v1/me/player/play',
    'pause': 'https://api.spotify.com/v1/me/player/pause',
    'next': 'https://api.spotify.com/v1/me/player/next',
    'previous': 'https://api.spotify.com/v1/me/player/previous',
    'shuffle': 'https://api.spotify.com/v1/me/player/shuffle?state=true',
    'repeat': 'https://api.spotify.com/v1/me/player/repeat?state=off',
    'volume': 'https://api.spotify.com/v1/me/player/volume',
    'currently_playing': 'https://api.spotify.com/v1/me/player/currently-playing',
    'device': 'https://api.spotify.com/v1/me/player/devices'
}

"""## Currenlty Playing Part"""

currently_playing_request = requests.get(requests_kinds['currently_playing'], headers=headers)
currently_playing_data = currently_playing_request.json()

"""#### Songer"""

currently_playing_songer = currently_playing_data['item']['album']['artists'][0]['name']
print(currently_playing_songer)

"""### Title"""

currently_playing_title = currently_playing_data['item']['name']
print(currently_playing_title)

"""#### Get Device"""

device_request = requests.get(requests_kinds['device'], headers=headers)
device_data = device_request.json()
device_id = device_data['devices'][0]['id']

print("device id: "+str(device_id))

# Graphic User Interface

def pause():
    requests.put(requests_kinds['pause'], headers=headers)
    print("pause: "+str(requests.put(requests_kinds['pause'], headers=headers)))

def play():
    requests.put(requests_kinds['play'], headers=headers)
    print("play: "+str(requests.put(requests_kinds['play'], headers=headers)))

def next():
    requests.post(requests_kinds['next'], headers=headers)
    requests.post(requests_kinds['previous'], headers=headers)
    print("next: "+str(requests.post(requests_kinds['next'], headers=headers)))

def previous():
    requests.post(requests_kinds['previous'], headers=headers)
    requests.post(requests_kinds['next'], headers=headers)
    print("previous: "+str(requests.post(requests_kinds['previous'], headers=headers)))

def shuffle():
    requests.put(requests_kinds['shuffle'], headers=headers)
    if list(requests_kinds['shuffle'])[-2]=='u':
        requests_kinds['shuffle']='https://api.spotify.com/v1/me/player/shuffle?state=false'
        shuffle_state.set(list(requests_kinds['shuffle'])[-5:len(list(requests_kinds['shuffle']))])
    elif list(requests_kinds['shuffle'])[-2]=='s':
        requests_kinds['shuffle']='https://api.spotify.com/v1/me/player/shuffle?state=true'
        shuffle_state.set(list(requests_kinds['shuffle'])[-4:len(list(requests_kinds['shuffle']))])
    print("shuffle: "+str(requests.put(requests_kinds['shuffle'], headers=headers))+" state: "+shuffle_state.get())

def repeat():
    requests.put(requests_kinds['repeat'], headers=headers)
    if list(requests_kinds['repeat'])[-1]=='f':
        requests_kinds['repeat']='https://api.spotify.com/v1/me/player/repeat?state=track'
        repeat_state.set('false')
    elif list(requests_kinds['repeat'])[-1]=='k':
        requests_kinds['repeat']='https://api.spotify.com/v1/me/player/repeat?state=off'
        repeat_state.set('true')
    else:
        pass
    print("repeat: "+str(list(requests.get(requests_kinds['repeat'], headers=headers)))+' state: '+repeat_state.get())

gui = Tk()
gui.geometry("300x300")
title_label = Label(gui, text=currently_playing_title).pack()
songer_label = Label(gui, text=currently_playing_songer).pack()
pause_button = Button(gui, text="Pause", command=pause).pack()
play_button = Button(gui, text="Play", command=play).pack()
next_button = Button(gui, text="Next", command=next).pack()
previous_button = Button(gui, text="Previous", command=previous).pack()
shuffle_button = Button(gui, text="Shuffle", command=shuffle).pack()
shuffle_state = StringVar()
# conditional rendering shuffle state
if list(requests_kinds['shuffle'])[-2]=='s':
    shuffle_state.set('false')
elif list(requests_kinds['shuffle'])[-2]=='u':
    shuffle_state.set('true')
shuffle_label = Label(gui, textvariable=shuffle_state).pack()
repeat_button = Button(gui, text="Repeat", command=repeat).pack()
repeat_state = StringVar()
# conditional rendering repeat state
if list(requests_kinds['repeat'])[-1]=='f':
    repeat_state.set("false")
elif list(requests_kinds['repeat'])[-1]=='k':
    repeat_state.set('true')
repeat_label = Label(gui, textvariable=repeat_state).pack()
gui.mainloop()
