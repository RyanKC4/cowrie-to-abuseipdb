import json
import csv
import io
import requests
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

def report_organizer(data):
    data_io = io.StringIO()
    writer = csv.writer(data_io)
    writer.writerow(['IP','Categories','ReportDate','Comment'])

    for ip,info in data.items():
        if info[0] >= 5:
            writer.writerow([ip,'18,22',info[1],f"Brute-force: {info[0]} connection attempts within 24 hours starting at {info[1]}."])

    data_io.seek(0)
    return data_io

def reporter(data_io,api_key):
    url = 'https://api.abuseipdb.com/api/v2/bulk-report'

    files = {
        'csv': (data_io)
    }

    headers = {
        'Accept': 'application/json',
        'Key': api_key
    }

    response = requests.request(method='POST', url=url, headers=headers, files=files)

    decodedResponse = json.loads(response.text)
    print(json.dumps(decodedResponse, sort_keys=True, indent=4))

def main():
    data = report_aggregator(argv[1])
    data_io = report_organizer(data)
    reporter(data_io,argv[2])
    data_io.close()

if __name__ == '__main__':
    main()
