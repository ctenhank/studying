import re
import argparse
from pathlib import Path

import_= set([])

def read_file(filepath):
    try:
        with Path(filepath).resolve().open(mode='r') as f:
            for line in f:
                if 'import' in line or 'from' in line:
                    parts = re.split('[ ,]', line)
                    if parts[0] == 'from' or parts[0] == 'import':
                        isAs = False
                        for part in parts:
                            if part == 'as':
                                isAs = True
                                continue

                            if isAs == True:
                                isAs = False
                                continue
                            
                            part = part.replace('\n', '')
                            import_.add(part)
            print("READ {}".format(file))
    except IOError:
        print("FAIL {}".format(file))
    


parser = argparse.ArgumentParser()
parser.add_argument('path')
parser.add_argument('-r', '--recursive', action='store_true')
parser.add_argument('-e', '--extension', default='.py')
parser.add_argument('-s', '--save', action='store_true', default=False)
parser.add_argument('-o', '--output-directory', default='.')
parser.add_argument('-f', '--filename', default='importparser.txt')

arg = parser.parse_args()

stream = []
p = Path(arg.path)

if arg.recursive is True:
    stream = p.rglob('*' + arg.extension)
else:
    stream = p.glob()

for file in stream:
    if Path(file).parts[3][0] == '.':
        continue
    read_file(file)

if arg.save is True:
    outdir = Path(arg.output_directory).resolve() / arg.filename
    try:
        with outdir.open('w', encoding='utf-8') as f:
            for module in import_:
                print(module, file=f, end=' ')
        print('Save the file {}'.format(outdir.__str__()))
    except IOError:
        print('Fail to save the file; {}'.format(IOError))
else:
    print(import_)
