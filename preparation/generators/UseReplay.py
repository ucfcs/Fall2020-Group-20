from sc2reader import events


class UseReplay:
	'''
	Terran
	TT
	TP
	TZ

	Protoss
	PT
	PP
	PZ

	Zerg
	ZT
	ZP
	ZZ
	'''


	# only look at first player
	def __getData__(self, replay=None, match_id=None, player_index=0):
		rows = []

		# enemy_player_index is the opposite of player_index
		enemy_player_index = int(player_index == 0)
		race = replay.players[player_index].pick_race[0]
		
		enemy_race = replay.players[enemy_player_index].pick_race[0]

		attr_race = self.attr_map[race]
		units_dict = dict.fromkeys(attr_race['units'], 0)

		attr_race_conversion_keys = attr_race['conversion'].keys()

		matchup = units_dict.copy()
		id_list = set()

		for event in replay.events:
			if event.second % 30 == 0:
				if isinstance(event, events.PlayerStatsEvent):
					if replay.players[player_index].pid == event.pid:
						lower_bound = 0 if event.second == 0 else event.second-30

						ap30s = sum(list(replay.players[player_index].aps.values())[lower_bound:event.second])
						win = replay.players[player_index].result == 'Win'
						map_name = replay.map_name
						region = replay.region
						game_length = replay.game_length.seconds

						row_data = {}

						row_data['match_id'] = match_id
						row_data['map_name'] = map_name
						row_data['region'] = region
						row_data['game_length'] = game_length
						row_data['race'] = race
						row_data['enemy_race'] = enemy_race
						row_data['ap30s'] = ap30s

						for col in attr_race['columns']:
							row_data[col] = eval('event.' + col)
						for unit in attr_race['units']:
							row_data[unit] = matchup[unit]

						row_data['win'] = win

						rows.append(row_data)

			# If event is a unit being created, typically the start of the game and military units being created such as marines, liberators etc.
			if isinstance(event, events.UnitBornEvent):

				# unit_name and unit_type are sometimes two different names so we need to check for both names to see if it's in our [race] Dictionary
				# some_units_to_be_converted special are two special cases for names that need to be converted to keep consitency within our dictionary
				unit_name = event.unit.name.lower()
				unit_type = event.unit_type_name.lower()
				some_units_to_be_converted = attr_race['unit_born']

				if replay.players[player_index].pid == event.control_pid:

					# We first check if the variable for the unit_type or unit_name exists in our dictionary, and  if true then
					# check to see if the unit's special id, which is unique for every individual unit, exist.
					# Sometimes sc2reader will wrongly re-read the creation of a unit so we keep track of the ID to get rid of any accidential duplication.
					# The counter for that unit is then incremented by one.
					if unit_type in matchup:
						if event.unit_id not in id_list:
							matchup[unit_type] += 1
						id_list.add(event.unit_id)
					elif unit_name in matchup:
						if event.unit_id not in id_list:
							matchup[unit_name] += 1
						id_list.add(event.unit_id)
					elif unit_name in some_units_to_be_converted and unit_name in attr_race_conversion_keys:
						converted_unit_name = attr_race['conversion'][unit_name]
						if event.unit_id not in id_list:
							matchup[converted_unit_name] += 1
						id_list.add(event.unit_id)

			if isinstance(event, events.UnitDiedEvent):
				if replay.players[player_index] == event.unit.owner:
					unit_name = event.unit.name.lower() 

					# Same as UnitBornEvent, except when we find a matching unit name and ID in the id_list, we then remove that ID.
					# This way of checking for the ID before decrementing should get rid of the negative counts for units in the dataset
					if unit_name in matchup:
						if event.unit_id in id_list:
							id_list.remove(event.unit_id)
							matchup[unit_name] -= 1
					elif unit_name in attr_race_conversion_keys:
						converted_unit_name = attr_race['conversion'][unit_name]
						if event.unit_id in id_list:
							id_list.remove(event.unit_id)
							matchup[converted_unit_name] -= 1

			if isinstance(event, events.UnitInitEvent):
				unit_name = event.unit.name.lower()
				some_units_to_be_converted = attr_race['unit_init'] # ['supplydepotlowered']

				# Same as UnitBorn, this class typically is called when a building has been intialized
				if replay.players[player_index].pid == event.control_pid:
					if unit_name in matchup:
						if event.unit_id not in id_list:
							matchup[unit_name] += 1
						id_list.add(event.unit_id)
					elif unit_name in some_units_to_be_converted and unit_name in attr_race_conversion_keys:
						converted_unit_name = attr_race['conversion'][unit_name]
						if event.unit_id not in id_list:
							matchup[converted_unit_name] += 1
						id_list.add(event.unit_id)

			if isinstance(event, events.UnitTypeChangeEvent):
				unit_name = event.unit.name.lower()
				some_weird_units = attr_race['unit_type_change']

				if replay.players[player_index] == event.unit.owner:
					if unit_name in some_weird_units:
						if event.unit_id in id_list:
							matchup[unit_name] += 1

		return rows