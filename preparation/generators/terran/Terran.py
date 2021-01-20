from sc2reader import data, events
import json


class Terran:
	def __init__(self, attr_map):
		# unit_data = json.loads(data.unit_data)

		# unit_map = {}
		# for k in unit_data:
		# 	unit_map[k] = list(unit_data[k].keys())

		# with open('../../constants/terran.json', 'rb') as f:
		# 	self.attr_map = json.load(f)

		# self.terran_dict = dict.fromkeys(self.attr_map['units'], 0)
		# self.self.attr_map_conversion_keys = self.attr_map['conversion'].keys()

		self.attr_map = attr_map
		self.terran_dict = dict.fromkeys(attr_map['units'], 0)
		self.self.attr_map_conversion_keys = attr_map['conversion'].keys()


	def get(self, replay, match_id):
		self.rows = []
		matchup = [self.terran_dict.copy(), self.terran_dict.copy()]
		id_list = set()

		for event in replay.events:
			if event.second % 30 == 0:
				for i in range(2):
					if isinstance(event, events.PlayerStatsEvent):
						if replay.players[i].pid == event.pid and replay.players[i].pick_race[0] == 'T':
							lower_bound = 0 if event.second == 0 else event.second-30
							ap30s = sum(list(replay.players[i].aps.values())[lower_bound:event.second])

							race = replay.players[i].pick_race[0]
							win = replay.players[i].result == 'Win'

							map_name = replay.map_name
							region = replay.region
							game_length = replay.game_length.seconds

							row_data = {}

							row_data['match_id'] = match_id
							row_data['map_name'] = map_name
							row_data['region'] = region
							row_data['game_length'] = game_length
							row_data['race'] = race
							row_data['ap30s'] = ap30s

							for col in self.attr_map['columns']:
								row_data[col] = eval('event.' + col)
							for unit in self.attr_map['units']:
								row_data[unit] = matchup[0][unit]

							row_data['win'] = win

							self.rows.append(row_data)

			# If event is a unit being created, typically the start of the game and military units being created such as marines, liberators etc.
			for i in range(2):
				if isinstance(event, events.UnitBornEvent):

					# unit_name and unit_type are sometimes two different names so we need to check for both names to see if it's in our Terran Dictionary
					# some_units_to_be_converted special are two special cases for names that need to be converted to keep consitency within our dictionary
					unit_name = event.unit.name.lower()
					unit_type = event.unit_type_name.lower()
					some_units_to_be_converted = ['liberatorag','vikingassault']

					for i in range(2):
						if replay.players[i].pid == event.control_pid and replay.players[i].pick_race[0] == 'T':

							# We first check if the variable for the unit_type or unit_name exists in our dictionary, and  if true then
							# check to see if the unit's special id, which is unique for every individual unit, exist.
							# Sometimes sc2reader will wrongly re-read the creation of a unit so we keep track of the ID to get rid of any accidential duplication.
							# The counter for that unit is then incremented by one.
							if unit_type in matchup[i]:
								if event.unit_id not in id_list:
									matchup[i][unit_type] += 1
								id_list.add(event.unit_id)
							elif unit_name in matchup[i]:
								if event.unit_id not in id_list:
									matchup[i][unit_name] += 1
								id_list.add(event.unit_id)
							elif unit_name in some_units_to_be_converted and unit_name in self.self.attr_map_conversion_keys:
								converted_unit_name = self.attr_map['conversion'][unit_name]
								if event.unit_id not in id_list:
									matchup[i][converted_unit_name] += 1
								id_list.add(event.unit_id)

				if isinstance(event, events.UnitDiedEvent):
					if replay.players[i] == event.unit.owner and replay.players[i].pick_race[0] == 'T':
						unit_name = event.unit.name.lower() 

						# Same as UnitBornEvent, except when we find a matching unit name and ID in the id_list, we then remove that ID.
						# This way of checking for the ID before decrementing should get rid of the negative counts for units in the dataset
						if unit_name in matchup[i]:
							if event.unit_id in id_list:
								id_list.remove(event.unit_id)
								matchup[i][unit_name] -= 1
						elif unit_name in self.self.attr_map_conversion_keys:
							converted_unit_name = self.attr_map['conversion'][unit_name]
							if event.unit_id in id_list:
								id_list.remove(event.unit_id)
								matchup[i][converted_unit_name] -= 1

				if isinstance(event, events.UnitInitEvent):
					unit_name = event.unit.name.lower()
					some_units_to_be_converted = ['supplydepotlowered']

					# Same as UnitBorn, this class typically is called when a building has been intialized
					if replay.players[i].pid == event.control_pid and replay.players[i].pick_race[0] == 'T':
						if unit_name in matchup[i]:
							if event.unit_id not in id_list:
								matchup[i][unit_name] += 1
							id_list.add(event.unit_id)
						elif unit_name in some_units_to_be_converted and unit_name in self.self.attr_map_conversion_keys:
							converted_unit_name = self.attr_map['conversion'][unit_name]
							if event.unit_id not in id_list:
								matchup[i][converted_unit_name] += 1
							id_list.add(event.unit_id)