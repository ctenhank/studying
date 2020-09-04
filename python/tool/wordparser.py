from pathlib import Path

with Path('./infocom2020.txt').open('r') as f:
    for line in f:
        print(line)