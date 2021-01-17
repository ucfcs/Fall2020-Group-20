import sc2reader
from sc2reader.engine.plugins import APMTracker, ContextLoader, SelectionTracker
from sc2reader import data
from sc2reader.events import *
import os
import glob
import pandas as pd
import json

sc2reader.engine.register_plugin(APMTracker())
sc2reader.engine.register_plugin(SelectionTracker())
sc2reader.engine.register_plugin(ContextLoader())

counter = 0

T_gang = []
id_list = []

unit_data = json.loads(data.unit_data)

unit_map = {}
for k in unit_data:
    unit_map[k] = list(unit_data[k].keys())

with open('./terran.json', 'rb') as f:
    terran_data = json.loads(f)
terran_dict = dict.fromkeys(terran_data['units'], 0)

for replay in sc2reader.load_replays(glob.glob('../**/*.SC2Replay', recursive=True)):
    # print(replay.players)
    if replay.players[0].pick_race[0] == 'T' or replay.players[1].pick_race[0] == 'T':
        matchup_dict = dict.fromkeys(terran_dict, 0)
        matchup_dict2 = dict.fromkeys(terran_dict, 0)
        id_list.clear()

        for event in replay.events:
            if event.second % 30 == 0:
                if type(event) is PlayerStatsEvent:
                    if replay.players[0].pid == event.pid and replay.players[0].pick_race[0] == 'T':

                        lower_bound = 0 if event.second == 0 else event.second-30
                        ap30s = sum(list(replay.players[0].aps.values())[
                                    lower_bound:event.second])

                        T_gang.append([
                            counter,
                            event.second,
                            replay.players[0].result,
                            event.player, ap30s, replay.players[0].pick_race[0], event.workers_active_count,
                            event.food_used, event.food_made, event.minerals_current, event.minerals_collection_rate,
                            event.minerals_used_in_progress, event.minerals_used_current, event.minerals_used_active_forces,
                            event.minerals_lost, event.vespene_current, event.vespene_collection_rate,
                            event.vespene_used_in_progress, event.vespene_used_current, event.vespene_used_active_forces,
                            event.vespene_lost, matchup_dict['armory'], matchup_dict['autoturret'], matchup_dict[
                                'banshee'], matchup_dict['barracks'], matchup_dict['barrackstechlab'],
                            matchup_dict['barracksreactor'], matchup_dict['battlecruiser'], matchup_dict['bunker'], matchup_dict['commandcenter'],
                            matchup_dict['cyclone'], matchup_dict['engineeringbay'], matchup_dict['factory'], matchup_dict[
                                'factoryreactor'], matchup_dict['factorytechlab'], matchup_dict['fusioncore'],
                            matchup_dict['ghost'], matchup_dict['ghostacademy'], matchup_dict['hellion'], matchup_dict[
                                'liberator'], matchup_dict['marauder'], matchup_dict['marine'], matchup_dict['medivac'],
                            matchup_dict['missileturret'], matchup_dict['mule'], matchup_dict['nuke'], matchup_dict[
                                'orbitalcommand'], matchup_dict['planetaryfortress'], matchup_dict['raven'], matchup_dict['reactor'],
                            matchup_dict['reaper'], matchup_dict['refinery'], matchup_dict[
                                'scv'], matchup_dict['sensortower'], matchup_dict['siegetank'],
                            matchup_dict['starport'], matchup_dict['starportreactor'], matchup_dict[
                                'starporttechlab'], matchup_dict['supplydepot'], matchup_dict['techlab'], matchup_dict['thor'],
                            matchup_dict['viking'], matchup_dict['warhound'], matchup_dict['widowmine']
                        ])

                    if replay.players[1].pid == event.pid and replay.players[1].pick_race[0] == 'T':
                        lower_bound = 0 if event.second == 0 else event.second-30
                        ap30s = sum(list(replay.players[1].aps.values())[
                                    lower_bound:event.second])

                        T_gang.append([
                            counter, event.second, replay.players[1].result, event.player, ap30s, replay.players[
                                1].pick_race[0], event.workers_active_count,
                            event.food_used, event.food_made, event.minerals_current, event.minerals_collection_rate,
                            event.minerals_used_in_progress, event.minerals_used_current, event.minerals_used_active_forces,
                            event.minerals_lost, event.vespene_current, event.vespene_collection_rate,
                            event.vespene_used_in_progress, event.vespene_used_current, event.vespene_used_active_forces,
                            event.vespene_lost, matchup_dict2['armory'], matchup_dict2['autoturret'], matchup_dict2[
                                'banshee'], matchup_dict2['barracks'], matchup_dict2['barrackstechlab'],
                            matchup_dict2['barracksreactor'], matchup_dict2[
                                'battlecruiser'], matchup_dict2['bunker'], matchup_dict2['commandcenter'],
                            matchup_dict2['cyclone'], matchup_dict2['engineeringbay'], matchup_dict2['factory'], matchup_dict2[
                                'factoryreactor'], matchup_dict2['factorytechlab'], matchup_dict2['fusioncore'],
                            matchup_dict2['ghost'], matchup_dict2['ghostacademy'], matchup_dict2['hellion'], matchup_dict2[
                                'liberator'], matchup_dict2['marauder'], matchup_dict2['marine'], matchup_dict2['medivac'],
                            matchup_dict2['missileturret'], matchup_dict2['mule'], matchup_dict2['nuke'], matchup_dict2[
                                'orbitalcommand'], matchup_dict2['planetaryfortress'], matchup_dict2['raven'], matchup_dict2['reactor'],
                            matchup_dict2['reaper'], matchup_dict2['refinery'], matchup_dict2[
                                'scv'], matchup_dict2['sensortower'], matchup_dict2['siegetank'],
                            matchup_dict2['starport'], matchup_dict2['starportreactor'], matchup_dict2[
                                'starporttechlab'], matchup_dict2['supplydepot'], matchup_dict2['techlab'], matchup_dict2['thor'],
                            matchup_dict2['viking'], matchup_dict2['warhound'], matchup_dict2['widowmine']
                        ])

            if type(event) is UnitBornEvent:
                if replay.players[0].pid == event.control_pid and replay.players[0].pick_race[0] == 'T':
                    if event.unit_type_name.lower() in matchup_dict:
                        if event.unit_id not in id_list:
                            id_list.append(event.unit_id)
                            matchup_dict[event.unit_type_name.lower()] += 1
                    elif event.unit.name.lower() in matchup_dict:
                        if event.unit_id not in id_list:
                            id_list.append(event.unit_id)
                            matchup_dict[event.unit.name.lower()] += 1
                    elif event.unit.name.lower() == 'liberatorag':
                        if event.unit_id not in id_list:
                            id_list.append(event.unit_id)
                            matchup_dict['liberator'] += 1
                    elif event.unit.name.lower() == 'vikingassault':
                        if event.unit_id not in id_list:
                            id_list.append(event.unit_id)
                            matchup_dict['viking'] += 1

                if replay.players[1].pid == event.control_pid and replay.players[1].pick_race[0] == 'T':
                    if event.unit_type_name.lower() in matchup_dict2:
                        if event.unit_id not in id_list:
                            id_list.append(event.unit_id)
                            matchup_dict2[event.unit_type_name.lower()] += 1
                    elif event.unit.name.lower() in matchup_dict2:
                        if event.unit_id not in id_list:
                            id_list.append(event.unit_id)
                            matchup_dict2[event.unit.name.lower()] += 1
                    elif event.unit.name.lower() == 'liberatorag':
                        if event.unit_id not in id_list:
                            id_list.append(event.unit_id)
                            matchup_dict2['liberator'] += 1
                    elif event.unit.name.lower() == 'vikingassault':
                        if event.unit_id not in id_list:
                            id_list.append(event.unit_id)
                            matchup_dict2['viking'] += 1

            if type(event) is UnitDiedEvent:
                if replay.players[0] == event.unit.owner and replay.players[0].pick_race[0] == 'T':
                    if event.unit.name.lower() in matchup_dict:
                        if event.unit_id in id_list:
                            id_list.remove(event.unit_id)
                            matchup_dict[event.unit.name.lower()] -= 1
                    elif event.unit.name.lower() == 'liberatorag':
                        if event.unit_id in id_list:
                            id_list.remove(event.unit_id)
                            matchup_dict['liberator'] -= 1
                    elif event.unit.name.lower() == 'vikingassault':
                        if event.unit_id in id_list:
                            id_list.remove(event.unit_id)
                            matchup_dict['viking'] -= 1
                    elif event.unit.name.lower() == 'siegetanksieged':
                        if event.unit_id in id_list:
                            id_list.remove(event.unit_id)
                            matchup_dict['siegetank'] -= 1
                    elif event.unit.name.lower() == 'widowmineburrowed':
                        if event.unit_id in id_list:
                            id_list.remove(event.unit_id)
                            matchup_dict['widowmine'] -= 1
                    elif event.unit.name.lower() == 'battlehellion':
                        if event.unit_id in id_list:
                            id_list.remove(event.unit_id)
                            matchup_dict['hellion'] -= 1
                    elif event.unit.name.lower() == 'supplydepotlowered':
                        if event.unit_id in id_list:
                            id_list.remove(event.unit_id)
                            matchup_dict['supplydepot'] -= 1
                    elif event.unit.name.lower() == 'orbitalcommandflying':
                        if event.unit_id in id_list:
                            id_list.remove(event.unit_id)
                            matchup_dict['orbitalcommand'] -= 1
                    elif event.unit.name.lower() == 'commandcenterflying':
                        if event.unit_id in id_list:
                            id_list.remove(event.unit_id)
                            matchup_dict['commandcenter'] -= 1
                    elif event.unit.name.lower() == 'factoryflying':
                        if event.unit_id in id_list:
                            id_list.remove(event.unit_id)
                            matchup_dict['factory'] -= 1
                    elif event.unit.name.lower() == 'barracksflying':
                        if event.unit_id in id_list:
                            id_list.remove(event.unit_id)
                            matchup_dict['barracks'] -= 1
                    elif event.unit.name.lower() == 'thorap':
                        if event.unit_id in id_list:
                            id_list.remove(event.unit_id)
                            matchup_dict['thor'] -= 1

                if replay.players[1] == event.unit.owner and replay.players[1].pick_race[0] == 'T':
                    if event.unit.name.lower() in matchup_dict2:
                        if event.unit_id in id_list:
                            id_list.remove(event.unit_id)
                            matchup_dict2[event.unit.name.lower()] -= 1
                    elif event.unit.name.lower() == 'liberatorag':
                        if event.unit_id in id_list:
                            id_list.remove(event.unit_id)
                            matchup_dict2['liberator'] -= 1
                    elif event.unit.name.lower() == 'vikingassault':
                        if event.unit_id in id_list:
                            id_list.remove(event.unit_id)
                            matchup_dict2['viking'] -= 1
                    elif event.unit.name.lower() == 'siegetanksieged':
                        if event.unit_id in id_list:
                            id_list.remove(event.unit_id)
                            matchup_dict2['siegetank'] -= 1
                    elif event.unit.name.lower() == 'widowmineburrowed':
                        if event.unit_id in id_list:
                            id_list.remove(event.unit_id)
                            matchup_dict2['widowmine'] -= 1
                    elif event.unit.name.lower() == 'battlehellion':
                        if event.unit_id in id_list:
                            id_list.remove(event.unit_id)
                            matchup_dict2['hellion'] -= 1
                    elif event.unit.name.lower() == 'supplydepotlowered':
                        if event.unit_id in id_list:
                            id_list.remove(event.unit_id)
                            matchup_dict2['supplydepot'] -= 1
                    elif event.unit.name.lower() == 'orbitalcommandflying':
                        if event.unit_id in id_list:
                            id_list.remove(event.unit_id)
                            matchup_dict2['orbitalcommand'] -= 1
                    elif event.unit.name.lower() == 'commandcenterflying':
                        if event.unit_id in id_list:
                            id_list.remove(event.unit_id)
                            matchup_dict2['commandcenter'] -= 1
                    elif event.unit.name.lower() == 'factoryflying':
                        if event.unit_id in id_list:
                            id_list.remove(event.unit_id)
                            matchup_dict2['factory'] -= 1
                    elif event.unit.name.lower() == 'barracksflying':
                        if event.unit_id in id_list:
                            id_list.remove(event.unit_id)
                            matchup_dict2['barracks'] -= 1
                    elif event.unit.name.lower() == 'thorap':
                        if event.unit_id in id_list:
                            id_list.remove(event.unit_id)
                            matchup_dict2['thor'] -= 1

            if type(event) is UnitInitEvent:
                if replay.players[0].pid == event.control_pid and replay.players[0].pick_race[0] == 'T':
                    if event.unit.name.lower() in matchup_dict:
                        if event.unit_id not in id_list:
                            id_list.append(event.unit_id)
                            matchup_dict[event.unit.name.lower()] += 1
                    elif event.unit.name.lower() == 'supplydepotlowered':
                        if event.unit_id not in id_list:
                            id_list.append(event.unit_id)
                            matchup_dict['supplydepot'] += 1
                    else:
                        print(event)

                if replay.players[1].pid == event.control_pid and replay.players[1].pick_race[0] == 'T':
                    if event.unit.name.lower() in matchup_dict2:
                        if event.unit_id not in id_list:
                            id_list.append(event.unit_id)
                            matchup_dict2[event.unit.name.lower()] += 1
                    elif event.unit.name.lower() == 'supplydepotlowered':
                        if event.unit_id not in id_list:
                            id_list.append(event.unit_id)
                            matchup_dict2['supplydepot'] += 1
                    else:
                        print(event)

        counter += 1

columns = terran_data['columns'] + matchup_dict.keys()
T_gang = pd.DataFrame(T_gang, columns=columns)

T_gang.to_csv('C:\\Users\\tluka\\Desktop\\data2.csv', index=False)
