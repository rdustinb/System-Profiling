"""
  --- DNS
  DNS is a powerful service provided by many different servers around the world. These servers translate website URLs
  (www.google.com) into machine-needed IP addresses, which is what the internet ***actually*** runs on...not the user-
  readable URLs.

  There are multiple types of DNS services that are provided and could be monitored, however this script will simply test
  multiple DNS servers for accessibility and proper response.

  URL for the list of DNS servers:
    https://www.lifewire.com/free-and-public-dns-servers-2626062
"""
import time
import sys

dependency_fail = False

try:
  from termcolor import colored, cprint
except:
  print("Please install Python 3 version of termcolor package using:\n\n\tpip install termcolor\n\n")
  dependency_fail = True

try:
  import dns.resolver
  from dns.exception import DNSException
except:
  print("Please install Python 3 version of dnspython package using:\n\n\tpip install dnspython\n\n")
  dependency_fail = True

if dependency_fail is True:
  sys.exit(-1)

dns_query_timeout_in_seconds = 1

def load_dns_data_structures(location):
  """
    This function will attempt to load/read the stored DNS and Web server JSON objects from the same directory that the
    script was launched from. If no file is found, the default will be used.
  """
  import json
  try:
    filename = '.'+location+'_dns.json'
    with open(filename, 'r') as fp:
      return(json.load(fp))
  except:
    print("DNS JSON File does not exist, using default.")
    filename = 'default_dns_list.json'
    with open(filename, 'r') as fp:
      return(json.load(fp))

def store_dns_data_structures(dns_servers, location):
  """
    This function will store the modified DNS server structure as a JSON object in the same directory that the script
    was launched from.
  """
  import json
  try:
    filename = '.'+location+'_dns.json'
    with open(filename, 'w') as fp:
      json.dump(dns_servers, fp)
  except:
    print("DNS JSON File could not be stored.")

def test_dns_servers(dns_server_list, dns_timeout):
  """
    This function will test multiple DNS servers, both primary and secondary as available, for proper responses.

      dns_server_list   A dictionary of lists. Each dictionary key is the name of the DNS server, and the list element is
                        of the primary and (if available) secondary addresses for that DNS server.
  """
  for server_name in dns_server_list.keys():
    cprint(server_name, 'white', attrs=['bold'])
    for ipaddress in dns_server_list[server_name].keys():
      # Create a new resolver to use for completing a DNS request, this will test each server for accessibility
      testing_resolver = dns.resolver.Resolver()
      testing_resolver.lifetime = dns_timeout
      try:
        testing_resolver.nameservers = [ipaddress]
        start_time = time.time();
        result = testing_resolver.resolve('google.com')
        elapsed_time_ms = int((time.time() - start_time)*1000);
        result_text = colored("Up", 'green')
        result_text = ("%s\t%s ms"%(result_text,elapsed_time_ms))
        # Append the elapsed time to the array
        dns_server_list[server_name][ipaddress].append(elapsed_time_ms)
      except DNSException:
        result_text = colored("timeout", 'red')
        # Append the timeout value to the array
        dns_server_list[server_name][ipaddress].append(0)
      except:
        result_text = colored("unknown", 'red')
        # Append the timeout value to the array
        dns_server_list[server_name][ipaddress].append(0)
      # Pretty Printou
      if(len(ipaddress) < 8):
        print("\t%s\t\t%s"%(ipaddress,result_text))
      else:
        print("\t%s\t%s"%(ipaddress,result_text))
  return dns_server_list

"""
  Execute the script.
"""
location = "unspecified"
if(len(sys.argv) > 1):
  location = sys.argv[1]

dns_servers_working = load_dns_data_structures(location)

print(colored("-- DNS Servers --", "white", attrs=['bold']))
dns_servers_working = test_dns_servers(dns_servers_working, dns_query_timeout_in_seconds)
print("\n")

store_dns_data_structures(dns_servers_working, location)
