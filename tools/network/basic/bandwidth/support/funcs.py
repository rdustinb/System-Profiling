import subprocess, re

def callIperf3(thisNode, theseRawResults):

  print("Capturing network segment bandwidth to node %s"%(thisNode))

  thisNodeRaw = list()

  try:
    cmdResultByteArray = subprocess.check_output(
      "iperf3 -f m -c %s | grep \"sec\""%thisNode,
      shell = True,
      executable = "/bin/bash",
      stderr = subprocess.STDOUT
    ).decode('utf-8').splitlines()
    theseRawResults[thisNode] = [re.sub(' +', ' ', x.strip()) for x in cmdResultByteArray]
  except:
    print("An error occured while transferring data with %s"%thisNode)

