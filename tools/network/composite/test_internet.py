"""
  ---
  The purpose of this script is to provide a tool to test the condition of the internet that you care about. This script
  will eventually test the following types of nodes:

    * DNS Servers
    * Certificate Authority Servers
    * Mail Servers
    * General Websites

  === DNS
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

try:
  from urllib import request
  from urllib import error
except:
  print("Please install Python 3 version of urllib package using:\n\n\tpip install urllib\n\n")
  dependency_fail = True

if dependency_fail is True:
  sys.exit(-1)

dns_query_timeout_in_seconds = 1
dns_servers_blank = {
  'Alternate DNS11'     : {
    '198.101.242.72'    : [],
    '23.253.163.53'     : []
  },
  'censurfridns.dk13'   : {
    '91.239.100.100'    : []
  },
  'CenturyLink'         : {
    '205.171.2.26'      : [],
    '205.171.2.65'      : [],
    '205.171.3.65'      : []
  },
  'Comodo Secure DNS'   : {
    '8.26.56.26'        : [],
    '8.20.247.20'       : []
  },
  'DNS Advantage'       : {
    '156.154.70.1'      : [],
    '156.154.71.1'      : []
  },
  'DNS.WATCH4'          : {
    '84.200.69.80'      : [],
    '84.200.70.40'      : []
  },
  'Dyn'                 : {
    '216.146.35.35'     : [],
    '216.146.36.36'     : []
  },
  'FreeDNS10'           : {
    '37.235.1.174'      : [],
    '37.235.1.177'      : []
  },
  'Google3'             : {
    '8.8.8.8'           : [],
    '8.8.4.4'           : []
  },
  'GreenTeamDNS7'       : {
    '81.218.119.11'     : [],
    '209.88.198.133'    : []
  },
  'Hurricane Electric14' : {
    '74.82.42.42'        : []
  },
  'Level31'             : {
    '209.244.0.3'       : [],
    '209.244.0.4'       : []
  },
  'Norton ConnectSafe6' : {
    '199.85.126.10'     : [],
    '199.85.127.10'     : []
  },
  'OpenDNS Home5'       : {
    '208.67.222.222'    : [],
    '208.67.220.220'    : []
  },
  'puntCAT15'            : {
    '109.69.8.51'        : []
  },
  'SafeDNS8'            : {
    '195.46.39.39'      : [],
    '195.46.39.40'      : []
  },
  'Verisign2'           : {
    '64.6.64.6'         : [],
    '64.6.65.6'         : []
  },
  'Yandex.DNS12'        : {
    '77.88.8.8'         : [],
    '77.88.8.1'         : []
  }
}

web_servers_blank = {
  'apple.com' : [],
  'bbc.co.uk' : [],
  'ebay.com' : [],
  'facebook.com' : [],
  'fivethirtyeight.com' : [],
  'github.com' : [],
  'goodreads.com' : [],
  'google.com' : [],
  'ifixit.com' : [],
  'imgur.com' : [],
  'netflix.com' : [],
  'nytimes.com' : [],
  'paypal.com' : [],
  'pinterest.com' : [],
  'shopify.com' : [],
  'tumblr.com' : [],
  'twitter.com' : [],
  'whatsapp.com' : [],
  'wikipedia.org' : [],
  'youtube.com' : [],
  'zoho.com' : []
}

ping_servers = [
  'cnn.com',
  'etsy.com',
  'reddit.com'
]

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
    return(dns_servers_blank)

def load_web_data_structures(location):
  """
    This function will attempt to load/read the stored DNS and Web server JSON objects from the same directory that the
    script was launched from. If no file is found, the default will be used.
  """
  import json
  try:
    filename = '.'+location+'_web.json'
    with open(filename, 'r') as fp:
      return(json.load(fp))
  except:
    print("Web JSON File does not exist, using default.")
    return(web_servers_blank)

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

def store_web_data_structures(web_servers, location):
  """
    This function will store the modified DNS server structure as a JSON object in the same directory that the script
    was launched from.
  """
  import json
  try:
    filename = '.'+location+'_web.json'
    with open(filename, 'w') as fp:
      json.dump(web_servers, fp)
  except:
    print("Web JSON File could not be stored.")

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
        result = testing_resolver.query('google.com')
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

def test_web_servers(web_server_list):
  for server_name in web_server_list.keys():
    req = request.Request(('https://www.'+server_name))
    try: 
      start_time = time.time();
      reponse = request.urlopen(req)
      elapsed_time_ms = int((time.time() - start_time)*1000);
      result_text = colored("good", 'green')
      result_text = ("%s\t%s ms"%(result_text,elapsed_time_ms))
      # Append the elapsed time to the array
      web_server_list[server_name].append(elapsed_time_ms)
    except:
      result_text = colored("unreachable", 'red')
      # Append the timeout value to the array
      web_server_list[server_name].append(0)
    if(len(server_name) < 8):
      server_name = colored(server_name, 'white', attrs=['bold'])
      print("%s\t\t\t%s"%(server_name,result_text))
    elif(len(server_name) < 16):
      server_name = colored(server_name, 'white', attrs=['bold'])
      print("%s\t\t%s"%(server_name,result_text))
    else:
      server_name = colored(server_name, 'white', attrs=['bold'])
      print("%s\t%s"%(server_name,result_text))
  return web_server_list

"""
  Execute the script.
"""
location = "unspecified"
if(len(sys.argv) > 1):
  location = sys.argv[1]

dns_servers_working = load_dns_data_structures(location)
web_servers_working = load_web_data_structures(location)

print(colored("-- DNS Servers --", "white", attrs=['bold']))
dns_servers_working = test_dns_servers(dns_servers_working, dns_query_timeout_in_seconds)
print("\n")
print(colored("-- Web Servers --", "white", attrs=['bold']))
web_servers_working = test_web_servers(web_servers_working)
print("\n")

store_dns_data_structures(dns_servers_working, location)
store_web_data_structures(web_servers_working, location)
