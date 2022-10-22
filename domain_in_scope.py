import ipaddress
import socket
import sys
import logging
import threading
import argparse

# Color output
COLORS = {
    "grey": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "white": 37
}
def colored(text: str, color: str) -> str:
    """Colorize text with ANSI escape sequences."""
    return f"\033[{COLORS[color]}m{text}\033[0m"

class LookupThread(threading.Thread):
    def __init__(self, domain, result):
        self.domain = domain
        self.result = result
        threading.Thread.__init__(self)

    def run(self):
        self.lookup(self.domain, ips_list)

    def lookup(self, domain, ips_list):
        """Try to find the IPs of a domain

        Returns a dict:
            {domain: {"ips": [ip1, ip2], "error": ""}
        If host is not found, then the dict will hold:
            {domain: {"ips": [], "error": "error message"}
        """

        try:
            hostname, aliaslist, ipaddrlist = socket.gethostbyname_ex(domain)
        except Exception as e:
            self.result[domain] = {"ips": [], "error": str(e)}
            if IS_SILENT:
                pass
            else:
                print(f"{colored('[!]', 'yellow')} {domain}: {colored(str(e), 'yellow')}")
        else:
            self.result[domain] = {"ips": ipaddrlist, "error": ""}
            intersection = ips_list.intersection(set(ipaddrlist))
            if intersection:
                res_ipaddrlist = ipaddrlist.copy()
                for i in range(len(res_ipaddrlist)):
                    if res_ipaddrlist[i] in intersection:
                        res_ipaddrlist[i] = colored(res_ipaddrlist[i], "green")
                if IS_SILENT:
                    print(domain)
                else:
                    print(f"{colored('[+]', 'green')} {domain}: {', '.join(res_ipaddrlist)}")
            else:
                if IS_SILENT:
                    pass
                else:
                    print(f"{colored('[-]', 'red')} {domain}: {', '.join(ipaddrlist)}")

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog="domain_in_scope",
        description="Return domains in IP addresses scope",
        allow_abbrev=False
    )
    parser.add_argument(
        '--domains',
        nargs='?',
        type=argparse.FileType('r'),
        default=(None if sys.stdin.isatty() else sys.stdin),
        help='path to domains list')
    parser.add_argument(
        '--ips',
        nargs='?',
        type=argparse.FileType('r'),
        required=True,
        help='path to IP addresses list')
    parser.add_argument(
        '--silent',
        help="be silent and return only domains in scope",
        action="store_true"
    )
    args = parser.parse_args()
    ips_file = args.ips
    domains_file = args.domains
    if not args.domains:
        sys.exit("Please provide an input file, or pipe it via stdin")
    IS_SILENT = args.silent

    # List IP address from ips_file
    ips_list = set()
    lines = ips_file.read().splitlines()
    # import pdb; pdb.set_trace()
    for line in lines:
        ips_list.update([str(ip) for ip in ipaddress.IPv4Network(line)])

    # Check if domains is in IP address list
    domains_lookup_res = {}
    lookup_threads = []
    lines = domains_file.read().splitlines()
    for line in lines:
        lookup_threads.append(LookupThread(line, domains_lookup_res))

    # Start the threads
    for t in lookup_threads:
        t.start()
