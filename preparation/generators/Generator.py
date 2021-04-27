from glob import glob
from sc2reader import load_replays
from sc2reader.engine import register_plugin
from sc2reader.engine.plugins import APMTracker, ContextLoader, SelectionTracker

from .WorkReplays import WorkReplays


class Generator(WorkReplays):
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


    def __init__(self, attr_map=None):
        '''
        Constructs all the necessary attributes for HandleReplays.

        Parameters
        ----------
        attr_map : dict
            Attribute map
        '''

        if attr_map is None:
            return Exception('Please provide an attr_map.')
        
        self.attr_map = attr_map


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

        paths = [path for path in glob(glob_path, recursive=True)]
        loader_amount = len(paths) if limit is None or limit > len(paths) else limit
        n_replays = len(paths)

        register_plugin(APMTracker())
        register_plugin(SelectionTracker())
        register_plugin(ContextLoader())

        replays = load_replays(paths[:limit])
        
        if verbose:
            print('Loaded {} replays out of {}.'.format(loader_amount, n_replays))

        self.paths = paths[:limit]
        self.replays = replays
        self.n_replays = n_replays
        self.loader_amount = loader_amount