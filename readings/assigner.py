import os
import sys, getopt
from shutil import which

help_msg = 'Usage: assigner.py -t <title> -l [label] -m [milestone] -b [body]'
collaborators = ['vadManuel','elaineng21','Ipleau','oamer6','tlukas23']

def issue(title='', body='', label='', milestone='', assignee=''):
    if not title:
        print(help_msg)
        sys.exit(2)
    if not assignee:    
        print(help_msg)
        sys.exit(2)
    return 'gh issue create -t "{}" -b "{}" -l "{}" -m "{}" --assignee {}'.format(title,body,label,milestone,assignee)


def main(argv):
    if not which('gh'):
        print('\nPlease install Github CLI.\nhttps://github.com/cli/cli')
        sys.exit(3)

    try:
        opts, args = getopt.getopt(argv, 'ht:b:l:m:', ['help', 'title=', 'body=', 'label=', 'milestone='])
    except getopt.GetoptError:
        print(help_msg)
        sys.exit(2)

    title = ''
    body = ''
    label = ''
    milestone = ''
    for opt, arg in opts:
        if opt in ['-h','--help']:
            print(help_msg)
            sys.exit(2)
        elif opt in ['-t','--title']:
            title = arg
        elif opt in ['-b','--body']:
            body = arg
        elif opt in ['-l','--label']:
            label = arg
        elif opt in ['-m','--milestone']:
            milestone = arg
    
    if not title:
        print(help_msg)
        sys.exit(2)

    print('''
Available collaborators: {}

title="{}"
body="{}"
label="{}"
milestone="{}"

Is this correct? (Y/n): '''.format(', '.join(collaborators),title,body,label,milestone), end='')
    
    is_correct = input()
    while is_correct.upper() != 'Y':
        if is_correct.upper() == 'N':
            sys.exit()
        print('Please use options Y/n:', end=' ')
        is_correct = input()
    print()

    for collaborator in collaborators:
        new_issue = issue(title=title, body=body, label=label, milestone=milestone, assignee=collaborator)
        os.system(new_issue)


if __name__ == '__main__':
    main(sys.argv[1:])
