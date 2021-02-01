import sc2reader
from sc2reader.engine.plugins import APMTracker, ContextLoader, SelectionTracker
from sc2reader import data
from sc2reader.events import *
import os
import glob
import pandas as pd
import json

counter = 0
#path = "C:/Users/iplea/Desktop/HSC19"
#os.chdir(path)

unit_data = json.loads(data.unit_data)
unit_map = {}
df = []
ZergArray = []

zerg_dict = {'corruptor' : 0, 'broodlord' : 0, 'drone' : 0, 'hydralisk' : 0,'infestor' : 0, 'larva' : 0, 'mutalisk' : 0, 'overlord' : 0, 'queen' : 0, 'roach' : 0, 'ultralisk' : 0, 
'zergling' : 0, 'baneling' : 0, 'broodling' : 0, 'changeling' : 0, 'banelingnest' : 0, 'creeptumor' : 0, 'evolutionchamber' : 0, 'extractor' : 0, 'hatchery' : 0, 'lair' : 0, 
'hive' : 0, 'hydraliskden' : 0, 'infestationpit' : 0, 'nydusnetwork' : 0, 'nydusworm' : 0, 'roachwarren' : 0, 'spawningpool' : 0, 'spinecrawler' : 0, 'spire' : 0, 'greaterspire' : 0, 'sporecrawler' : 0, 
'ultraliskcavern' : 0, 'overseer' : 0, 'ravager' : 0, 'nyduscanal' : 0}



for replay in sc2reader.load_replays(glob.glob('C:/Users/iplea/Desktop/Replays/**/*.SC2Replay', recursive=True)):
    if counter > 10:
        break
    if replay.players[0].pick_race[0] == 'Z' or replay.players[1].pick_race[0] == 'Z':
        unitDictionary = dict.fromkeys(zerg_dict, 0)
        unitDictionary2 = dict.fromkeys(zerg_dict, 0)

        for event in replay.events:
            if event.second % 30 == 0:
                if type(event) is PlayerStatsEvent:
                    if replay.players[0].pid == event.pid and replay.players[0].pick_race[0] == 'Z':

                        ZergArray.append([counter, event.second, replay.players[0].result, event.player, replay.players[0].pid, replay.players[0].pick_race[0], event.workers_active_count,
                                          event.food_used, event.food_made, event.minerals_current, event.minerals_collection_rate,
                                          event.minerals_used_in_progress, event.minerals_used_current, event.minerals_used_active_forces,
                                          event.minerals_lost, event.vespene_current, event.vespene_collection_rate,
                                          event.vespene_used_in_progress, event.vespene_used_current, event.vespene_used_active_forces,
                                          event.vespene_lost, unitDictionary['corruptor'], unitDictionary['broodlord'], unitDictionary['drone'], unitDictionary['hydralisk'], unitDictionary['infestor'], 
                                          unitDictionary['larva'], unitDictionary['mutalisk'], unitDictionary['overlord'], unitDictionary['queen'], unitDictionary['roach'], 
                                          unitDictionary['ultralisk'], unitDictionary['zergling'], unitDictionary['baneling'], unitDictionary['broodling'], unitDictionary['changeling'], 
                                          unitDictionary['banelingnest'], unitDictionary['creeptumor'], unitDictionary['evolutionchamber'], unitDictionary['extractor'], 
                                          unitDictionary['hatchery'], unitDictionary['lair'], unitDictionary['hive'], unitDictionary['hydraliskden'], unitDictionary['infestationpit'], unitDictionary['nydusnetwork'], 
                                          unitDictionary['nydusworm'], unitDictionary['roachwarren'], unitDictionary['spawningpool'], unitDictionary['spinecrawler'], unitDictionary['spire'], 
                                          unitDictionary['greaterspire'], unitDictionary['sporecrawler'], unitDictionary['ultraliskcavern'], unitDictionary['overseer'], unitDictionary['ravager'], unitDictionary['nyduscanal']])

                    if replay.players[1].pid == event.pid and replay.players[1].pick_race[0] == 'Z':
                        ZergArray.append([counter, event.second, replay.players[1].result, event.player, replay.players[1].pid, replay.players[1].pick_race[0], event.workers_active_count,
                                          event.food_used, event.food_made, event.minerals_current, event.minerals_collection_rate,
                                          event.minerals_used_in_progress, event.minerals_used_current, event.minerals_used_active_forces,
                                          event.minerals_lost, event.vespene_current, event.vespene_collection_rate,
                                          event.vespene_used_in_progress, event.vespene_used_current, event.vespene_used_active_forces,
                                          event.vespene_lost, unitDictionary2['corruptor'], unitDictionary2['broodlord'], unitDictionary2['drone'], unitDictionary2['hydralisk'], unitDictionary2['infestor'], 
                                          unitDictionary2['larva'], unitDictionary2['mutalisk'], unitDictionary2['overlord'], unitDictionary2['queen'], unitDictionary2['roach'], 
                                          unitDictionary2['ultralisk'], unitDictionary2['zergling'], unitDictionary2['baneling'], unitDictionary2['broodling'], unitDictionary2['changeling'],
                                          unitDictionary2['banelingnest'], unitDictionary2['creeptumor'], unitDictionary2['evolutionchamber'], unitDictionary2['extractor'], 
                                          unitDictionary2['hatchery'], unitDictionary2['lair'], unitDictionary2['hive'], unitDictionary2['hydraliskden'], unitDictionary2['infestationpit'], unitDictionary2['nydusnetwork'], 
                                          unitDictionary2['nydusworm'], unitDictionary2['roachwarren'], unitDictionary2['spawningpool'], unitDictionary2['spinecrawler'], unitDictionary2['spire'], 
                                          unitDictionary2['greaterspire'], unitDictionary2['sporecrawler'], unitDictionary2['ultraliskcavern'], unitDictionary2['overseer'], unitDictionary2['ravager'], unitDictionary2['nyduscanal']])

            if type(event) is UnitBornEvent:
                if replay.players[0].pid == event.control_pid and replay.players[0].pick_race[0] == 'Z':
                    if event.unit.name.lower() == 'overseer':
                        unitDictionary['overseer']+=1
                    elif event.unit.name.lower() in unitDictionary:
                        unitDictionary[event.unit_type_name.lower()] += 1
                    elif event.unit_type_name.lower() in unitDictionary:
                        unitDictionary[event.unit_type_name.lower()] += 1

                    
                    

                if replay.players[1].pid == event.control_pid and replay.players[1].pick_race[0] == 'Z':
                    if event.unit.name.lower() == 'overseer':
                        unitDictionary['overseer']+=1
                    elif event.unit.name.lower() in unitDictionary2:
                        unitDictionary2[event.unit_type_name.lower()] += 1
                    elif event.unit_type_name.lower() in unitDictionary2:
                        unitDictionary2[event.unit_type_name.lower()] += 1
                    
                    


            if type(event) is UnitDiedEvent:
                if replay.players[0].pid != event.killing_player_id and replay.players[0].pick_race[0] == 'Z':
                    if event.unit.name.lower() in unitDictionary:
                        unitDictionary[event.unit.name.lower()] -= 1
           
                    
                if replay.players[1].pid != event.killing_player_id and replay.players[1].pick_race[0] == 'Z':
                    if event.unit.name.lower() in unitDictionary2:
                        unitDictionary2[event.unit.name.lower()] -= 1
                

            if type(event) is UnitInitEvent:
                if replay.players[0].pid == event.control_pid and replay.players[0].pick_race[0] == 'Z':
                    if event.unit.name.lower() in unitDictionary:
                        unitDictionary[event.unit_type_name.lower()] += 1
                    elif event.unit_type_name.lower() in unitDictionary:
                        unitDictionary[event.unit_type_name.lower()] += 1
                   
                   
                if replay.players[1].pid == event.control_pid and replay.players[1].pick_race[0] == 'Z':
                    if event.unit.name.lower() in unitDictionary2:
                        unitDictionary2[event.unit_type_name.lower()] += 1
                    elif event.unit_type_name.lower() in unitDictionary2:
                        unitDictionary2[event.unit_type_name.lower()] += 1
                  

            if type(event) is UnitTypeChangeEvent:
              #print(event.unit.name.lower())
              #print(unitDictionary['overseer'])
              if replay.players[0] == event.unit.owner and replay.players[0].pick_race[0] == 'Z':
                if event.unit.name.lower() == 'greaterspire':
                    unitDictionary['greaterspire'] +=1
                elif event.unit.name.lower() == 'greaterspire':
                    unitDictionary['greaterspire'] +=1
              if replay.players[1] == event.unit.owner and replay.players[1].pick_race[1] == 'Z':
                if event.unit.name.lower() == 'overseersiegemode':
                    unitDictionary['overseer'] +=1
                elif event.unit.name.lower() == 'overseersiegemode':
                    unitDictionary['overseer'] +=1

                

        counter += 1

ZergArray = pd.DataFrame(ZergArray)
pd.set_option("display.max_rows", None, "display.max_columns", None)
columns = ["Match ID", "Second", "Result", "Player", "Player#", "Race", "Current Workers", "Food Used", "Food Available",
           "Current Minerals", "Minerals Collection Rate", "Minerals Used in Progress", "Minerals Used",
           "Minerals Used Active Forces", "Minerals Lost", "Current Vespene", "Vespene Collection Rate",
           "Vespene Used in Progress", "Vespene Used", "Vespene Used Active Forces", "Vespene Lost", ]
columns.extend(unitDictionary.keys())
ZergArray.columns = columns
ZergArray.to_csv('C:/Users/iplea/Desktop/Zdata.csv', index=False)
