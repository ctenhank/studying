from pathlib import Path
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('pattern')
parser.add_argument('-s','--save', action='store_true')
parser.add_argument('-f', '--filename', default='fileformat.txt')

arg = parser.parse_args()

path = Path(arg.file).resolve()

set_ = set([])
with path.open('r') as f:
    for line in f:
        if line.startswith(arg.pattern) == True:
            part = line.split(' ')[0]
            part = part.split(arg.pattern)[-1]
            if part.find('\\tA') == -1 :
                set_.add(part)

if arg.save == True:
    with Path(arg.filename).resolve().open('w') as f:
        print(list(set_), file=f)
#         for element in set_:
#             print(element, file=f)        
else:
    print(list(set_))
# print(list(set_)
