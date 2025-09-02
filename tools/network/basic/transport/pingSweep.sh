HOSTNAME=$1
PINGCOUNT=$2
VERBOSE=$3
PINGDELAY_SECONDS=0.005
LOGFILE=testOut.log

# -f floods the pings out as soon as the previous response returns, up to 100 times per second or a period of 0.01
# seconds.
#
# -i x.xx is the amount of delay to wait from when the previous response returns to when the next request is sent.
# Minimum of 0.002 seconds unless sudo is used.

usage () {
  echo -e "Usage:"
  echo -e "\tpingTest.sh <hostname> <ping packet count> <verbose Y or N>"
  exit
}

declare -a PAYLOAD_BYTES_ARRAY=(
  56
  120
  248
  504
  1016
  1406
  2040
)

# Check for incorrect call of the script...
if [ "${HOSTNAME}" == "" ] || [ "${PINGCOUNT}" == "" ] || [ "${VERBOSE}" == "" ]; then
  usage
fi

# Run the ping sweep...
(
echo -e "\n###################################################"
echo -e "# Target: ${HOSTNAME}"
echo -e "###################################################"

for PAYLOAD_BYTES in "${PAYLOAD_BYTES_ARRAY[@]}"; do
  echo -e "\n"
  echo -e "###################################################"
  echo -e "# ${PAYLOAD_BYTES} byte payload"
  echo -e "###################################################"
  ping -c ${PINGCOUNT} -i ${PINGDELAY_SECONDS} -s ${PAYLOAD_BYTES} ${HOSTNAME}
done
) > ${LOGFILE}

# Dump the results...
if [ "${VERBOSE}" == "Y" ]; then
  cat ${LOGFILE}
else
  grep -e "packet loss" -e "#" ${LOGFILE}
fi
