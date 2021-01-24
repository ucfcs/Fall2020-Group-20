import sc2reader
from sc2reader.engine.plugins import APMTracker, ContextLoader, SelectionTracker
from sc2reader import data
from sc2reader.events import *
import glob,os
import pandas as pd
import json

pd.set_option("display.max_rows", None, "display.max_columns", None)


# %%
#PvP matchups
path = "C:/Users/tluka/Desktop/HSC XIII Replay Pack"
os.chdir(path)
matsPP = []
pp = -1;
id_list = []

protoss_dict = {'adept': 0,'archon': 0, 'assimilator': 0, 'carrier': 0, 'colossus': 0, 'cyberneticscore': 0, 
                'darkshrine': 0, 'darktemplar': 0, 'disruptor': 0, 'fleetbeacon': 0, 'forge': 0, 'gateway': 0, 
                'hightemplar': 0, 'immortal': 0, 'interceptor': 0, 'mothership': 0, 'mothershipcore': 0, 'nexus': 0, 
                'observer': 0, 'oracle': 0, 'phoenix': 0, 'photoncannon': 0, 'probe': 0, 'pylon': 0, 'reactor': 0, 
                'roboticsbay': 0, 'roboticsfacility': 0, 'sentry': 0, 'shieldbattery': 0, 'stalker': 0, 'stargate': 0, 
                'tempest': 0, 'templararchive': 0, 'twilightcouncil': 0, 'voidray': 0, 'warpgate': 0, 'warpprism': 0, 
                'zealot': 0}

for replay in sc2reader.load_replays(glob.glob('../**/*.SC2Replay', recursive=True)):
    if pp>100:
      break
    if replay.players[0].pick_race[0] == 'P' or replay.players[1].pick_race[0] == 'P':
        pp += 1
        print(replay.players)
        pp_dict1 = dict.fromkeys(protoss_dict,0)
        pp_dict2 = dict.fromkeys(protoss_dict,0)
        id_list.clear()
        for event in replay.events:
            #PlayerStatsEvent
            if type(event) is PlayerStatsEvent:
                if event.second % 30 == 0: 
                    #Player 1
                    if replay.players[0].pid == event.pid and replay.players[0].pick_race[0] == 'P':
                        matsPP.append([pp, event.second, replay.map_name, str(replay.game_length), replay.players[0].result,
                                       event.player, replay.players[0].pid, replay.players[0].pick_race[0], 
                                       event.workers_active_count,event.food_used, event.food_made, 
                                       event.minerals_current, event.minerals_collection_rate, event.minerals_used_in_progress, 
                                       event.minerals_used_current, event.minerals_used_active_forces, event.minerals_lost, 
                                       event.vespene_current, event.vespene_collection_rate, event.vespene_used_in_progress, 
                                       event.vespene_used_current, event.vespene_used_active_forces,event.vespene_lost, 
                                       pp_dict1['adept'], pp_dict1['archon'], pp_dict1['assimilator'], pp_dict1['carrier'], 
                                       pp_dict1['colossus'], pp_dict1['cyberneticscore'], pp_dict1['darkshrine'], 
                                       pp_dict1['darktemplar'], pp_dict1['disruptor'], pp_dict1['fleetbeacon'], 
                                       pp_dict1['forge'], pp_dict1['gateway'], pp_dict1['hightemplar'], pp_dict1['immortal'], 
                                       pp_dict1['interceptor'], pp_dict1['mothership'], pp_dict1['mothershipcore'], 
                                       pp_dict1['nexus'], pp_dict1['observer'], pp_dict1['oracle'], pp_dict1['phoenix'], 
                                       pp_dict1['photoncannon'], pp_dict1['probe'], pp_dict1['pylon'], pp_dict1['reactor'], 
                                       pp_dict1['roboticsbay'], pp_dict1['roboticsfacility'], pp_dict1['sentry'], pp_dict1['shieldbattery'],
                                       pp_dict1['stalker'], pp_dict1['stargate'], pp_dict1['tempest'], pp_dict1['templararchive'], 
                                       pp_dict1['twilightcouncil'], pp_dict1['voidray'], pp_dict1['warpgate'], 
                                       pp_dict1['warpprism'], pp_dict1['zealot']])

                    #Player 2
                    if replay.players[1].pid == event.pid and replay.players[1].pick_race[0] == 'P':
                        matsPP.append([pp, event.second, replay.map_name, str(replay.game_length), replay.players[1].result,
                                       event.player, replay.players[1].pid, replay.players[1].pick_race[0], 
                                       event.workers_active_count,event.food_used, event.food_made, 
                                       event.minerals_current, event.minerals_collection_rate, event.minerals_used_in_progress, 
                                       event.minerals_used_current, event.minerals_used_active_forces, event.minerals_lost, 
                                       event.vespene_current, event.vespene_collection_rate, event.vespene_used_in_progress, 
                                       event.vespene_used_current, event.vespene_used_active_forces,event.vespene_lost, 
                                       pp_dict2['adept'], pp_dict2['archon'], pp_dict2['assimilator'], pp_dict2['carrier'], 
                                       pp_dict2['colossus'], pp_dict2['cyberneticscore'], pp_dict2['darkshrine'], 
                                       pp_dict2['darktemplar'], pp_dict2['disruptor'], pp_dict2['fleetbeacon'], 
                                       pp_dict2['forge'], pp_dict2['gateway'], pp_dict2['hightemplar'], pp_dict2['immortal'], 
                                       pp_dict2['interceptor'], pp_dict2['mothership'], pp_dict2['mothershipcore'], 
                                       pp_dict2['nexus'], pp_dict2['observer'], pp_dict2['oracle'], pp_dict2['phoenix'], 
                                       pp_dict2['photoncannon'], pp_dict2['probe'], pp_dict2['pylon'], pp_dict2['reactor'], 
                                       pp_dict2['roboticsbay'], pp_dict2['roboticsfacility'], pp_dict2['sentry'], pp_dict2['shieldbattery'],
                                       pp_dict2['stalker'], pp_dict2['stargate'], pp_dict2['tempest'], pp_dict2['templararchive'], 
                                       pp_dict2['twilightcouncil'], pp_dict2['voidray'], pp_dict2['warpgate'], 
                                       pp_dict2['warpprism'], pp_dict2['zealot']])

            #UnitBornEvent
            if type(event) is UnitBornEvent:
                if replay.players[0].pid == event.control_pid and replay.players[0].pick_race[0] == 'P':
                    if event.unit.name.lower() in pp_dict1:
                      if event.unit_id not in id_list:
                        id_list.append(event.unit_id)
                        pp_dict1[event.unit.name.lower()] +=1
                    elif event.unit_type_name.lower() in pp_dict1:
                      if event.unit_id not in id_list:
                        id_list.append(event.unit_id)
                        pp_dict1[event.unit_type_name.lower()] +=1
                    elif event.unit_type_name.lower() == 'warpprismphasing':
                      if event.unit_id not in id_list:
                         id_list.append(event.unit_id)
                         pp_dict1['warpprism'] +=1
                
            #Player 2's unit born
                if replay.players[1].pid == event.control_pid and replay.players[1].pick_race[0] == 'P':
                    if event.unit_type_name.lower() in pp_dict2:
                      if event.unit_id not in id_list:
                         id_list.append(event.unit_id)
                         pp_dict2[event.unit_type_name.lower()] +=1
                    elif event.unit_type_name.lower() in pp_dict2:
                      if event.unit_id not in id_list:
                         id_list.append(event.unit_id)
                         pp_dict2[event.unit_type_name.lower()] +=1
                    elif event.unit_type_name.lower() == 'warpprismphasing':
                      if event.unit_id not in id_list:
                         id_list.append(event.unit_id)
                         pp_dict2['warpprism'] +=1
                    
                   
            #UnitDiedEvent
            if type(event) is UnitDiedEvent:
                if replay.players[0] == event.unit.owner and  replay.players[0].pick_race[0] == 'P':
                  if event.unit.name.lower() in pp_dict1:
                     if event.unit_id in id_list:
                         id_list.remove(event.unit_id)
                         pp_dict1[event.unit.name.lower()] -=1
                  elif event.unit.name.lower() == 'warpprismphasing':
                    if event.unit_id in id_list:
                         id_list.remove(event.unit_id)
                         pp_dict1['warpprism'] -=1
                  elif event.unit.name.lower() == 'observersiegemode':
                    if event.unit_id in id_list:
                         id_list.remove(event.unit_id)
                         pp_dict1['observer'] -=1
                  elif event.unit.name.lower() == 'pylonovercharged':
                    if event.unit_id in id_list:
                         id_list.remove(event.unit_id)
                         pp_dict1['pylon'] -=1
                  
                    
                if replay.players[1] == event.unit.owner and  replay.players[1].pick_race[0] == 'P':
                    if event.unit.name.lower() in pp_dict2:
                      if event.unit_id in id_list:
                         id_list.remove(event.unit_id)
                         pp_dict2[event.unit.name.lower()] -=1
                    elif event.unit.name.lower() == 'warpprismphasing':
                      if event.unit_id in id_list:
                         id_list.remove(event.unit_id)
                         pp_dict2['warpprism'] -=1
                    elif event.unit.name.lower() == 'observersiegemode':
                      if event.unit_id in id_list:
                         id_list.remove(event.unit_id)
                         pp_dict2['observer'] -=1
                    elif event.unit.name.lower() == 'pylonovercharged':
                      if event.unit_id in id_list:
                         id_list.remove(event.unit_id)
                         pp_dict2['pylon'] -=1
                    
            #UnitInitEvent            
            if type(event) is UnitInitEvent:
                #Player 1
                if replay.players[0].pid == event.control_pid and replay.players[0].pick_race[0] == 'P':
                    if event.unit.name.lower() in pp_dict1:
                       if event.unit_id not in id_list:
                         id_list.append(event.unit_id)
                         pp_dict1[event.unit.name.lower()] +=1
                    elif event.unit_type_name.lower() in pp_dict1:
                       if event.unit_id not in id_list:
                         id_list.append(event.unit_id)
                         pp_dict1[event.unit_type_name.lower()]+=1
                    else:
                      print(event)

                #Player 2
                if replay.players[1].pid == event.control_pid and replay.players[1].pick_race[0] == 'P':
                    if event.unit.name.lower() in pp_dict2:
                        pp_dict2[event.unit.name.lower()] +=1
                    elif event.unit_type_name.lower() in pp_dict2:
                        pp_dict2[event.unit_type_name.lower()]+=1
                    else:
                      print(event)


matsPP_df = pd.DataFrame(matsPP)
columns =  ["Match ID", "Second", "Map", "Game Length", "Result", "Player", "Player#", "Race", "Current Workers", 
            "Food Used", "Food Available", "Current Minerals", "Minerals Collection Rate", "Minerals Used in Progress", 
            "Minerals Used", "Minerals Used Active Forces", "Minerals Lost", "Current Vespene", "Vespene Collection Rate", 
            "Vespene Used in Progress", "Vespene Used", "Vespene Used Active Forces", "Vespene Lost",]
columns.extend(protoss_dict.keys())
matsPP_df.columns = columns
#print(matsPP_df)
matsPP_df.to_csv(r'C:\Users\tluka\Desktop\Pdata.csv', index=False)    


