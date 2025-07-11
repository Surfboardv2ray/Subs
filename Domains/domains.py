import json
import socket

def extract_domains(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    domains = []
    if 'data' in data and isinstance(data['data'], list):
        for item in data['data']:
            domain = item.get('domain', '')
            if domain:
                try:
                    # Attempt to resolve the domain to an IP address
                    ip_address = socket.gethostbyname(domain)
                    print(f"Domain: {domain}, IP Address: {ip_address}")
                    domains.append(domain)
                except (socket.gaierror, socket.error):
                    # Skip if the domain can't be resolved
                    print(f"Skipping domain: {domain}, couldn't be resolved")

    with open(output_file, 'w') as f:
        for domain in domains:
            f.write(f"{domain}\n")

if __name__ == "__main__":
    extract_domains('Domains/input.json', 'Domains/output.txt')
