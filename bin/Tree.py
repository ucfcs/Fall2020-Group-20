from pathlib import Path
import re


space =  '    '
branch = '│   '
tee =    '├── '
last =   '└── '


with open(Path(__file__).parent.parent / '.gitignore', 'r') as f:
	lines = f.read().splitlines()

new_lines = []
for line in lines:
    if len(line) > 0 and line[0] not in ['#']:
        new_line = str(line)

        # if new_line[0] == '\\':
        #     new_line = '/' + new_line[1:]
        # elif new_line[0] != '/':
        #     new_line = '/' + new_line
        
        new_line = new_line.replace('/','\/').replace('.','\.')

        if new_line[-1] == '*':
            new_lines.append(new_line.replace('*','.*'))
        else:
            new_lines.append(new_line.replace('*','.*?'))

ret = '\/(' + '|'.join(new_lines) + ')'
matcher = re.compile(ret)


class Tree():
    def __init__(self, dir_path: Path, only_dirs: bool=False, ignore_dirs: list=[], level: int=-1):
        self.only_dirs = only_dirs
        self.dir_path = dir_path
        self.ignore_dirs = set(ignore_dirs) | set(['/.git','media/'])
        self.level = level

        self.files = 0
    
    def generate(self):
        ret = [self.dir_path.name or '.']
        ret.extend(self.__make__())

        return ret
    
    def __make__(self, prefix: str=''):
        if not self.level:
            return

        if self.only_dirs:
            contents = []
            for d in self.dir_path.iterdir():
                if d.is_dir() and d.name not in self.ignore_dirs:
                    contents.append(d)
        else:
            contents = []
            for d in self.dir_path.iterdir():
                m = str(d)
                m = '/' + m[0:] if m[0] != '/' else m
                ignore = any([g in m for g in self.ignore_dirs])
                match = matcher.search(m)
                if match is None and not ignore:
                    contents.append(d)

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
            elif not self.only_dirs:
                yield prefix + pointer + path.name
                self.files += 1


if __name__ == '__main__':
    tree = Tree(Path(__file__).parent.parent)
    pretty = tree.generate()
    print('\n'.join(pretty))