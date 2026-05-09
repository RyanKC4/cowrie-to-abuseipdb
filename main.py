import json
from sys import argv

def report_aggregator(jsonFile):
    with open(jsonFile) as jFile:
        for entry in jFile:
            entryItem = json.loads(entry)
            if entryItem['eventid'] == 'cowrie.login.failed'

def main():
    report_aggregator(argv[1])

if __name__ == '__main__':
    main()
