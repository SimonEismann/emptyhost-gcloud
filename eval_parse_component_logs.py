#IMPORTANT: Python version 3.7

import csv

path = "logs/"
filenames = ["A", "B", "C"]
runs = ["const_10", "const_20", "const_30", "const_40", "const_50", "const_60", "const_70", "training"]
for run in runs:
    for file in filenames:
        scenario = path + run
        reader = csv.reader(open(scenario + "/" + file + ".csv"), delimiter=",")   # data format: [arrival time, department time]
        sortedlist = sorted(reader, key=lambda row: int(row[0]))
        open_requests = []
        writer = csv.writer(open(scenario + "/" + file + "_trainingdata.csv", "w", newline=''), delimiter=',')
        writer.writerow(["Response Time", "Concurrency (WC1)"])
        for row in sortedlist:
            to_remove = []
            for open_request in open_requests:
                if open_request[1] < row[0]:
                    to_remove.append(open_request)
            for req in to_remove:
                open_requests.remove(req)
            writer.writerow([(int(row[1]) - int(row[0])) / 1000000, len(open_requests) + 1])    #converts response time from nano to milliseconds and writes the concurrency (including the processed request -> +1) to file
            open_requests.append(row)
