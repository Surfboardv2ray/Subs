import base64
import json

# Global variable to keep track of processed proxies
proxy_counter = 0

def rename_vmess_address(proxy, new_address):
    global proxy_counter
    base64_str = proxy.split('://')[1]
    missing_padding = len(base64_str) % 4
    if missing_padding:
        base64_str += '=' * (4 - missing_padding)
    try:
        decoded_str = base64.b64decode(base64_str).decode('utf-8')
        print("Decoded VMess proxy JSON:", decoded_str)  # Debugging
        proxy_json = json.loads(decoded_str)
        proxy_json['add'] = new_address
        proxy_json['ps'] = new_address  # Set remarks to new address
        proxy_counter += 1
        encoded_str = base64.b64encode(json.dumps(proxy_json).encode('utf-8')).decode('utf-8')
        renamed_proxy = 'vmess://' + encoded_str
        print("Renamed VMess proxy:", renamed_proxy)  # Debugging
        return renamed_proxy
    except Exception as e:
        print("Error processing VMess proxy: ", e)
        return None

def rename_vless_address(proxy, new_address):
    global proxy_counter
    try:
        parts = proxy.split('@')
        userinfo = parts[0]
        hostinfo = parts[1].split('#')[0]
        hostinfo_parts = hostinfo.split(':')
        hostinfo_parts[0] = new_address
        hostinfo = ':'.join(hostinfo_parts)
        remarks = new_address  # Set remarks to new address
        renamed_proxy = userinfo + '@' + hostinfo + '#' + remarks
        proxy_counter += 1
        print("Renamed VLess proxy:", renamed_proxy)  # Debugging
        return renamed_proxy
    except Exception as e:
        print("Error processing VLess proxy: ", e)
        return None

def rename_trojan_address(proxy, new_address):
    global proxy_counter
    try:
        parts = proxy.split('@')
        userinfo = parts[0]
        hostinfo = parts[1].split('#')[0]
        hostinfo_parts = hostinfo.split(':')
        hostinfo_parts[0] = new_address
        hostinfo = ':'.join(hostinfo_parts)
        remarks = new_address  # Set remarks to new address
        renamed_proxy = userinfo + '@' + hostinfo + '#' + remarks
        proxy_counter += 1
        print("Renamed Trojan proxy:", renamed_proxy)  # Debugging
        return renamed_proxy
    except Exception as e:
        print("Error processing Trojan proxy: ", e)
        return None

def process_proxies(input_file, ips_file, output_file):
    # Read all proxy configurations from config.txt
    with open(input_file, 'r') as f:
        proxies = [line.strip() for line in f.readlines() if line.strip()]

    # Read the list of IP addresses, skipping lines that start with "//"
    with open(ips_file, 'r') as ip_f:
        ips = [line.strip() for line in ip_f.readlines() if not line.strip().startswith("//")]

    # Process each configuration with each IP address
    with open(output_file, 'w') as out_f:
        for proxy in proxies:
            for ip in ips:
                if proxy.startswith('vmess://'):
                    renamed_proxy = rename_vmess_address(proxy, ip)
                elif proxy.startswith('vless://'):
                    renamed_proxy = rename_vless_address(proxy, ip)
                elif proxy.startswith('trojan://'):
                    renamed_proxy = rename_trojan_address(proxy, ip)

                if renamed_proxy is not None:
                    out_f.write(renamed_proxy + '\n')

# Example usage
input_file = 'IPTest/config.txt'
ips_file = 'IPTest/ips.txt'
output_file = 'IPTest/output'

process_proxies(input_file, ips_file, output_file)

# Append extra configurations from extra.txt to the output file
extra_file = 'IPTest/extra.txt'
try:
    with open(extra_file, 'r') as extra_f:
        extra_configs = [line for line in extra_f.readlines() if line.strip()]
    with open(output_file, 'a') as out_f:
        for config in extra_configs:
            out_f.write(config.rstrip('\n') + '\n')
except Exception as e:
    print("Error appending extra configurations: ", e)
