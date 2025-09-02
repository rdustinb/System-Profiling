DEBUG_PRINT_STEP0 = False
DEBUG_PRINT_STEP1 = False
DEBUG_PRINT_STEP2 = False
DEBUG_PRINT_STEP3 = True
DEBUG_PRINT_ELAPSED = True

THREADED = True

################################
# Get the configuration
################################
import configparser

# Create a config parser object
config = configparser.ConfigParser()

# Read the configuration file (this just needs to be relative to the top executable)
config.read('config.ini')

# Access values from the configuration file
theseNodes = config.get('main', 'nodes').split()

# DEBUG
if DEBUG_PRINT_STEP0:
  print(theseNodes)

################################
# iPerf3 All Nodes
################################
import time, threading
from support import funcs

# For each node, simply get the output from iPerf3 with some minor filtering
start_time = time.time()

# Raw results are stored in a dictionary
theseRawResults = dict()

# Branch if threading is enabled (this doesn't currently work because of how iperf3 works)
if THREADED:

  theseThreads = list()
  
  # Start all the threads
  for thisNode in theseNodes:
    thisThread = threading.Thread(target=funcs.callIperf3, args=(thisNode,theseRawResults,))
    theseThreads.append(thisThread)
    thisThread.start()
  
  # Wait for all the threads to complete...
  for thisThread in theseThreads:
    thisThread.join()

else:

  for thisNode in theseNodes:
    funcs.callIperf3(thisNode,theseRawResults)

end_time = time.time()
elapsed_time = int(end_time - start_time)

# DEBUG
if DEBUG_PRINT_STEP1:
  print(theseRawResults)

################################
# Pull Out the Data we want
################################

# String Shape:   [ 7] 0.00-1.01 sec 116 MBytes 971 Mbits/sec
# Split Indices:  0  1         2   3   4      5   6         7

theseNodeBWLists = dict()

for thisNode, theseNodeValues in theseRawResults.items():
  thisBWList = list()
  thisUnit = ""
  # Pull out only the BW value
  for thisNodeValue in theseNodeValues:
    thisBWList.append(thisNodeValue.split()[6])
    thisUnit = thisNodeValue.split()[7]
  # Put the list under the dict key, strip out the last two values since they are average values
  theseNodeBWLists[thisNode] = ([float(x) for x in thisBWList[:-2]], thisUnit)

# DEBUG
if DEBUG_PRINT_STEP2:
  for thisNode, theseNodeValues in theseNodeBWLists.items():
    print("The node %s has the BW sample points:"%(thisNode))
    print(theseNodeValues)

################################
# Determine Min/AVG/Max values
################################

theseNodeMinMaxAvgLists = dict()

for thisNode, thisNodeList in theseNodeBWLists.items():
  thisMin =  min(thisNodeList[0])
  thisMax = max(thisNodeList[0])
  thisAvg = float("%.1f"%(sum(thisNodeList[0])/len(thisNodeList[0])))
  theseNodeMinMaxAvgLists[thisNode] = {
    "min": thisMin, 
    "max": thisMax, 
    "avg": thisAvg, 
    "unit": thisNodeList[1], 
    "raw": thisNodeList
  }

# DEBUG
if DEBUG_PRINT_STEP3:
  thisCumulativeBW = 0.0
  thisCumulativeUnit = ""

  for thisNode, thisNodeDict in theseNodeMinMaxAvgLists.items():
    print("\nThe node %s has the points:"%(thisNode))
    print("Min: %s %s"%(thisNodeDict["min"], thisNodeDict["unit"]))
    print("Max: %s %s"%(thisNodeDict["max"], thisNodeDict["unit"]))
    print("Avg: %s %s"%(thisNodeDict["avg"], thisNodeDict["unit"]))
    thisCumulativeBW += thisNodeDict["avg"]
    thisCumulativeUnit = thisNodeDict["unit"]

  thisCumulativeBW = float("%.1f"%(thisCumulativeBW))
  if THREADED:
    print("\nCumulative Average Bandwidth:")
    print("%s %s"%(thisCumulativeBW, thisCumulativeUnit))

if DEBUG_PRINT_ELAPSED:
  print("\nElapsed time: %s seconds"%(elapsed_time))
