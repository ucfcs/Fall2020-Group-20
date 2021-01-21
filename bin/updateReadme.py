from Tree import Tree
from pathlib import Path

if __name__ == '__main__':
    tree = Tree(Path(__file__).parent.parent)
    gen = tree.generate()

    file_path = Path(__file__).parent.parent / 'README.md'

    index = None
    index2 = None
    with open(file_path, 'r') as f:
        a = f.read().splitlines()

        if '### Contents' in a:
            index = a.index('### Contents')+1
            if '' in a[index:]:
                index2 = index + a[index:].index('')
        else:
            print('Could not find "### Contents"')

    if index is not None and index2 is not None:
        with open(file_path, 'w') as f:
            new_readme = '\n'.join(a[:index]) + '\n' + '```\n' + \
                '\n'.join(gen) + '\n```' + '\n' + '\n'.join(a[index2:])
            f.write(new_readme)
