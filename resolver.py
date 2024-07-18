#!/usr/bin/python3

# Программа для перобразования dns имен (fqdn) в ip адреса, ввод имен происходит из списков самой программы
# NAMES. После преобразования пишутся в скрипты, используемые параметром client-connect на сервере OpenVPN. 

import sys
from typing import List
from dns import resolver
from datetime import datetime

timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

NAMESERVERS = ['1.1.1.1', '8.8.8.8']
NAMES = ['ya.ru','mail.ru',]

def get_ip(domain: str) -> List[str]:
    try:
        ip_list = []
        resolver_ = resolver.Resolver(configure=False)
        for server in NAMESERVERS:
            resolver_.nameservers = [server]
            result = resolver_.resolve(str(domain), 'A')
            for i in result:
                if str(i) not in ip_list:
                    ip_list.append(i.to_text())
        return ip_list
    except: pass

def resolve(domain_names: List[str]) -> List[str]:
    addr = []
    config = []
    for name in domain_names:
        ip_list = get_ip(name)
        if ip_list != None:
            for ip in ip_list:
                if str(ip) not in config:
                    config.append(ip)
                    addr.append(f'{ip}' )
    sys.stdout.write(f'{timestamp} Success resolved: {config}\n')
    return addr

def update_script(insert_list, start_line, end_line, lines):
    start = lines.index(start_line)
    end = lines.index(end_line) + 1
    return lines[:start + 1] + insert_list + lines[end - 1:]

def ip_to_bash(command: str = None, ip_addrs: List[str] = None) -> List[str]:
    try:
        if command == 'echo_with_bits_mask':
            result_list = []
            for i in ip_addrs:
                i = 'echo "push \\"route ' + str(i) + ' 255.255.255.255\\"" >> $1\n'
                result_list.append(i)
            return result_list

        else: sys.stdout.write(f'{timestamp} Warning: looks like ip_to_bash arg command: str = None.\n')

    except Exception as e: 
        sys.stdout.write(f'{timestamp} Error with ip_to_com module: {e}\n')
        

def renderer(people: List[str] = None, core_ru: List[str] = None, core_eu: List[str] = None):
    try:
        with open('/etc/openvpn/scripts/routes.sh', 'r') as f:
            lines = f.readlines()
        sys.stdout.write(f'{timestamp} Success readed lines script /etc/openvpn/scripts/routes.sh.\n')

        lines = update_script(ip_to_bash(command="echo_with_bits_mask", ip_addrs=people), "# START NAMES\n", "# FINISH NAMES\n", lines)
        with open('/etc/openvpn/scripts/routes.sh', 'w') as f:
            f.writelines(lines)
        sys.stdout.write(f'{timestamp} Success wrote updates in /etc/openvpn/scripts/routes.sh.\n')

    except Exception as e:
        sys.stdout.write(f'{timestamp} Error, can not wrote updates in /etc/openvpn/scripts/(people/core). Error: {str(e)}\n')
    
def main():
    sys.stdout.write(f'{timestamp} [Resolver] - starting work.\n')

    people_addr = resolve(NAMES)
    
    sys.stdout.write(f'{timestamp} [Worker] - working with resolve and assist file.\n')
    renderer(people = people_addr)

    sys.stdout.write(f'{timestamp} [Resolver] - work finished.\n')

if __name__ == "__main__":
    main()
