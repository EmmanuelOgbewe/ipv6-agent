#!/usr/bin/env python3
import time
import socket
import subprocess
from datetime import datetime
import requests
import psutil

# Define the sleep interval in seconds
SLEEP_INTERVAL = 10
HOSTNAME = socket.gethostname() 

def is_ipv6_enabled():
  if psutil.POSIX and psutil.LINUX:
    try:
      output = subprocess.check_output(
          ['sysctl', '-n',
           'net.ipv6.conf.all.disable_ipv6']).decode('utf-8').strip()
      return output == '0'
    except subprocess.CalledProcessError:
      return False
  elif psutil.POSIX and psutil.MACOS:
    try:
      output = subprocess.check_output(['networksetup', '-getinfo',
                                        'Wi-Fi']).decode('utf-8')
      return "IPv6: Automatic" in output
    except subprocess.CalledProcessError:
      return False
  else:
    # Unsupported platform
    return False


# Function to get IPv6 addresses
def get_ipv6_addresses():
  ipv6_addresses = []
  try:
    # Get network interface information using psutil
    interfaces = psutil.net_if_addrs()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for interface_name, interface_addresses in interfaces.items():
      for addr in interface_addresses:
        if addr.family == socket.AddressFamily.AF_INET6:
          ipv6_addresses.append(addr.address.split('%')[0])
  except Exception as e:
    print(f"{timestamp} - Error getting IPv6 addresses for {HOSTNAME}: {e}")
  return ipv6_addresses


# Function to send IPv6 addresses to server
def send_ipv6_addresses(ipv6_addresses):
  try:
    print(ipv6_addresses)
    # Replace 'http://localhost:5000' with the URL of your server
    url = 'http://localhost:5000/ipv6'
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {'ipv6_addresses': ipv6_addresses, 'hostname': HOSTNAME, 'timestamp': str(datetime.now())}
    response = requests.post(url, json=data)
    response.raise_for_status()  # Raise an exception for non-200 status codes
    print(f"{timestamp} - {HOSTNAME} IPv6 addresses sent successfully.")
  except requests.exceptions.RequestException as e:
    print(f"{timestamp} - Error sending IPv6 addresses from {HOSTNAME}: {e}")


# Function to send notification to server if IPv6 is not enabled on the system
def send_ipv6_not_enabled_notification():
  try:
    # Replace 'http://localhost:5000' with the URL of your server
    url = 'http://localhost:5000/ipv6/not-enabled'
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        'message': 'IPv6 is not enabled on the system',
        'hostname': HOSTNAME,
        'timestamp': str(datetime.now())
    }
    response = requests.post(url, json=data)
    response.raise_for_status()  # Raise an exception for non-200 status codes
    print(f"{timestamp} - IPv6 not enabled on {HOSTNAME}, notification sent to server.")
  except requests.exceptions.RequestException as e:
    print(f"{timestamp} - {HOSTNAME} error sending notification: {e}")


# A helper to get a well formatted output of the system network information
def get_network_interfaces():
  # Get a list of network interfaces
  net_ifs = psutil.net_if_addrs()

  # Construct a string to represent the network interface information
  output = ""
  for interface, addresses in net_ifs.items():
    output += f"Interface: {interface}\n"
    for address in addresses:
      if address.family == socket.AddressFamily.AF_INET6:  # Check if address family is IPv=6
        output += f"{address.family.name}: {address.address}\n"
    output += "\n"

  # Print or process the output as needed
  return output


def run():
  if is_ipv6_enabled():
    ipv6_addresses = get_ipv6_addresses()
    if ipv6_addresses:
      send_ipv6_addresses(ipv6_addresses)
  else:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} - IPv6 not enabled for {HOSTNAME}")
    send_ipv6_not_enabled_notification()
    exit()


# Main function
def main():
  #print network configuration
  timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  print(f"{timestamp} -  Network configuration for {HOSTNAME}: {get_network_interfaces()}")
  while True:
    run()
    time.sleep(
        SLEEP_INTERVAL)  # Sleep for the defined interval before updating again


if __name__ == '__main__':
  main()
