import sc2reader
from sc2reader.engine.plugins import APMTracker, ContextLoader, SelectionTracker
from sc2reader.events import *
import pandas as pd

path = 'TIME_vs_MacSed_G1.SC2Replay'
workers = []

replay = sc2reader.load_replay(path)
for event in replay.events:
	if type(event) is PlayerStatsEvent:
		if replay.players[0].pid == event.pid:
			workers.append([event.player, replay.players[0].pick_race[0],
				event.workers_active_count,event.minerals_collection_rate,event.second])
		else:
			workers.append([event.player,replay.players[0].pick_race[0], 
			event.workers_active_count,event.minerals_collection_rate,event.second])

work = pd.DataFrame(workers)

work.columns = ["Player", "Race", "Worker Count", "Min Collection Rate","Seconds"]
print(work)
