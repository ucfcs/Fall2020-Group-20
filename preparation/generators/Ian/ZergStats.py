import sc2reader
from sc2reader.engine.plugins import APMTracker, ContextLoader, SelectionTracker
from sc2reader import data
from sc2reader.events import *
import os,glob
import pandas as pd
import json

counter = 0;
path = "C:/Users/iplea/Desktop/HSC19"
os.chdir(path)

unit_data = json.loads(data.unit_data)
unit_map = {}
df = []
ZergArray = []

for k in unit_data:
    unit_map[k] = list(unit_data[k].keys())

unitDictionary = dict.fromkeys(unit_map['Zerg'],0)

for replay in sc2reader.load_replays(glob.glob('../**/*.SC2Replay', recursive=True)):
	if counter > 10:
		break
	if replay.players[0].pick_race[0] == 'Z' or replay.players[1].pick_race[0] == 'Z':
		unitDictionary = dict.fromkeys(unit_map['Zerg'],0)
		unitDictionary2 = dict.fromkeys(unit_map['Zerg'],0)
		
		for event in replay.events:
			if event.second %30 == 0:
				if type(event) is PlayerStatsEvent:
					if replay.players[0].pid == event.pid and replay.players[0].pick_race[0] == 'Z':

						ZergArray.append([counter, event.second, replay.players[0].result, event.player, replay.players[0].pid, replay.players[0].pick_race[0], event.workers_active_count,
                                event.food_used, event.food_made, event.minerals_current, event.minerals_collection_rate, 
                                event.minerals_used_in_progress, event.minerals_used_current, event.minerals_used_active_forces, 
                                event.minerals_lost, event.vespene_current, event.vespene_collection_rate, 
                                event.vespene_used_in_progress, event.vespene_used_current, event.vespene_used_active_forces,
                                event.vespene_lost, unitDictionary['baneling'],unitDictionary['banelingburrowed'],unitDictionary['banelingcocoon'],unitDictionary['banelingnest'],unitDictionary['broodlord'],
                                unitDictionary['broodlordcocoon'],unitDictionary['corruptor'],unitDictionary['creeptumor'],unitDictionary['creeptumorburrowed'],unitDictionary['drone'],unitDictionary['droneburrowed'],
                                unitDictionary['evolutionchamber'], unitDictionary['extractor'], unitDictionary['greaterspire'], unitDictionary['hatchery'], unitDictionary['hive'], unitDictionary['hydralisk'], 
                                unitDictionary['hydraliskburrowed'], unitDictionary['hydraliskden'], unitDictionary['infestationpit'], unitDictionary['infestor'], unitDictionary['infestorburrowed'], unitDictionary['lair'], 
                                unitDictionary['locust'], unitDictionary['mutalisk'], unitDictionary['nydusnetwork'], unitDictionary['nydusworm'], unitDictionary['overlord'], unitDictionary['overseer'], 
                                unitDictionary['overseercocoon'], unitDictionary['queen'], unitDictionary['queenburrowed'], unitDictionary['roach'], unitDictionary['roachburrowed'], unitDictionary['roachwarren'], 
                                unitDictionary['spawningpool'], unitDictionary['spinecrawler'], unitDictionary['spinecrawleruprooted'], unitDictionary['spire'], unitDictionary['sporecrawler'], unitDictionary['sporecrawleruprooted'], 
                                unitDictionary['swarmhost'], unitDictionary['swarmhostburrowed'], unitDictionary['ultralisk'], unitDictionary['ultraliskburrowed'], unitDictionary['ultraliskcavern'], unitDictionary['viper'], unitDictionary['zergling'], 
                                unitDictionary['zerglingburrowed']])

					if replay.players[1].pid == event.pid and replay.players[1].pick_race[0] == 'Z':
						ZergArray.append([counter, event.second, replay.players[1].result, event.player, replay.players[1].pid, replay.players[1].pick_race[0], event.workers_active_count,
                                event.food_used, event.food_made, event.minerals_current, event.minerals_collection_rate, 
                                event.minerals_used_in_progress, event.minerals_used_current, event.minerals_used_active_forces, 
                                event.minerals_lost, event.vespene_current, event.vespene_collection_rate, 
                                event.vespene_used_in_progress, event.vespene_used_current, event.vespene_used_active_forces,
                                event.vespene_lost, unitDictionary['baneling'],unitDictionary['banelingburrowed'],unitDictionary['banelingcocoon'],unitDictionary['banelingnest'],unitDictionary['broodlord'],
                                unitDictionary['broodlordcocoon'],unitDictionary['corruptor'],unitDictionary['creeptumor'],unitDictionary['creeptumorburrowed'],unitDictionary['drone'],unitDictionary['droneburrowed'],
                                unitDictionary['evolutionchamber'], unitDictionary['extractor'], unitDictionary['greaterspire'], unitDictionary['hatchery'], unitDictionary['hive'], unitDictionary['hydralisk'], 
                                unitDictionary['hydraliskburrowed'], unitDictionary['hydraliskden'], unitDictionary['infestationpit'], unitDictionary['infestor'], unitDictionary['infestorburrowed'], unitDictionary['lair'], 
                                unitDictionary['locust'], unitDictionary['mutalisk'], unitDictionary['nydusnetwork'], unitDictionary['nydusworm'], unitDictionary['overlord'], unitDictionary['overseer'], 
                                unitDictionary['overseercocoon'], unitDictionary['queen'], unitDictionary['queenburrowed'], unitDictionary['roach'], unitDictionary['roachburrowed'], unitDictionary['roachwarren'], 
                                unitDictionary['spawningpool'], unitDictionary['spinecrawler'], unitDictionary['spinecrawleruprooted'], unitDictionary['spire'], unitDictionary['sporecrawler'], unitDictionary['sporecrawleruprooted'], 
                                unitDictionary['swarmhost'], unitDictionary['swarmhostburrowed'], unitDictionary['ultralisk'], unitDictionary['ultraliskburrowed'], unitDictionary['ultraliskcavern'], unitDictionary['viper'], unitDictionary['zergling'], 
                                unitDictionary['zerglingburrowed']])


			if type(event) is UnitBornEvent:
				if replay.players[0].pid == event.control_pid and replay.players[0].pick_race[0] == 'Z':
					if event.unit_type_name.lower() in unitDictionary:
						unitDictionary[event.unit_type_name.lower()] +=1
					
				if replay.players[1].pid == event.control_pid and replay.players[1].pick_race[0] == 'Z':
					if event.unit_type_name.lower() in unitDictionary2:
						unitDictionary2[event.unit_type_name.lower()] +=1
					

			if type(event) is UnitTypeChangeEvent:
				if replay.players[0] == event.unit.owner and replay.players[0].pick_race[0] == 'Z':
					if event.unit_type_name.lower() in unitDictionary:
						unitDictionary[event.unit_type_name.lower()] +=1
				if replay.players[1].pid == event.unit.owner and replay.players[1].pick_race[0] == 'Z':
					if event.unit_type_name.lower() in unitDictionary2:
						unitDictionary2[event.unit_type_name.lower()] +=1

			if type(event) is UnitDiedEvent:
				if replay.players[0].pid != event.killing_player_id and  replay.players[0].pick_race[0] == 'Z':
					if event.unit.name.lower() in unitDictionary:
						unitDictionary[event.unit.name.lower()] -=1
				if replay.players[1].pid != event.killing_player_id and  replay.players[1].pick_race[0] == 'Z':
					if event.unit.name.lower() in unitDictionary2:
						unitDictionary2[event.unit.name.lower()] -=1

			if type(event) is UnitInitEvent:
				if replay.players[0].pid == event.control_pid and replay.players[0].pick_race[0] == 'Z':
					if event.unit_type_name.lower() in unitDictionary:
						unitDictionary[event.unit_type_name.lower()] +=1
				if replay.players[1].pid == event.control_pid and replay.players[1].pick_race[0] == 'Z':
					if event.unit_type_name.lower() in unitDictionary2:
						unitDictionary2[event.unit_type_name.lower()] +=1

		counter+=1

ZergArray = pd.DataFrame(ZergArray)
pd.set_option("display.max_rows", None, "display.max_columns", None)
columns =  ["Match ID", "Second", "Result", "Player", "Player#", "Race", "Current Workers", "Food Used", "Food Available",
                    "Current Minerals", "Minerals Collection Rate", "Minerals Used in Progress", "Minerals Used", 
                    "Minerals Used Active Forces", "Minerals Lost", "Current Vespene", "Vespene Collection Rate", 
                    "Vespene Used in Progress", "Vespene Used", "Vespene Used Active Forces", "Vespene Lost",]
columns.extend(unitDictionary.keys())
ZergArray.columns = columns
ZergArray.to_csv(r'C:\Users\tluka\Desktop\data.csv', index=False)
