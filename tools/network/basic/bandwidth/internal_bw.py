DEBUG_PRINT_STEP0 = False
DEBUG_PRINT_STEP1 = False
DEBUG_PRINT_STEP2 = False
DEBUG_PRINT_ELAPSED = True

################################
# Get the configuration
################################
import configparser

# Create a config parser object
config = configparser.ConfigParser()

# Read the configuration file (this just needs to be relative to the top executable)
config.read('config.ini')

# Access values from the configuration file
theseNodes  = config.get('main', 'nodes').split()
THREADED    = config.getboolean('main', 'threaded')
archive     = config.get('main', 'archive')

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
from datetime import datetime, timezone

local_time = datetime.now(timezone.utc).astimezone()

theseNodeMinMaxAvgLists = dict()

for thisNode, thisNodeList in theseNodeBWLists.items():
  thisMin =  min(thisNodeList[0])
  thisMax = max(thisNodeList[0])
  thisAvg = float("%.1f"%(sum(thisNodeList[0])/len(thisNodeList[0])))
  theseNodeMinMaxAvgLists[thisNode] = {
    "min": [thisMin], 
    "max": [thisMax], 
    "avg": [thisAvg], 
    "time": [local_time.isoformat()],
    "unit": thisNodeList[1]
  }

################################
# Output
################################
if archive == "JSON":

  import json, copy

  thisArchiveFile = "archive.%s"%(archive.lower())
  thisArchiveFileContent_new = dict()

  ########
  # Read the data
  try:

    # If the file doesn't already exist, this will fail and the except clause will be taken
    with open(thisArchiveFile, "r") as fh_read:
      thisArchiveFileContent_orig = json.load(fh_read)

    # Make a working copy of the new data dictionary
    # Deepcopy is needed, otherwise the new variable name still points to the original dictionary memory location and
    # the mutations below could cause disjointed datasets.
    thisArchiveFileContent_new = copy.deepcopy(theseNodeMinMaxAvgLists)

    ########
    # Modify the data
    for thisNode, thisNodeDict in theseNodeMinMaxAvgLists.items():
      # If the current node is already stored in the archive file, just append to it.
      if(thisNode in thisArchiveFileContent_orig):
        # If any new fields are added to the new dataset, it will fail here. This will cause the except clause to be
        # taken and the entire archive file overwritten with the new data.
        thisArchiveFileContent_new[thisNode]["min"] += thisArchiveFileContent_orig[thisNode]["min"]
        thisArchiveFileContent_new[thisNode]["max"] += thisArchiveFileContent_orig[thisNode]["max"]
        thisArchiveFileContent_new[thisNode]["avg"] += thisArchiveFileContent_orig[thisNode]["avg"]
        thisArchiveFileContent_new[thisNode]["time"] += thisArchiveFileContent_orig[thisNode]["time"]
  
  except:
    print("Archive doesn't exist, creating empty data structure...")
    # Re-copy the new dataset if anything went wrong trying to merge the archive and the new data...
    thisArchiveFileContent_new = copy.deepcopy(theseNodeMinMaxAvgLists)

  ########
  # Store the data
  try:
    with open(thisArchiveFile, "w") as fh_write:
      json.dump(thisArchiveFileContent_new, fh_write)

  except:
    print("Something went wrong storing the data.")

else:
  thisCumulativeBW = 0.0
  thisCumulativeUnit = ""

  for thisNode, thisNodeDict in theseNodeMinMaxAvgLists.items():
    print("\nThe node %s has the points:"%(thisNode))
    print("Min: %s %s"%(thisNodeDict["min"], thisNodeDict["unit"]))
    print("Max: %s %s"%(thisNodeDict["max"], thisNodeDict["unit"]))
    print("Avg: %s %s"%(thisNodeDict["avg"], thisNodeDict["unit"]))
    thisCumulativeBW += thisNodeDict["avg"][0]
    thisCumulativeUnit = thisNodeDict["unit"]

  thisCumulativeBW = float("%.1f"%(thisCumulativeBW))
  if THREADED:
    print("\nCumulative Average Bandwidth:")
    print("%s %s"%(thisCumulativeBW, thisCumulativeUnit))

if DEBUG_PRINT_ELAPSED:
  print("\nElapsed time: %s seconds"%(elapsed_time))
