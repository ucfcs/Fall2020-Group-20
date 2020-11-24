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
T_gang = []

for k in unit_data:
    unit_map[k] = list(unit_data[k].keys())

terran_dict = {'armory': 0, 'autoturret': 0, 'banshee': 0, 'barracks': 0, 'barrackstechlab': 0, 
'barracksreactor': 0, 'battlecruiser': 0,'bunker': 0,'commandcenter': 0,'cyclone': 0, 'engineeringbay': 0, 'factory': 0,
'factoryreactor': 0, 'factorytechlab': 0, 'fusioncore': 0, 'ghost': 0, 
'ghostacademy': 0, 'hellion': 0, 'liberator': 0,'marauder': 0, 'marine': 0, 'medivac': 0, 'missileturret': 0, 
'mule': 0, 'nuke':0, 'orbitalcommand': 0, 'planetaryfortress': 0, 'raven': 0, 'reactor':0,
'reaper': 0, 'refinery': 0, 'scv': 0, 'sensortower': 0, 'siegetank': 0, 'starport': 0, 
'starportreactor': 0, 'starporttechlab': 0, 'supplydepot': 0, 
'techlab': 0, 'thor': 0, 'viking': 0, 'warhound': 0, 'widowmine': 0}

for replay in sc2reader.load_replays(glob.glob('../**/*.SC2Replay', recursive=True)):
	if replay.players[0].pick_race[0] == 'T' or replay.players[1].pick_race[0] == 'T':
		pt_dict = dict.fromkeys(terran_dict,0)
		pt_dict2 = dict.fromkeys(terran_dict,0)
		
		for event in replay.events:
			if event.second %30 == 0:
				if type(event) is PlayerStatsEvent:
					if replay.players[0].pid == event.pid and replay.players[0].pick_race[0] == 'T':

						T_gang.append([counter, event.second, replay.players[0].result, event.player, replay.players[0].pid, replay.players[0].pick_race[0], event.workers_active_count,
                                event.food_used, event.food_made, event.minerals_current, event.minerals_collection_rate, 
                                event.minerals_used_in_progress, event.minerals_used_current, event.minerals_used_active_forces, 
                                event.minerals_lost, event.vespene_current, event.vespene_collection_rate, 
                                event.vespene_used_in_progress, event.vespene_used_current, event.vespene_used_active_forces,
                                event.vespene_lost, pt_dict['armory'], pt_dict['autoturret'], pt_dict['banshee'], pt_dict['barracks'], pt_dict['barrackstechlab'],
                                pt_dict['barracksreactor'], pt_dict['battlecruiser'], pt_dict['bunker'], pt_dict['commandcenter'],
                                pt_dict['cyclone'], pt_dict['engineeringbay'], pt_dict['factory'], pt_dict['factoryreactor'], pt_dict['factorytechlab'], pt_dict['fusioncore'],
                                pt_dict['ghost'], pt_dict['ghostacademy'], pt_dict['hellion'], pt_dict['liberator'],pt_dict['marauder'], pt_dict['marine'], pt_dict['medivac'],
                                pt_dict['missileturret'], pt_dict['mule'], pt_dict['nuke'],pt_dict['orbitalcommand'], pt_dict['planetaryfortress'], pt_dict['raven'], pt_dict['reactor'],
                                pt_dict['reaper'], pt_dict['refinery'], pt_dict['scv'], pt_dict['sensortower'], pt_dict['siegetank'],
                                pt_dict['starport'], pt_dict['starportreactor'], pt_dict['starporttechlab'], pt_dict['supplydepot'], pt_dict['techlab'], pt_dict['thor'],
                                pt_dict['viking'], pt_dict['warhound'], pt_dict['widowmine']])

					if replay.players[1].pid == event.pid and replay.players[1].pick_race[0] == 'T':
						T_gang.append([counter, event.second, replay.players[1].result, event.player, replay.players[1].pid, replay.players[1].pick_race[0], event.workers_active_count,
                                event.food_used, event.food_made, event.minerals_current, event.minerals_collection_rate, 
                                event.minerals_used_in_progress, event.minerals_used_current, event.minerals_used_active_forces, 
                                event.minerals_lost, event.vespene_current, event.vespene_collection_rate, 
                                event.vespene_used_in_progress, event.vespene_used_current, event.vespene_used_active_forces,
                                event.vespene_lost, pt_dict2['armory'], pt_dict2['autoturret'], pt_dict2['banshee'], pt_dict2['barracks'], pt_dict2['barrackstechlab'],
                                pt_dict2['barracksreactor'], pt_dict2['battlecruiser'], pt_dict2['bunker'], pt_dict2['commandcenter'],
                                pt_dict2['cyclone'], pt_dict2['engineeringbay'], pt_dict2['factory'], pt_dict2['factoryreactor'], pt_dict2['factorytechlab'], pt_dict2['fusioncore'],
                                pt_dict2['ghost'], pt_dict2['ghostacademy'], pt_dict2['hellion'], pt_dict2['liberator'],pt_dict2['marauder'], pt_dict2['marine'], pt_dict2['medivac'],
                                pt_dict2['missileturret'], pt_dict2['mule'], pt_dict2['nuke'], pt_dict2['orbitalcommand'], pt_dict2['planetaryfortress'], pt_dict2['raven'], pt_dict2['reactor'],
                                pt_dict2['reaper'], pt_dict2['refinery'], pt_dict2['scv'], pt_dict2['sensortower'], pt_dict2['siegetank'],
                                pt_dict2['starport'], pt_dict2['starportreactor'], pt_dict2['starporttechlab'], pt_dict2['supplydepot'], pt_dict2['techlab'], pt_dict2['thor'],
                                pt_dict2['viking'], pt_dict2['warhound'], pt_dict2['widowmine']])

			if type(event) is UnitBornEvent:
				if replay.players[0].pid == event.control_pid and replay.players[0].pick_race[0] == 'T':
					if event.unit.name.lower() == 'orbitalcommand':
						pt_dict['orbitalcommand']+=1
						pt_dict['commandcenter']+=1
					elif event.unit.name.lower() in pt_dict:
						pt_dict[event.unit.name.lower()] +=1
					elif event.unit_type_name.lower() in pt_dict:
						pt_dict[event.unit_type_name.lower()] +=1
					elif event.unit.name.lower() == 'liberatorag':
						pt_dict['liberator']+=1
					elif event.unit.name.lower() == 'vikingassault':
						pt_dict['viking']+=1
			
				if replay.players[1].pid == event.control_pid and replay.players[1].pick_race[0] == 'T':
					if event.unit.name.lower() == 'orbitalcommand':
						pt_dict2['orbitalcommand']+=1
						pt_dict2['commandcenter']+=1
					elif event.unit.name.lower() in pt_dict2:
						pt_dict2[event.unit.name.lower()] +=1
					elif event.unit_type_name.lower() in pt_dict2:
						pt_dict2[event.unit_type_name.lower()] +=1
					elif event.unit.name.lower() == 'liberatorag':
						pt_dict2['liberator']+=1
					elif event.unit.name.lower() == 'vikingassault':
						pt_dict2['viking']+=1

			if type(event) is UnitDiedEvent:
				if replay.players[0] == event.unit.owner and  replay.players[0].pick_race[0] == 'T':
					if event.unit.name.lower() == 'orbitalcommand':
						pt_dict['orbitalcommand']-=1
						pt_dict['commandcenter']-=1
					elif event.unit.name.lower() in pt_dict:
						pt_dict[event.unit.name.lower()] -=1
					elif event.unit.name.lower() == 'liberatorag':
						pt_dict['liberator']-=1
					elif event.unit.name.lower() == 'vikingassault':
						pt_dict['viking']-=1
					elif event.unit.name.lower() == 'siegetanksieged':
						pt_dict['siegetank']-=1
					elif event.unit.name.lower() == 'widowmineburrowed':
						pt_dict['widowmine']-=1
					elif event.unit.name.lower() == 'battlehellion':
						pt_dict['hellion']-=1
					elif event.unit.name.lower() == 'supplydepotlowered':
						pt_dict['supplydepot']-=1
					elif event.unit.name.lower() == 'orbitalcommandflying':
						pt_dict['orbitalcommand']-=1
						pt_dict['commandcenter']-=1
					elif event.unit.name.lower() == 'commandcenterflying':
						pt_dict['commandcenter']-=1
					elif event.unit.name.lower() == 'thorap':
						pt_dict['thor']-=1
			
				if replay.players[1].pid == event.unit.owner and  replay.players[1].pick_race[0] == 'T':
					if event.unit.name.lower() == 'orbitalcommand':
						pt_dict2['orbitalcommand']-=1
						pt_dict2['commandcenter']-=1
					elif event.unit.name.lower() in pt_dict2:
						pt_dict2[event.unit.name.lower()] -=1
					elif event.unit.name.lower() == 'liberatorag':
						pt_dict2['liberator']-=1
					elif event.unit.name.lower() == 'vikingassault':
						pt_dict2['viking']-=1
					elif event.unit.name.lower() == 'siegetanksieged':
						pt_dict2['siegetank']-=1
					elif event.unit.name.lower() == 'widowmineburrowed':
						pt_dict2['widowmine']-=1
					elif event.unit.name.lower() == 'battlehellion':
						pt_dict2['hellion']-=1
					elif event.unit.name.lower() == 'supplydepotlowered':
						pt_dict2['supplydepot']-=1
					elif event.unit.name.lower() == 'orbitalcommandflying':
						pt_dict2['orbitalcommand']-=1
						pt_dict2['commandcenter']-=1
					elif event.unit.name.lower() == 'commandcenterflying':
						pt_dict2['commandcenter']-=1
					elif event.unit.name.lower() == 'thorap':
						pt_dict2['thor']-=1

			if type(event) is UnitInitEvent:
				if replay.players[0].pid == event.control_pid and replay.players[0].pick_race[0] == 'T':
					if event.unit.name.lower() == 'orbitalcommand':
						pt_dict['orbitalcommand']+=1
						pt_dict['commandcenter']+=1
					elif event.unit.name.lower() in pt_dict:
						pt_dict[event.unit.name.lower()]+=1
					elif event.unit.name.lower() == 'supplydepotlowered':
						pt_dict['supplydepot']+=1
					
				if replay.players[1].pid == event.control_pid and replay.players[1].pick_race[0] == 'T':
					if event.unit.name.lower() == 'orbitalcommand':
						pt_dict2['orbitalcommand']+=1
						pt_dict2['commandcenter']+=1
					if event.unit.name.lower() in pt_dict2:
						pt_dict2[event.unit.name.lower()]+=1
					elif event.unit.name.lower() == 'supplydepotlowered':
						pt_dict2['supplydepot']+=1
					
				
		counter+=1

T_gang = pd.DataFrame(T_gang)
pd.set_option("display.max_rows", None, "display.max_columns", None)
columns =  ["Match ID", "Second", "Result", "Player", "Player#", "Race", "Current Workers", "Food Used", "Food Available",
                    "Current Minerals", "Minerals Collection Rate", "Minerals Used in Progress", "Minerals Used", 
                    "Minerals Used Active Forces", "Minerals Lost", "Current Vespene", "Vespene Collection Rate", 
                    "Vespene Used in Progress", "Vespene Used", "Vespene Used Active Forces", "Vespene Lost",]
columns.extend(pt_dict.keys())
T_gang.columns = columns
T_gang.to_csv(r'C:\Users\tluka\Desktop\data.csv', index=False)
