import argparse
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument('path')
parser.add_argument('-r', '--recursive', action='store_true')
parser.add_argument('-e', '--extension', default='.py')
parser.add_argument('-s', '--save', action='store_true', default=False)
parser.add_argument('-o', '--output-directory', default='.')
parser.add_argument('-f', '--filename', default='extensionparser.txt')
arg = parser.parse_args()

path = Path(arg.path).resolve()
if arg.recursive is True:
    ext = set([Path(f).suffix for f in path.rglob('*')])
else:
    ext = set([Path(f).suffix for f in path.glob('*')])
    
if arg.save is True:
    outdir = Path(arg.output_directory).resolve() / arg.filename
    try:
        with outdir.open('w', encoding='utf-8') as f:
            for aext in ext:
                print(aext, file=f)
        print('Save the file {}'.format(outdir.__str__()))
    except IOError:
        print('Fail to save the file; {}'.format(IOError))
else:
    print(ext)