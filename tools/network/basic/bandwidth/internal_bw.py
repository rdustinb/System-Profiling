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

################################
# iPerf3 All Nodes
################################
import subprocess, re

# Raw results are stored in a dictionary
theseRawResults = dict()

# For each node, simply get the output from iPerf3 with some minor filtering
for thisNode in theseNodes:
  try:
    cmdResultByteArray = subprocess.check_output(
      "iperf3 -c %s | grep \"sec\""%thisNode,
      shell = True,
      executable = "/bin/bash",
      stderr = subprocess.STDOUT
    ).decode('utf-8').splitlines()
    theseRawResults[thisNode] = [re.sub(' +', ' ', x.strip()) for x in cmdResultByteArray]
  except:
    print("An error occured while transferring data with %s"%thisNode)

print(theseRawResults)

################################
# Pull Out the Data we want
################################

# String Shape
# [ 7] 0.00-1.01 sec 116 MBytes 971 Mbits/sec
# Split Indices
# 0  1         2   3   4      5   6         7
for thisNode, theseNodeValues in theseRawResults.items():
  for thisNodeValue in theseNodeValues:
