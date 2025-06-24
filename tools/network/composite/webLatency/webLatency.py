import time
import sys

dependency_fail = False

try:
  from termcolor import colored, cprint
except:
  print("Please install Python 3 version of termcolor package using:\n\n\tpip install termcolor\n\n")
  dependency_fail = True

try:
  from urllib import request
  from urllib import error
except:
  print("Please install Python 3 version of urllib package using:\n\n\tpip install urllib\n\n")
  dependency_fail = True

if dependency_fail is True:
  sys.exit(-1)

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
  'mastadon.com' : [],
  'netflix.com' : [],
  'nytimes.com' : [],
  'paypal.com' : [],
  'pinterest.com' : [],
  'tumblr.com' : [],
  'whatsapp.com' : [],
  'wikipedia.org' : [],
  'youtube.com' : [],
  'zoho.com' : []
}

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

web_servers_working = load_web_data_structures(location)

print(colored("-- Web Servers --", "white", attrs=['bold']))
web_servers_working = test_web_servers(web_servers_working)
print("\n")

store_web_data_structures(web_servers_working, location)
