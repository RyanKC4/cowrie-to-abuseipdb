import json
from sys import argv

def report_aggregator(jsonFile):
    data = {}

    with open(jsonFile) as jFile:
        for entry in jFile:
            entryItem = json.loads(entry)
            if entryItem['eventid'] == 'cowrie.login.failed' or entryItem['eventid'] == 'cowrie.login.success':
                if entryItem['src_ip'] not in data:
                    data[entryItem['src_ip']] = [1,entryItem['timestamp']]
                else:
                    data[entryItem['src_ip']][0] += 1
    return data

#def report_compiler(data):


def main():
    data = report_aggregator(argv[1])
    for i,j in data.items():
        print(i,j)

if __name__ == '__main__':
    main()
