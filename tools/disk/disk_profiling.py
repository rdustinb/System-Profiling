import subprocess
import sys
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# Access values from the configuration file
folderLocation  = config.get('general', 'folderLocation')
dataType        = config.get('general', 'dataType')
runThroughput   = config.getboolean('general', 'runThroughput')
runLatency      = config.getboolean('general', 'runLatency')
printResults    = config.getboolean('general', 'printResults')

# Throughput (large block size, only one)
throughputBlockList = [ "262144", "524288", "1048576", "2097152", "4194304", "8388608", "16777216", "33554432", "67108864", "134217728", "268435456", "536870912", "1073741824" ]
#throughputBlockList = [ "64M" ]
throughputCount = "1"

throughputResults = dict()

if runThroughput:
    for i, thisBlock in enumerate(throughputBlockList):
        # Run the single test
        result = subprocess.run(
                ["dd",
                 f"if=/dev/{dataType}",
                 f"of={folderLocation}/throughput_{i}.dat",
                 f"bs={thisBlock}",
                 f"count={throughputCount}"],
                capture_output=True,
                text=True
                )
        # Parse for the bandwidth
        rawResult = result.stderr.split()[-2].strip("(")
        # Format the data point
        throughputResults[thisBlock] = "{:.3f}".format(float(rawResult)/1024/1024)
        # Print the results
        if printResults:
            print(f"{throughputCount} count of {thisBlock} is {throughputResults[thisBlock]} MBps")
    
    with open(f"{folderLocation}/throughput.csv", "w") as fh:
        fh.write("Block Size, Block Count, Total Data, Total Data [MB], Bandwidth [MBps]\n")
        for (thisBlock, thisBW) in zip(throughputResults.keys(),throughputResults.values()):
            totalData = int(thisBlock) * int(throughputCount) 
            totalDataMB = int(totalData) / 1024 / 1024 
            fh.write(f"{thisBlock}, {throughputCount}, {totalData}, {totalDataMB}, {thisBW}\n")

# Latency (small block size, varying count)
latencyBlock = "512"

latencyResults = dict()

if runLatency:
    for i, thisCount in enumerate(throughputBlockList):
        # To keep the total data transferred as the point of reference, the count in the latency test takes the throughput
        # block sizes and divides them by the constant latency block size
        latencyCount = int(int(thisCount)/int(latencyBlock))
        # Run the single test
        result = subprocess.run(
                ["dd",
                 f"if=/dev/{dataType}",
                 f"of={folderLocation}/latency_{i}.dat",
                 f"bs={latencyBlock}",
                 f"count={latencyCount}"],
                capture_output=True,
                text=True
                )
        # Parse for the bandwidth
        rawResult = result.stderr.split()[-2].strip("(")
        # Format the data point
        latencyResults[latencyCount] = "{:.3f}".format(float(rawResult)/1024/1024)
        # Print the results
        if printResults:
            print(f"{latencyCount} count of {latencyBlock} is {latencyResults[latencyCount]} MBps")
    
    with open(f"{folderLocation}/latency.csv", "w") as fh:
        fh.write("Block Size, Block Count, Total Data, Total Data [MB], Bandwidth [MBps]\n")
        for (thisCount, thisBW) in zip(latencyResults.keys(),latencyResults.values()):
            totalData = int(latencyBlock) * int(thisCount) 
            totalDataMB = int(totalData) / 1024 / 1024 
            fh.write(f"{latencyBlock}, {thisCount}, {totalData}, {totalDataMB}, {thisBW}\n")
