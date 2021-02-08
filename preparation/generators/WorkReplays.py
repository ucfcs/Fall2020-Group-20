from pandas import DataFrame
from .UseReplay import UseReplay
import time
from .utils import getTime


class WorkReplays(UseReplay):
    def getData(self, verbose=True):
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

        df_data = {
            'P': [],
            'T': [],
            'Z': []
        }

        self.valid_matches = dict.fromkeys(df_data.keys(), 0)
        self.invalid_matches = dict.fromkeys(df_data.keys(), 0)

        t0 = time.time()

        for i, replay in enumerate(self.replays):
            if not verbose:
                time_elapsed = time.time() - t0
                eta = (self.loader_amount - i+1) * (time_elapsed/(i+1))

                time_elapsed_str = getTime(time_elapsed)
                eta_str = getTime(eta)

                print('\rLoading replay {:4}/{:04} | Loaded {:6.2f}% | ETA {} Elapsed {}'.format(
                    i+1, self.loader_amount, (i+1)/self.loader_amount*100, eta_str, time_elapsed_str), end='', flush=True)

            if verbose:
                print('\n{} Game #{:03} | {} vs. {} {}'.format('-'*17, i+1, replay.players[0].pick_race, replay.players[1].pick_race, '-'*17))

            # stores both sides of the matchup
            for player_index in range(2):
                race = replay.players[player_index].pick_race[0]

                try:
                    rows = self.__getData__(replay=replay, match_id=i, player_index=player_index)
                    self.valid_matches[race] += 1
                    df_data[race].extend(rows)
                except Exception as e:
                    self.invalid_matches[race] += 1
                    print('\nSkipping replay #{} due to thrown exception.'.format(i))
                    print(e)

        dfs = {}

        for k in df_data.keys():
            dfs[k] = DataFrame(df_data[k])

        total_valid_matches = sum(self.valid_matches.values())
        print('\n\nEND: Found {} valid games (total={}) out of {}.'.format(self.valid_matches, total_valid_matches, self.n_replays))

        return dfs
