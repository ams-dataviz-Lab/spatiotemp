import sys
import getopt
import pandas as pd
import pyproj as pp
from polycircles import polycircles
import simplekml
import datetime

# Returns minimum difference between any pair in an unsorted array
def findMinDiff(arr):

    # Sort array in ascending order
    arr = sorted(arr)

    # Initialize difference as infinite
    diff = 10**20

    # Find the min diff by comparing adjacent
    # pairs in sorted array
    for i in range(len(arr)-1):
        if arr[i+1] - arr[i] < diff:
            diff = arr[i+1] - arr[i]

    # Return min diff
    return diff

# generate KML file
def convertToKML(inputFilename,
                 outputFilename,
                 radius,
                 maxHeight,
                 nrVertices):

    # read data from input file
    data = pd.read_csv(inputFilename)
    # get maximum value for scaling the height of the cylinders
    maxValue = data['value'].max()

    # find smallest difference in timestamps, this is the interval size
    uniqueTimestamps = data.time.unique()
    timestamps = uniqueTimestamps.tolist()
    timestamps.sort()
    timeIntervalSize = findMinDiff(timestamps)

    kml = simplekml.Kml()

    for index,row in data.iterrows():
        scaledValue = row['value'] * (maxHeight/maxValue)
        polycircle = polycircles.Polycircle(latitude = row['latitude'], longitude=row['longitude'], radius=radius, number_of_vertices=nrVertices)

        coordsWithZ = [] # coords with z-value equal to scaledValue
        for coord in polycircle.to_kml():
            coordsWithZ.append(coord + (scaledValue,))

        pol = kml.newpolygon(extrude=1,
                             altitudemode='absolute',
                             outerboundaryis=coordsWithZ)
        pol.timespan.begin = datetime.datetime.fromtimestamp(row['time']).strftime('%Y-%m-%dT%H:%M:%S')
        pol.timespan.end = datetime.datetime.fromtimestamp(row['time']+timeIntervalSize).strftime('%Y-%m-%dT%H:%M:%S')

    kml.save(outputFilename)


def main(argv):
    # set default values
    inputFilename = 'input.csv'
    outputFilename = 'output.csv'
    radius = 100 # radius of cylinders, in meters
    maxHeight = 2000 # maximum height of cylinders, in meters
    nrVertices = 36 # nr vertices to construct circle of cylinder, the more, the smoother

    usage = """usage: convertKML.py
                -i <inputfile>
                -o <outputfile>
                -r <radius>
                -h <maxheight>
                -v <nrvertices>"""
    try:
        opts, args = getopt.getopt(argv,"hi:o:r:h:v:",
            ["inputfile=","outputfile=","radius=","maxheight=","nrvertices="])
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
        elif opt in ("-r", "--radius"):
            radius = arg
        elif opt in ("-h", "--maxheight"):
            maxHeight = arg
        elif opt in ("-v", "--nrvertices"):
            nrVertices = arg

    convertToKML(
                inputFilename,
                outputFilename,
                radius,
                maxHeight,
                nrVertices)

if __name__ == "__main__":
   main(sys.argv[1:])
