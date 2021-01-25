from pandas import DataFrame
from .UseReplay import UseReplay
import time


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

        t0 = time.time()

        for i, replay in enumerate(self.replays):
            if not verbose:
                m, s = divmod(time.time() - t0, 60)
                h, m = divmod(m, 60)
                print('\rLoading replay {:4}/{:04} | Loaded {:6.2f}% | Elapsed {:02d}h{:02d}m{:02d}s'.format(
                    i+1, self.loader_amount, (i+1)/self.loader_amount*100, int(h), int(m), int(s)), end='', flush=True)

            race = replay.players[0].pick_race[0]

            if race in self.attr_map.keys():
                if verbose:
                    print('\n{} Game #{:03} | {} vs. {} {}'.format('-'*17, i+1, replay.players[0].pick_race, replay.players[1].pick_race, '-'*17))

                try:
                    rows = self.__getData__(replay=replay, match_id=i)
                    self.valid_matches[race] += 1
                    df_data[race].extend(rows)
                except Exception as e:
                    print('\nSkipping replay #{} due to thrown exception.'.format(i))
                    print(e)

        dfs = {}

        for k in df_data.keys():
            dfs[k] = DataFrame(df_data[k])

        total_valid_matches = sum(self.valid_matches.values())
        print('\n\nEND: Found {} valid games (total={}) out of {}.'.format(self.valid_matches, total_valid_matches, self.n_replays))

        return dfs
