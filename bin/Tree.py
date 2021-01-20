from pathlib import Path


space =  '    '
branch = '│   '
tee =    '├── '
last =   '└── '

class Tree():
    def __init__(self, dir_path: Path, ignore_dirs: list=[], level: int=-1):
        self.dir_path = dir_path
        self.ignore_dirs = ignore_dirs
        self.level = level
    
    def generate(self):
        dir_path = Path(self.dir_path)

        ret = [dir_path.name or '.']
        ret.extend(self.__make__())

        return ret
    
    def __make__(self, prefix: str=''):
        if not self.level:
            return

        contents = [d for d in self.dir_path.iterdir() if d.is_dir() and d.name not in self.ignore_dirs]
        pointers = [tee] * (len(contents) - 1) + [last]

        for pointer, path in zip(pointers, contents):
            if path.is_dir():
                yield prefix + pointer + path.name

                if pointer == tee:
                    extension = branch
                else:
                    extension = space

                self.dir_path = path
                self.level = self.level-1
                yield from self.__make__(prefix=prefix+extension)


if __name__ == '__main__':
    tree = Tree(Path(__file__).parent.parent, ignore_dirs=['data','.git','__pycache__','.ipynb_checkpoints','.vscode'])
    print('\n'.join(tree.generate()))