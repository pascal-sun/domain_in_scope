# Domain in scope

`domain_in_scope` is a Python script to check if a domain is in scope from a list of IP addresses. 

#### Use cases

- You have a list of IP addresses that belong to you, and you want to check if a list of domains are hosted on these IP addresses.

## Prerequisites

- Python3
- Only use Python’s standard libraries, there is no need to install specific libraries

## Installation

```console
$ git clone https://github.com/pascal-sun/domain_in_scope.git
$ cd domain_in_scope
```

## Usage
![Demo](https://github.com/pascal-sun/domain_in_scope/blob/main/domain_in_scope_demo.gif)

#### Specifying a domain file and an IP file
```console
$ python domain_in_scope.py --domains <DOMAIN FILE PATH> --ips <IP FILE PATH>
```
With:
- `<DOMAIN FILE PATH>` path to file containing a list of domain to check (one domain per line)
- `<IP FILE PATH>` path to file containing a list of IP address (one per line, can be an IP address or a CIDR)

The list of domain can be also piped via stdin:
```console
$ cat <DOMAIN FILE PATH> | python domain_in_scope.py --ips <IP FILE PATH>
```

#### Display domains from scope only with `--silent`
```console
$ python domain_in_scope.py --domains domains.txt --ips ips.txt --silent
```

#### Directly from subdomains enumeration tools
```console
$ subfinder -d google.com -silent | python domain_in_scope.py --ips google_ips.txt --silent
$ amass enum -d google.com -nocolor 2>/dev/null | python domain_in_scope.py --ips google_ips.txt --silent
$ sublist3r -d google.io | python domain_in_scope.py --ips google_ips.txt --silent
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
