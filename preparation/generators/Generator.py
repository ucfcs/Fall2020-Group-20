from collections import Counter
import pandas as pd
import glob
import os

cache_dir = './cache'
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

os.environ['SC2READER_CACHE_DIR'] = cache_dir
os.environ['SC2READER_CACHE_MAX_SIZE'] = '2048MB'

import sc2reader
from sc2reader import events
from sc2reader.engine.plugins import APMTracker, SelectionTracker


class WorkReplays:
    def get_dataframe(self, verbose=True):
        '''
        Returns the generated DataFrame with the provided matchup.

        Parameters
        ----------
        matchup : str
            Matchup as a two character string with membership [PT,TP,PZ,ZP,TZ,ZT].
        verbose : bool, optional
            Show verbose information (default is True)
            

        Returns
        -------
        Matchup DataFrame
        '''
        
        race_map = {
            'P': 'Protoss',
            'T': 'Terran',
            'Z': 'Zerg'
        }

        df_data = {
            'PP': [],
            'PT': [],
            'PZ': [],
            'TT': [],
            'TZ': [],
            'ZZ': []
        }

        valid_match = 0

        for i, replay in enumerate(self.replays):
            if not verbose:
                 print('\rLoading replay {:4}/{:04} | Loaded {:6.2f}% of total!'.format(i+1, self.loader_amount, (i+1)/self.loader_amount*100), end='', flush=True)

            races = sorted([replay.players[0].pick_race[0], replay.players[1].pick_race[0]])
            unit_dict = {
                races[0]: dict.fromkeys(self.unit_map[race_map[races[0]]] + self.unit_map[race_map[races[1]]], 0),
                races[1]: dict.fromkeys(self.unit_map[race_map[races[0]]] + self.unit_map[race_map[races[1]]], 0)
            }

            if verbose:
                print('\n{} Game #{:03} | {} vs. {} {}'.format('-'*17, i+1, replay.players[0].pick_race, replay.players[1].pick_race, '-'*17))

            valid_match += 1
            dd = {}

            for event in replay.events:

                # break if nothing to collect
                if isinstance(event, events.PlayerLeaveEvent):
                    if verbose:
                        print('Player {} left {} seconds into the game.'.format(event.player, event.second))
                    break
                
                if isinstance(event, events.UnitInitEvent):
                    is_player_1 = replay.players[1].pid == event.control_pid
                    race = replay.players[is_player_1].pick_race[0]
                    unit = event.unit_type_name.lower()

                    if unit in unit_dict:
                        unit_dict[race][unit] += 1
                    elif verbose:
                        print('Found invalid unit "{}".'.format(unit))


                if isinstance(event, events.UnitBornEvent):
                    is_player_1 = replay.players[1].pid == event.control_pid
                    race = replay.players[is_player_1].pick_race[0]
                    unit = event.unit_type_name.lower()

                    if unit in unit_dict[race]:
                        unit_dict[race][unit] += 1
                    elif unit == 'vikingfighter':
                        unit_dict[race]['viking'] += 1
                    elif verbose:
                        print('Found invalid unit "{}".'.format(unit))

                if isinstance(event, events.UnitTypeChangeEvent):
                    try:
                        is_player_1 = replay.players[1].pid == event.unit.owner
                        race = replay.players[is_player_1].pick_race[0]
                        unit = event.unit_type_name.lower()

                        if unit in unit_dict:
                            unit_dict[race][unit] += 1
                        elif verbose:
                            print('Found invalid unit "{}".'.format(unit))
                    except:
                        print('Error', replay)
                        continue

                if isinstance(event, events.UnitDiedEvent):
                    is_player_1 = replay.players[1].pid == event.killing_player_id
                    race = replay.players[is_player_1].pick_race[0]
                    unit = event.unit.name.lower()

                    if unit in unit_dict:
                        unit_dict[race][unit] += 1
                    elif verbose:
                        print('Found invalid unit "{}".'.format(unit))

                # every 30 seconds
                if event.second % 30 == 0:

                    # every 10 seconds
                    if isinstance(event, events.PlayerStatsEvent):
                        d = {}

                        is_player_1 = replay.players[1].pid == event.pid
                        race = replay.players[is_player_1].pick_race[0]
                        win = replay.players[is_player_1].result == 'Win'

                        map_name = replay.map_name
                        region = replay.region
                        game_length = replay.game_length.seconds

                        lower_bound = 0 if event.second == 0 else event.second-30
                        ap30s = sum(list(replay.players[is_player_1].aps.values())[lower_bound:event.second])

                        d['match_id'] = i
                        d['map_name'] = map_name
                        d['region'] = region
                        d['game_length'] = game_length
                        d['frame'] = event.frame
                        d['second'] = event.second
                        d['race'] = race
                        d['ap30s'] = ap30s

                        for attr in self.attr_map['PlayerStatsEvent']:
                            d[attr] = eval('event.' + attr)
                        
                        d['win'] = win

                        dd[replay.players[is_player_1].pid] = d

                    # every 15 seconds
                    if isinstance(event, events.UnitPositionsEvent):
                        dd1 = dd[replay.players[0].pid]
                        dd2 = dd[replay.players[1].pid]

                        dd1.update(unit_dict[replay.players[0].pick_race[0]])
                        dd2.update(unit_dict[replay.players[1].pick_race[0]])

                        current_units = [str(a).split(' ')[0].lower() for a in event.units.keys()]
                        counted_units = Counter(current_units)

                        for k in counted_units:
                            if k in self.unit_map[race_map[races[0]]]:
                                dd1[k] = counted_units[k]
                            elif k in self.unit_map[race_map[races[1]]]:
                                dd2[k] = counted_units[k]
                            elif verbose:
                                print('Found invalid unit "{}".'.format(k))

                        df_data[''.join(races)].extend([dd1, dd2])
                        dd = {}

        print('')
        dfs = {}

        for k in df_data.keys():
            dfs[k] = pd.DataFrame(df_data[k])


        if verbose:
            print('\nEND: ({}, {}) found {} valid games out of {}.'.format(*dfs.shape, valid_match, len(self.replays)))

        return dfs


class HandleReplays(WorkReplays):
    '''
    A class to handle all thing SC2 replay. Extends WorkReplays.

    ...

    Attributes
    ----------
    attr_map : dict
        Attribute map
    unit_map : dict
        Unit map
    loader_amount : int
        Number of replays loaded

    Methods
    -------
    load_replays(glob_path, amount=None, verbose=True):
        Loads SC2 replays found in path.
    '''


    def __init__(self, attr_map=None, unit_map=None):
        '''
        Constructs all the necessary attributes for HandleReplays.

        Parameters
        ----------
        attr_map : dict
            Attribute map
        unit_map : dict
            Unit map
        '''

        if attr_map is None:
            return Exception('Please provide an attr_map.')
        if unit_map is None:
            return Exception('Please provide a unit_map.')
        
        self.attr_map = attr_map
        self.unit_map = unit_map


    def load_replays(self, glob_path, limit=None, verbose=True):
        '''
        Loads SC2 replays found in the provided path.

        If the argument 'amount' is passed, then only that amount will be loaded.

        Parameters
        ----------
        glob_path : str
            Path to .SC2Replay files as a glob string
        limit : int, optional
            Number of replays to be loaded (default is All)
        verbose : bool, optional
            Show verbose information (default is True)
            

        Returns
        -------
        None
        '''

        paths = [path for path in glob.glob(glob_path, recursive=True)]
        loader_amount = len(paths) if limit is None or limit > len(paths) else limit

        replays = sc2reader.load_replays(
            paths[:limit],
            engine=sc2reader.engine.GameEngine(plugins=[
                APMTracker(),
                SelectionTracker()
            ])
        )
        
        if verbose:
            print('Loaded {} replays.'.format(loader_amount))

        self.replays = replays
        self.loader_amount = loader_amount