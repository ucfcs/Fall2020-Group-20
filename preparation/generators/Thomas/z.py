import sc2reader
from sc2reader.engine.plugins import APMTracker, ContextLoader, SelectionTracker
from sc2reader import data
from sc2reader.events import *
import os,glob
import pandas as pd
import json

counter = 0;
path = "C:/Users/tluka/Desktop/HSC XIII Replay Pack"
os.chdir(path)

unit_data = json.loads(data.unit_data)
unit_map = {}
df = []
ZergArray = []
id_list = []

for k in unit_data:
    unit_map[k] = list(unit_data[k].keys())

zerg_dict = {
'baneling': 0, 'banelingnest': 0, 'broodling': 0,'broodlingescort': 0,
'changeling': 0,'corruptor': 0,'creeptumor': 0,'drone': 0,'evolutionchamber': 0,
'extractor': 0, 'greaterspire': 0, 'hatchery': 0,'hive': 0,'hydralisk': 0, 
'hydraliskden': 0,'infestationpit': 0, 'infestor': 0, 'lair': 0, 'locust': 0, 'mutalisk':0, 
'nydusnetwork': 0, 'nydusworm': 0, 'overlord': 0, 'queen': 0, 
'roach': 0, 'roachwarren': 0,'spawningpool': 0, 'spinecrawler': 0, 
'spire': 0, 'sporecrawler': 0, 'swarmhost': 0,
'ultralisk': 0, 'ultraliskcavern': 0, 'viper': 0, 'zergling': 0,
} 

for replay in sc2reader.load_replays(glob.glob('../**/*.SC2Replay', recursive=True)):
	print(replay.players)
	if replay.players[0].pick_race[0] == 'Z' or replay.players[1].pick_race[0] == 'Z':
		unitDictionary = dict.fromkeys(zerg_dict,0)
		unitDictionary2 = dict.fromkeys(zerg_dict,0)
		id_list.clear()
		
		for event in replay.events:
			if event.second %30 == 0:
				if type(event) is PlayerStatsEvent:
					if replay.players[0].pid == event.pid and replay.players[0].pick_race[0] == 'Z':

						ZergArray.append([counter, event.second, replay.players[0].result, event.player, replay.players[0].pid, replay.players[0].pick_race[0], event.workers_active_count,
                                event.food_used, event.food_made, event.minerals_current, event.minerals_collection_rate, 
                                event.minerals_used_in_progress, event.minerals_used_current, event.minerals_used_active_forces, 
                                event.minerals_lost, event.vespene_current, event.vespene_collection_rate, 
                                event.vespene_used_in_progress, event.vespene_used_current, event.vespene_used_active_forces,
                                event.vespene_lost, unitDictionary['baneling'],unitDictionary['banelingnest'], unitDictionary['broodling'], unitDictionary['broodlingescort'],
                                unitDictionary['changeling'], unitDictionary['corruptor'],unitDictionary['creeptumor'],unitDictionary['drone'], 
                                unitDictionary['evolutionchamber'], unitDictionary['extractor'], unitDictionary['greaterspire'], unitDictionary['hatchery'], unitDictionary['hive'], unitDictionary['hydralisk'], 
                                unitDictionary['hydraliskden'], unitDictionary['infestationpit'], unitDictionary['infestor'], unitDictionary['lair'], 
                                unitDictionary['locust'], unitDictionary['mutalisk'], unitDictionary['nydusnetwork'], unitDictionary['nydusworm'], unitDictionary['overlord'],
                                unitDictionary['queen'], unitDictionary['roach'],  unitDictionary['roachwarren'], 
                                unitDictionary['spawningpool'], unitDictionary['spinecrawler'],unitDictionary['spire'], unitDictionary['sporecrawler'], 
                                unitDictionary['swarmhost'], unitDictionary['ultralisk'], unitDictionary['ultraliskcavern'], unitDictionary['viper'], unitDictionary['zergling']])

					if replay.players[1].pid == event.pid and replay.players[1].pick_race[0] == 'Z':
						ZergArray.append([counter, event.second, replay.players[1].result, event.player, replay.players[1].pid, replay.players[1].pick_race[0], event.workers_active_count,
                                event.food_used, event.food_made, event.minerals_current, event.minerals_collection_rate, 
                                event.minerals_used_in_progress, event.minerals_used_current, event.minerals_used_active_forces, 
                                event.minerals_lost, event.vespene_current, event.vespene_collection_rate, 
                                event.vespene_used_in_progress, event.vespene_used_current, event.vespene_used_active_forces,
                                event.vespene_lost, unitDictionary2['baneling'],unitDictionary2['banelingnest'], unitDictionary2['broodling'], unitDictionary2['broodlingescort'],
                                unitDictionary2['changeling'], unitDictionary2['corruptor'],unitDictionary2['creeptumor'],unitDictionary2['drone'], 
                                unitDictionary2['evolutionchamber'], unitDictionary2['extractor'], unitDictionary2['greaterspire'], unitDictionary2['hatchery'], unitDictionary2['hive'], unitDictionary2['hydralisk'], 
                                unitDictionary2['hydraliskden'], unitDictionary2['infestationpit'], unitDictionary2['infestor'], unitDictionary2['lair'], 
                                unitDictionary2['locust'], unitDictionary2['mutalisk'], unitDictionary2['nydusnetwork'], unitDictionary2['nydusworm'], unitDictionary2['overlord'],
                                unitDictionary2['queen'], unitDictionary2['roach'],  unitDictionary2['roachwarren'], 
                                unitDictionary2['spawningpool'], unitDictionary2['spinecrawler'], unitDictionary2['spire'], unitDictionary2['sporecrawler'],
                                unitDictionary2['swarmhost'], unitDictionary2['ultralisk'], unitDictionary2['ultraliskcavern'], unitDictionary2['viper'], unitDictionary2['zergling']])


			if type(event) is UnitBornEvent:
				if replay.players[0].pid == event.control_pid and replay.players[0].pick_race[0] == 'Z':
					if event.unit_type_name.lower() in unitDictionary:
						if event.unit_id not in id_list:
							id_list.append(event.unit_id)
							unitDictionary[event.unit_type_name.lower()] +=1
					elif event.unit.name.lower() in unitDictionary:
						if event.unit_id not in id_list:
							id_list.append(event.unit_id)
							unitDictionary[event.unit.name.lower()] +=1
		
				if replay.players[1].pid == event.control_pid and replay.players[1].pick_race[0] == 'Z':
					if event.unit_type_name.lower() in unitDictionary:
						if event.unit_id not in id_list:
							id_list.append(event.unit_id)
							unitDictionary2[event.unit_type_name.lower()] +=1
					elif event.unit.name.lower() in unitDictionary:
						if event.unit_id not in id_list:
							id_list.append(event.unit_id)
							unitDictionary2[event.unit.name.lower()] +=1

			if type(event) is UnitTypeChangeEvent:
				if replay.players[0] == event.unit.owner and replay.players[0].pick_race[0] == 'Z':
					if event.unit_type_name.lower() == 'lair':
						if event.unit_id in id_list:
							unitDictionary[event.unit_type_name.lower()] +=1
					elif event.unit_type_name.lower() == 'hive':
						print(event)
						if event.unit_id in id_list:
							unitDictionary[event.unit_type_name.lower()] +=1
					elif event.unit_type_name.lower() == 'greaterspire':
						if event.unit_id in id_list:
							unitDictionary[event.unit_type_name.lower()] +=1
				if replay.players[1].pid == event.unit.owner and replay.players[1].pick_race[0] == 'Z':
					if event.unit_type_name.lower() == 'lair':
						if event.unit_id in id_list:
							unitDictionary2[event.unit_type_name.lower()] +=1
					elif event.unit_type_name.lower() == 'hive':
						print(event)
						if event.unit_id in id_list:
							unitDictionary2[event.unit_type_name.lower()] +=1
					elif event.unit_type_name.lower() == 'greaterspire':
						if event.unit_id in id_list:
							unitDictionary2[event.unit_type_name.lower()] +=1


			if type(event) is UnitDiedEvent:
				if replay.players[0] == event.unit.owner and  replay.players[0].pick_race[0] == 'Z':
					#print(event)
					if event.unit.name.lower() in unitDictionary:
						if event.unit.name.lower() == 'hive':
							print(event)
						if event.unit_id in id_list:
							id_list.remove(event.unit_id)
							unitDictionary[event.unit.name.lower()] -=1
					elif event.unit.name.lower() == 'spinecrawleruprooted':
						if event.unit_id in id_list:
							id_list.remove(event.unit_id)
							unitDictionary['spinecrawler']-=1
					elif event.unit.name.lower() == 'zerglingburrowed':
						if event.unit_id in id_list:
						    id_list.remove(event.unit_id)
						    unitDictionary['zergling'] -=1
					elif event.unit.name.lower() == 'banelingburrowed':
						if event.unit_id in id_list:
							id_list.remove(event.unit_id)
							unitDictionary['baneling'] -=1
					elif event.unit.name.lower() == 'creeptumorburrowed':
						if event.unit_id in id_list:
							id_list.remove(event.unit_id)
							unitDictionary['creeptumor'] -=1
					elif event.unit.name.lower() == 'droneburrowed':
						if event.unit_id in id_list:
							id_list.remove(event.unit_id)
							unitDictionary['droneburrowed'] -=1
					elif event.unit.name.lower() == 'hydraliskburrowed':
						if event.unit_id in id_list:
							id_list.remove(event.unit_id)
							unitDictionary['hydralisk'] -=1
					elif event.unit.name.lower() == 'infestorburrowed':
						if event.unit_id in id_list:
							id_list.remove(event.unit_id)
							unitDictionary['infestor'] -=1
					elif event.unit.name.lower() == 'swarmhostburrowed':
						if event.unit_id in id_list:
							id_list.remove(event.unit_id)
							unitDictionary['swarmhost'] -=1
					elif event.unit.name.lower() == 'ultraliskburrowed':
							if event.unit_id in id_list:
								id_list.remove(event.unit_id)
								unitDictionary['ultralisk'] -=1



				if replay.players[1]== event.unit.owner and  replay.players[1].pick_race[0] == 'Z':
					if event.unit.name.lower() in unitDictionary2:
						if event.unit.name.lower() == 'hive':
							print(event)
						if event.unit_id in id_list:
							id_list.remove(event.unit_id)
							unitDictionary2[event.unit.name.lower()] -=1
					elif event.unit.name.lower() == 'spinecrawleruprooted':
						if event.unit_id in id_list:
							id_list.remove(event.unit_id)
							unitDictionary2['spinecrawler'] -=1
					elif event.unit.name.lower() == 'zerglingburrowed':
						if event.unit_id in id_list:
						    id_list.remove(event.unit_id)
						    unitDictionary2['zergling'] -=1
					elif event.unit.name.lower() == 'banelingburrowed':
						if event.unit_id in id_list:
							id_list.remove(event.unit_id)
							unitDictionary2['baneling'] -=1
					elif event.unit.name.lower() == 'creeptumorburrowed':
						if event.unit_id in id_list:
							id_list.remove(event.unit_id)
							unitDictionary2['creeptumor'] -=1
					elif event.unit.name.lower() == 'droneburrowed':
						if event.unit_id in id_list:
							id_list.remove(event.unit_id)
							unitDictionary2['droneburrowed'] -=1
					elif event.unit.name.lower() == 'hydraliskburrowed':
						if event.unit_id in id_list:
							id_list.remove(event.unit_id)
							unitDictionary2['hydralisk'] -=1
					elif event.unit.name.lower() == 'infestorburrowed':
						if event.unit_id in id_list:
							id_list.remove(event.unit_id)
							unitDictionary2['infestor'] -=1
					elif event.unit.name.lower() == 'swarmhostburrowed':
						if event.unit_id in id_list:
							id_list.remove(event.unit_id)
							unitDictionary2['swarmhost'] -=1
					elif event.unit.name.lower() == 'ultraliskburrowed':
						if event.unit_id in id_list:
							id_list.remove(event.unit_id)
							unitDictionary2['ultralisk'] -=1

			if type(event) is UnitInitEvent:
				if replay.players[0].pid == event.control_pid and replay.players[0].pick_race[0] == 'Z':
					if event.unit_type_name.lower() in unitDictionary:
						#print(event)
						if event.unit_id not in id_list:
							id_list.append(event.unit_id)
							unitDictionary[event.unit_type_name.lower()] +=1
				
				if replay.players[1].pid == event.control_pid and replay.players[1].pick_race[0] == 'Z':
					if event.unit_type_name.lower() in unitDictionary2:
						if event.unit_id not in id_list:
							id_list.append(event.unit_id)
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
