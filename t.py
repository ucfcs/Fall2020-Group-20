import sc2reader
from sc2reader.engine.plugins import APMTracker, ContextLoader, SelectionTracker
from sc2reader import data
from sc2reader.events import *
import os,glob
import pandas as pd
import json

T_gang = []
counter = 0;
path = "C:/Users/tluka/Desktop/HSC XIII Replay Pack"
os.chdir(path)

unit_data = json.loads(data.unit_data)
unit_map = {}

for k in unit_data:
    unit_map[k] = list(unit_data[k].keys())

pt_dict = dict.fromkeys(unit_map['Terran'],0)
#print(pt_dict)

for replay in sc2reader.load_replays(glob.glob('../**/*.SC2Replay', recursive=True)):
	if counter > 10:
		break
	if replay.players[0].pick_race[0] == 'T' or replay.players[1].pick_race[0] == 'T':
		for event in replay.events:
			if event.second %30 == 0:
				if type(event) is PlayerStatsEvent:
					if replay.players[0].pid == event.pid and replay.players[0].pick_race[0] == 'T':
						T_gang.append([counter, event.second, replay.players[0].result, event.player, replay.players[0].pick_race[0], event.workers_active_count,
                                event.food_used, event.food_made, event.minerals_current, event.minerals_collection_rate, 
                                event.minerals_used_in_progress, event.minerals_used_current, event.minerals_used_active_forces, 
                                event.minerals_lost, event.vespene_current, event.vespene_collection_rate, 
                                event.vespene_used_in_progress, event.vespene_used_current, event.vespene_used_active_forces,
                                event.vespene_lost])
					if replay.players[1].pid == event.pid and replay.players[1].pick_race[0] == 'T':
						T_gang.append([counter, event.second, replay.players[1].result, event.player, replay.players[0].pick_race[0], event.workers_active_count,
                                event.food_used, event.food_made, event.minerals_current, event.minerals_collection_rate, 
                                event.minerals_used_in_progress, event.minerals_used_current, event.minerals_used_active_forces, 
                                event.minerals_lost, event.vespene_current, event.vespene_collection_rate, 
                                event.vespene_used_in_progress, event.vespene_used_current, event.vespene_used_active_forces,
                                event.vespene_lost])

				if type(event) is UnitBornEvent:
					if replay.players[0].pid == event.control_pid and replay.players[0].pick_race[0] == 'T':
						print(event.unit_id)
					if replay.players[1].pid == event.control_pid and replay.players[1].pick_race[0] == 'T':
						print(event.unit_id)

				
		counter+=1

T_gang = pd.DataFrame(T_gang)
pd.set_option("display.max_rows", None, "display.max_columns", None)
T_gang.columns = ["Match ID", "Second", "Result", "Player", "Race", "Current Workers", "Food Used", "Food Available",
                    "Current Minerals", "Minerals Collection Rate", "Minerals Used in Progress", "Minerals Used", 
                    "Minerals Used Active Forces", "Minerals Lost", "Current Vespene", "Vespene Collection Rate", 
                    "Vespene Used in Progress", "Vespene Used", "Vespene Used Active Forces", "Vespene Lost"]
T_gang.to_csv(r'C:\Users\tluka\Desktop\data.csv', index=False)
