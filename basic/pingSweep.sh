HOSTNAME=$1
PINGCOUNT=20
PINGDELAY_SECONDS=0.005

# -f floods the pings out as soon as the previous response returns, up to 100 times per second or a period of 0.01
# seconds.
#
# -i x.xx is the amount of delay to wait from when the previous response returns to when the next request is sent.
# Minimum of 0.002 seconds unless sudo is used.

declare -a PAYLOAD_BYTES_ARRAY=(
  56
  248
  504
  1016
  1406
  2040
)

if [ "${HOSTNAME}" == "" ]; then
  echo -e "Please provide a hostname to test..."
  echo -e "Usage:"
  echo -e "\tpingTest.sh <hostname>"
  exit
fi

echo -e "\n###################################################"
echo -e "Hostname is: ${HOSTNAME}"
echo -e "###################################################"

for PAYLOAD_BYTES in "${PAYLOAD_BYTES_ARRAY[@]}"; do
  echo -e "\n"
  echo -e "###################################################"
  echo -e "Byte payload of ${PAYLOAD_BYTES} bytes"
  echo -e "###################################################"
  ping -c ${PINGCOUNT} -i ${PINGDELAY_SECONDS} -s ${PAYLOAD_BYTES} ${HOSTNAME}
done
