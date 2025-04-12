from colorama import Fore, Style, init
init(autoreset=True)

banner = f"""{Fore.RED}
██████████                       █████      ██████████              █████                                  █████   
░░███░░░░███                     ░░███      ░░███░░░░░█             ░░███                                  ░░███    
 ░███   ░░███  ██████   ████████  ░███ █████ ░███  █ ░  █████ █████ ███████   ████████   ██████    ██████  ███████  
 ░███    ░███ ░░░░░███ ░░███░░███ ░███░░███  ░██████   ░░███ ░░███ ░░░███░   ░░███░░███ ░░░░░███  ███░░███░░░███░   
 ░███    ░███  ███████  ░███ ░░░  ░██████░   ░███░░█    ░░░█████░    ░███     ░███ ░░░   ███████ ░███ ░░░   ░███    
 ░███    ███  ███░░███  ░███      ░███░░███  ░███ ░   █  ███░░░███   ░███ ███ ░███      ███░░███ ░███  ███  ░███ ███
 ██████████  ░░████████ █████     ████ █████ ██████████ █████ █████  ░░█████  █████    ░░████████░░██████   ░░█████ 
░░░░░░░░░░    ░░░░░░░░ ░░░░░     ░░░░ ░░░░░ ░░░░░░░░░░ ░░░░░ ░░░░░    ░░░░░  ░░░░░      ░░░░░░░░  ░░░░░░     ░░░░░  
BY AHMAD JOUMAA
{Style.RESET_ALL}
"""

print(banner)




import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import time
import random
from colorama import Fore, Style, init
from datetime import datetime

# Initialize colorama
init(autoreset=True)

# List of darknet sites from a user-supplied file
def get_darknet_sites_from_file(file_path):
    sites = []
    try:
        with open(file_path, "r") as f:
            for line in f:
                site = line.strip()
                if site:
                    sites.append(site)
        return sites
    except FileNotFoundError:
        print(Fore.RED + "The specified file was not found.")
        return []

# HTTP headers to blend in with normal traffic
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

# Proxy settings to route through Tor via SOCKS5
proxies = {
    "http": "socks5h://127.0.0.1:9050",
    "https": "socks5h://127.0.0.1:9050"
}

# File to store the results
output_file = "darknet_leaks.txt"

def scrape_leaks(site):
    try:
        print(Fore.CYAN + f"Visiting {site}...")
        response = requests.get(site, headers=headers, proxies=proxies, timeout=15)
        response.raise_for_status()  # Check if the request was successful
        
        soup = BeautifulSoup(response.text, "html.parser")
        leak_data = []
        
        # Extract links and text from relevant elements
        for element in soup.find_all(["a", "p", "pre", "code"]):
            if element.text.strip():
                leak_data.append(element.text.strip())
            if element.get("href"):
                leak_data.append(urljoin(site, element["href"]))
        
        return leak_data
    
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Failed to access {site}: {e}")
        return []

def save_leaks(leaks, site):
    with open(output_file, "a", encoding="utf-8") as f:
        # Add site URL and timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"\n{'='*50}\n")
        f.write(f"Site: {site}\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"{'='*50}\n")
        
        # Add the leak data
        for leak in leaks:
            f.write(f"{leak}\n")
        
        f.write(f"{'='*50}\n")
    print(Fore.GREEN + f"Saved {len(leaks)} entries to {output_file}")

def main():
    file_path = input(Fore.YELLOW + "Enter the path to your .txt file with darknet site URLs: ")
    darknet_sites = get_darknet_sites_from_file(file_path)
    
    if not darknet_sites:
        print(Fore.RED + "No valid sites to scrape. Exiting.")
        return
    
    if os.path.exists(output_file):
        os.remove(output_file)  # Clean slate if output file exists
    
    # Loop through each site and scrape it
    for i, site in enumerate(darknet_sites, 1):
        print(Fore.YELLOW + f"Currently processing link {i}/{len(darknet_sites)}: {site}")
        leaks = scrape_leaks(site)
        if leaks:
            save_leaks(leaks, site)
        print(Fore.GREEN + f"Successfully extracted data from {site}")
        time.sleep(random.uniform(3, 7))  # Random delay between requests to avoid blocking

if __name__ == "__main__":
    print(Fore.MAGENTA + "Starting darknet search...")
    main()
    print(Fore.MAGENTA + "Finished collecting data.")
