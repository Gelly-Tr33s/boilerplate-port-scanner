import socket
import re
from common_ports import ports_and_services

def get_open_ports(target, port_range, verbose=False):
    open_ports = []

    try:
        ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')

        if ip_pattern.match(target):
            parts = target.split('.')
            for part in parts:
                if int(part) > 255:
                    return "Error: Invalid IP address"
            ip = target
        else:
            ip = socket.gethostbyname(target)

    except socket.gaierror:
        if re.search('[a-zA-Z]', target):
            return "Error: Invalid hostname"
        return "Error: Invalid IP address"
    except (socket.error, ValueError):
        return "Error: Invalid IP address"

    for port in range(port_range[0], port_range[1] + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3) 

        try:
            result = s.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
        except socket.error:
            pass
        except KeyboardInterrupt:
            s.close()
            return "Exiting program"
        finally:
            s.close()

    if not verbose:
        return open_ports

    hostname = None
    try:
        hostname = socket.gethostbyaddr(ip)[0]
    except (socket.herror, socket.gaierror):
        hostname = None

    if hostname and hostname != ip:
        result_str = f"Open ports for {hostname} ({ip})\n"
    else:
        result_str = f"Open ports for {ip}\n"

    result_str += "PORT     SERVICE\n"

    for port in open_ports:
        service_name = ports_and_services.get(port, "unknown")
        result_str += f"{port}{' ' * (9 - len(str(port)))}{service_name}\n"

    return result_str.rstrip()