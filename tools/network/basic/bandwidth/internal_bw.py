DEBUG_PRINT_STEP0 = False
DEBUG_PRINT_STEP1 = False
DEBUG_PRINT_STEP2 = True
DEBUG_PRINT_STEP3 = False

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
import subprocess, re

# Raw results are stored in a dictionary
theseRawResults = dict()

# For each node, simply get the output from iPerf3 with some minor filtering
for thisNode in theseNodes:
  try:
    print("Capturing network segment bandwidth to node %s"%(thisNode))
    cmdResultByteArray = subprocess.check_output(
      "iperf3 -f m -c %s | grep \"sec\""%thisNode,
      shell = True,
      executable = "/bin/bash",
      stderr = subprocess.STDOUT
    ).decode('utf-8').splitlines()
    theseRawResults[thisNode] = [re.sub(' +', ' ', x.strip()) for x in cmdResultByteArray]
  except:
    print("An error occured while transferring data with %s"%thisNode)

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
  # Pull out only the BW value
  for thisNodeValue in theseNodeValues:
    thisBWList.append(thisNodeValue.split()[6])
  # Put the list under the dict key, strip out the last two values since they are average values
  theseNodeBWLists[thisNode] = thisBWList[:-2]

# DEBUG
if DEBUG_PRINT_STEP2:
  for thisNode, theseNodeValues in theseNodeBWLists.items():
    print("The node %s has the BW sample points:"%(thisNode))
    print(theseNodeValues)
