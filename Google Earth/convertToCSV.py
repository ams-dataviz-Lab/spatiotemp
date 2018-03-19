import sys
import getopt
import csv
import time

def convertCSV(
                inputFilename,
                outputFilename,
                timeFormat,
                inputFieldnameTime,
                inputFieldnameLatitude,
                inputFieldnameLongitude,
                inputFieldnameValue
                ):

    outputFieldnames = ['time','latitude','longitude','value']

    with open(inputFilename, 'r') as csvInput:
        reader = csv.DictReader(csvInput, delimiter=',')
        with open(outputFilename, 'w') as csvOutput:
            writer = csv.DictWriter(csvOutput, delimiter=',', fieldnames=outputFieldnames)
            writer.writeheader()
            for row in reader:
                if timeFormat == "":
                    timeStamp = row[inputFieldnameTime]
                else:
                    timeStamp = time.mktime(time.strptime(row[inputFieldnameTime], timeFormat))
                latitude = row[inputFieldnameLatitude]
                longitude = row[inputFieldnameLongitude]
                value = row[inputFieldnameValue]
                writer.writerow({'time': timeStamp, 'latitude': latitude, 'longitude': longitude, 'value': value})

def main(argv):
    # set default values
    inputFilename = 'input.csv'
    outputFilename = 'output.csv'
    timeFormat = ""
    inputFieldnameTime = 'time'
    inputFieldnameLatitude = 'latitude'
    inputFieldnameLongitude = 'longitude'
    inputFieldnameValue = 'value'

    usage = """usage: convertCSV.py
                -i <inputfile>
                -o <outputfile>
                -f <timeformat>
                -t <timefield>
                -y <latitudefield>
                -x <longitudefield>
                -v <valuefield>"""
    try:
        opts, args = getopt.getopt(argv,"hi:o:f:t:y:x:v:",
            ["inputfile=","outputfile=","timeformat=","timefield=","latitudefield=","longitudefield=","valuefield="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ("-i", "--inputfile"):
            inputFilename = arg
        elif opt in ("-o", "--outputfile"):
            outputFilename = arg
        elif opt in ("-f", "--timeformat"):
            timeFormat = arg
        elif opt in ("-t", "--timefield"):
            inputFieldnameTime = arg
        elif opt in ("-y", "--latitudefield"):
            inputFieldnameLatitude = arg
        elif opt in ("-x", "--longitudefield"):
            inputFieldnameLongitude = arg
        elif opt in ("-v", "--valuefield"):
            inputFieldnameValue = arg

    convertCSV(
                inputFilename,
                outputFilename,
                timeFormat,
                inputFieldnameTime,
                inputFieldnameLatitude,
                inputFieldnameLongitude,
                inputFieldnameValue)

if __name__ == "__main__":
   main(sys.argv[1:])
