import subprocess, re

def callIperf3(thisNode, theseRawResults):

  print("Capturing network segment bandwidth to node %s"%(thisNode))

  testBidirectional = True
  testType = "bytes" # time, bytes, or packets
  testCount = "20" # any number
  testUnit = "G" # K, M, G, or T

  thisNodeRaw = list()

  if testType == "time":
    thisTestVariant = f"-t {testCount}"
  elif testType == "bytes":
    thisTestVariant = f"-n {testCount}{testUnit}"
  elif testType == "packets":
    thisTestVariant = f"-k {testCount}{testUnit}"

  if testBidirectional:
    thisBidi = "--bidi"
  else:
    thisBidi = ""

  # Mutually Exclusive Options:
  #
  # Add -t X to specify the number of time in seconds to transmit
  # Add -n X[KMGT] to specify the number of bytes to transmit
  # Add -k X[KMGT] to specify the number of packets to transmit
  # Add -l X[KMGT] to specify the length of buffer to transmit
  #
  # Extra Options:
  #
  # Add --bidir to flow data in both directions
  #
  try:
    cmdResultByteArray = subprocess.check_output(
      f"iperf3 -f m {thisTestVariant} {thisBidi} -c {thisNode} | grep \"sec\"",
      shell = True,
      executable = "/bin/bash",
      stderr = subprocess.STDOUT
    ).decode('utf-8').splitlines()
    theseRawResults[thisNode] = [re.sub(' +', ' ', x.strip()) for x in cmdResultByteArray]
  except:
    print("An error occured while transferring data with %s"%thisNode)

