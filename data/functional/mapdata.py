import sc2reader
from sc2reader.engine.plugins import APMTracker, ContextLoader, SelectionTracker
from sc2reader import data
from sc2reader.events import *
import os
import glob
import pandas as pd
import json
from collections import Counter

counter = 0
#path = "C:/Users/iplea/Desktop/HSC19"
#os.chdir(path)

unit_data = json.loads(data.unit_data)
unit_map = {}
df = []
Matchup = []
map_list=[]
map_frequency=[] 






for replay in sc2reader.load_replays(glob.glob('C:/Users/iplea/Desktop/Replays/**/*.SC2Replay', recursive=True)):
    if counter > 10:
        break
    if replay.map_hash not in map_list:
        map_list.append(replay.map_hash)


    mapnumb = map_list.index(replay.map_hash)
    
    Matchup.append([counter, replay.game_length, replay.players[0].result,  replay.players[1].result, replay.players[0].pick_race[0], replay.players[1].pick_race[1], mapnumb, len(map_frequency)])
    map_frequency.append(mapnumb)
    counts = Counter(map_frequency)
    counts.most_common()
    
    counter += 1

Matchup = pd.DataFrame(Matchup)
pd.set_option("display.max_rows", None, "display.max_columns", None)
columns = ["Match ID", "Game Length", "Player 1 Result", "Player 2 Result", "Player 1 Race", "Player 2 Race", "Map", "test"]
Matchup.columns = columns
Matchup.to_csv('C:/Users/iplea/Desktop/mapData2.csv', index=False)
