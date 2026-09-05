#!/usr/bin/env python3

import argparse
import json
import os
import re
import shutil
import socket
import subprocess
import sys
from datetime import datetime
from urllib.parse import urlparse

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ============================================================
# SOLO RECON
# Web Reconnaissance & Attack Surface Mapping Tool
# ============================================================

VERSION = "3.0.0"
USER_AGENT = "SOLO-RECON/3.0"
TIMEOUT = 10

# Colors
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
WHITE = "\033[97m"


BANNER = f"""
{RED}{BOLD}
 ███████╗ ██████╗ ██╗      ██████╗
 ██╔════╝██╔═══██╗██║     ██╔═══██╗
 ███████╗██║   ██║██║     ██║   ██║
 ╚════██║██║   ██║██║     ██║   ██║
 ███████║╚██████╔╝███████╗╚██████╔╝
 ╚══════╝ ╚═════╝ ╚══════╝ ╚═════╝

 ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
 ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
 ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
 ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
 ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
 ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝
{RESET}
{WHITE}{BOLD}        Web Reconnaissance & Attack Surface Mapper{RESET}
{CYAN}                 SOLO RECON v{VERSION}{RESET}
"""


# ============================================================
# UI
# ============================================================

def banner():
    print(BANNER)


def section(title):
    print()
    print(f"{RED}{BOLD}[+] {title}{RESET}")
    print(f"{RED}{'-' * 65}{RESET}")


def log(message, level="INFO"):
    colors = {
        "INFO": CYAN,
        "OK": GREEN,
        "WARN": YELLOW,
        "ERROR": RED,
    }

    color = colors.get(level, WHITE)
    print(f"{color}[{level}]{RESET} {message}")


# ============================================================
# DOMAIN
# ============================================================

def normalize_domain(domain):
    domain = domain.strip()

    if "://" in domain:
        parsed = urlparse(domain)
        domain = parsed.netloc

    domain = domain.split("/")[0]
    domain = domain.split(":")[0]
    domain = domain.lower().strip()

    return domain


def validate_domain(domain):
    pattern = r"^(?=.{1,253}$)([a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,63}$"

    if not re.match(pattern, domain):
        return False

    return True


# ============================================================
# FILE SYSTEM
# ============================================================

class Workspace:

    def __init__(self, output, domain):

        self.base = os.path.join(output, domain)

        self.data = os.path.join(self.base, "data")
        self.logs = os.path.join(self.base, "logs")
        self.reports = os.path.join(self.base, "reports")

        os.makedirs(self.data, exist_ok=True)
        os.makedirs(self.logs, exist_ok=True)
        os.makedirs(self.reports, exist_ok=True)

    def path(self, filename):
        return os.path.join(self.data, filename)

    def report_path(self, filename):
        return os.path.join(self.reports, filename)


def save_text(path, data):

    with open(path, "w", encoding="utf-8") as f:

        if isinstance(data, list):
            f.write("\n".join(str(x) for x in data))

        else:
            f.write(str(data))


def save_json(path, data):

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# ============================================================
# COMMAND UTILITIES
# ============================================================

def command_exists(command):
    return shutil.which(command) is not None


def run_command(command, timeout=120):

    try:

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout
        )

        return result.stdout.strip()

    except subprocess.TimeoutExpired:

        log(f"Command timed out: {' '.join(command)}", "WARN")
        return ""

    except Exception as e:

        log(f"Command failed: {e}", "ERROR")
        return ""


# ============================================================
# CRT.SH
# ============================================================

def certificate_transparency(domain):

    section("Certificate Transparency")

    url = (
        "https://crt.sh/"
        f"?q=%25.{domain}"
        "&output=json"
    )

    subdomains = set()

    try:

        response = requests.get(
            url,
            headers={"User-Agent": USER_AGENT},
            timeout=TIMEOUT
        )

        if response.status_code != 200:

            log(
                f"crt.sh returned HTTP {response.status_code}",
                "WARN"
            )

            return []

        data = response.json()

        for item in data:

            names = item.get("name_value", "")

            for name in names.splitlines():

                name = name.strip().lower()

                name = name.lstrip("*.")

                if name == domain or name.endswith("." + domain):

                    subdomains.add(name)

        result = sorted(subdomains)

        log(f"Found {len(result)} certificate names", "OK")

        return result

    except Exception as e:

        log(f"Certificate Transparency error: {e}", "ERROR")

        return []


# ============================================================
# SUBDOMAIN ENUMERATION
# ============================================================

def subdomain_enumeration(domain):

    section("Subdomain Enumeration")

    found = set()

    # crt.sh
    for sub in certificate_transparency(domain):

        found.add(sub)

    # subfinder
    if command_exists("subfinder"):

        log("Running subfinder...", "INFO")

        output = run_command(
            [
                "subfinder",
                "-d",
                domain,
                "-silent"
            ],
            timeout=180
        )

        for line in output.splitlines():

            line = line.strip().lower()

            if line.endswith(domain):

                found.add(line)

    else:

        log(
            "subfinder not installed. Using crt.sh results only.",
            "WARN"
        )

    result = sorted(found)

    log(f"Total unique subdomains: {len(result)}", "OK")

    return result


# ============================================================
# DNS
# ============================================================

def dns_resolution(domain, subdomains):

    section("DNS Resolution")

    targets = [domain]

    for sub in subdomains:

        if sub not in targets:
            targets.append(sub)

    records = {}

    for host in targets:

        try:

            addresses = socket.gethostbyname_ex(host)[2]

            records[host] = sorted(set(addresses))

            log(
                f"{host} -> {', '.join(records[host])}",
                "OK"
            )

        except socket.gaierror:

            records[host] = []

            log(
                f"{host} -> DNS resolution failed",
                "WARN"
            )

    return records


def extract_ips(dns_records):

    ips = set()

    for addresses in dns_records.values():

        for ip in addresses:

            ips.add(ip)

    return sorted(ips)


# ============================================================
# HTTP PROBE
# ============================================================

def extract_title(html):

    match = re.search(
        r"<title[^>]*>(.*?)</title>",
        html,
        re.I | re.S
    )

    if not match:
        return ""

    title = re.sub(
        r"\s+",
        " ",
        match.group(1)
    ).strip()

    return title[:200]


def http_probe(subdomains):

    section("HTTP/HTTPS Probe")

    results = []

    session = requests.Session()

    session.headers.update(
        {
            "User-Agent": USER_AGENT
        }
    )

    for host in subdomains:

        for scheme in ["https", "http"]:

            url = f"{scheme}://{host}"

            try:

                response = session.get(
                    url,
                    timeout=TIMEOUT,
                    verify=False,
                    allow_redirects=True
                )

                title = extract_title(response.text)

                item = {
                    "input": url,
                    "url": response.url,
                    "status": response.status_code,
                    "content_length": len(response.content),
                    "server": response.headers.get(
                        "Server",
                        ""
                    ),
                    "title": title
                }

                results.append(item)

                log(
                    f"{response.status_code} "
                    f"{response.url} "
                    f"[{title}]",
                    "OK"
                )

                break

            except requests.RequestException:
                continue

    log(
        f"Live HTTP targets: {len(results)}",
        "OK"
    )

    return results


# ============================================================
# NMAP
# ============================================================

def port_scan(domain):

    section("Nmap Port Scan")

    if not command_exists("nmap"):

        log(
            "nmap is not installed.",
            "WARN"
        )

        return ""

    log(
        f"Running top 100 TCP ports against {domain}",
        "INFO"
    )

    output = run_command(
        [
            "nmap",
            "-Pn",
            "--top-ports",
            "100",
            "-T3",
            domain
        ],
        timeout=300
    )

    if output:

        log("Nmap scan completed.", "OK")

    return output


# ============================================================
# WAYBACK
# ============================================================

def wayback_urls(domain):

    section("Wayback URL Discovery")

    url = (
        "https://web.archive.org/cdx/search/cdx"
        f"?url=*.{domain}/*"
        "&output=json"
        "&fl=original"
        "&collapse=urlkey"
    )

    results = set()

    try:

        response = requests.get(
            url,
            headers={"User-Agent": USER_AGENT},
            timeout=30
        )

        if response.status_code != 200:

            log(
                f"Wayback returned HTTP {response.status_code}",
                "WARN"
            )

            return []

        try:

            data = response.json()

            for item in data:

                if isinstance(item, list):

                    for value in item:

                        if (
                            isinstance(value, str)
                            and value.startswith("http")
                        ):
                            results.add(value)

                elif isinstance(item, str):

                    if item.startswith("http"):
                        results.add(item)

        except ValueError:

            for line in response.text.splitlines():

                if line.startswith("http"):
                    results.add(line.strip())

        result = sorted(results)

        log(
            f"Wayback URLs found: {len(result)}",
            "OK"
        )

        return result

    except Exception as e:

        log(
            f"Wayback error: {e}",
            "WARN"
        )

        return []


# ============================================================
# SECURITY HEADERS
# ============================================================

def security_headers(http_results):

    section("Security Headers")

    results = []

    required_headers = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Content-Type-Options",
        "X-Frame-Options",
        "Referrer-Policy",
        "Permissions-Policy"
    ]

    for item in http_results:

        url = item["url"]

        try:

            response = requests.get(
                url,
                headers={"User-Agent": USER_AGENT},
                timeout=TIMEOUT,
                verify=False,
                allow_redirects=True
            )

            headers_lower = {
                key.lower(): value
                for key, value in response.headers.items()
            }

            missing = []

            for header in required_headers:

                if header.lower() not in headers_lower:

                    missing.append(header)

            results.append(
                {
                    "url": response.url,
                    "status": response.status_code,
                    "missing_headers": missing,
                    "headers": dict(response.headers)
                }
            )

            log(
                f"{response.url}: "
                f"{len(missing)} security headers missing",
                "OK"
            )

        except requests.RequestException as e:

            log(
                f"Header check failed for {url}: {e}",
                "WARN"
            )

    return results


# ============================================================
# NUCLEI
# ============================================================

def nuclei_scan(targets, workspace):

    section("Nuclei Scan")

    if not command_exists("nuclei"):

        log(
            "nuclei is not installed.",
            "WARN"
        )

        return ""

    if not targets:

        log(
            "No live targets available for Nuclei.",
            "WARN"
        )

        return ""

    target_file = workspace.path(
        "nuclei_targets.txt"
    )

    output_file = workspace.path(
        "nuclei.jsonl"
    )

    save_text(
        target_file,
        targets
    )

    log(
        f"Running Nuclei against {len(targets)} targets...",
        "INFO"
    )

    command = [
        "nuclei",
        "-l",
        target_file,
        "-jsonl",
        "-o",
        output_file,
        "-silent"
    ]

    output = run_command(
        command,
        timeout=600
    )

    if os.path.exists(output_file):

        log(
            f"Nuclei results saved: {output_file}",
            "OK"
        )

    else:

        log(
            "Nuclei produced no result file.",
            "WARN"
        )

    return output


# ============================================================
# RESULTS
# ============================================================

def save_results(workspace, results):

    section("Saving Results")

    save_text(
        workspace.path("subdomains.txt"),
        results["subdomains"]
    )

    save_json(
        workspace.path("dns.json"),
        results["dns"]
    )

    save_text(
        workspace.path("ips.txt"),
        results["ips"]
    )

    save_json(
        workspace.path("http.json"),
        results["http"]
    )

    save_text(
        workspace.path("live_urls.txt"),
        [
            item["url"]
            for item in results["http"]
        ]
    )

    save_text(
        workspace.path("wayback_urls.txt"),
        results["wayback"]
    )

    save_json(
        workspace.path("security_headers.json"),
        results["headers"]
    )

    save_text(
        workspace.path("nmap.txt"),
        results["nmap"]
    )

    log(
        "All reconnaissance data saved.",
        "OK"
    )


# ============================================================
# JSON REPORT
# ============================================================

def create_report(workspace, domain, results):

    section("Creating JSON Report")

    report = {
        "tool": "SOLO RECON",
        "version": VERSION,
        "domain": domain,
        "timestamp": datetime.utcnow().isoformat() + "Z",

        "summary": {
            "subdomains": len(
                results["subdomains"]
            ),

            "ips": len(
                results["ips"]
            ),

            "live_http": len(
                results["http"]
            ),

            "wayback_urls": len(
                results["wayback"]
            )
        },

        "results": results
    }

    path = workspace.report_path(
        "report.json"
    )

    save_json(
        path,
        report
    )

    log(
        f"Report created: {path}",
        "OK"
    )


# ============================================================
# FULL RECON
# ============================================================

def run_full_recon(domain, workspace):

    section("FULL SOLO RECON")

    results = {
        "subdomains": [],
        "dns": {},
        "ips": [],
        "http": [],
        "wayback": [],
        "headers": [],
        "nmap": "",
        "nuclei": ""
    }

    # 1. Subdomains
    results["subdomains"] = subdomain_enumeration(
        domain
    )

    if domain not in results["subdomains"]:

        results["subdomains"].insert(
            0,
            domain
        )

    # 2. DNS
    results["dns"] = dns_resolution(
        domain,
        results["subdomains"]
    )

    # 3. IPs
    results["ips"] = extract_ips(
        results["dns"]
    )

    # 4. HTTP
    results["http"] = http_probe(
        results["subdomains"]
    )

    # 5. Nmap
    results["nmap"] = port_scan(
        domain
    )

    # 6. Wayback
    results["wayback"] = wayback_urls(
        domain
    )

    # 7. Headers
    results["headers"] = security_headers(
        results["http"]
    )

    # 8. Nuclei
    live_urls = [
        item["url"]
        for item in results["http"]
    ]

    results["nuclei"] = nuclei_scan(
        live_urls,
        workspace
    )

    # Save
    save_results(
        workspace,
        results
    )

    create_report(
        workspace,
        domain,
        results
    )

    return results


# ============================================================
# PASSIVE RECON
# ============================================================

def run_passive(domain, workspace):

    section("PASSIVE SOLO RECON")

    results = {
        "subdomains": [],
        "dns": {},
        "ips": [],
        "http": [],
        "wayback": [],
        "headers": [],
        "nmap": "",
        "nuclei": ""
    }

    results["subdomains"] = (
        subdomain_enumeration(domain)
    )

    if domain not in results["subdomains"]:

        results["subdomains"].insert(
            0,
            domain
        )

    results["dns"] = dns_resolution(
        domain,
        results["subdomains"]
    )

    results["ips"] = extract_ips(
        results["dns"]
    )

    results["wayback"] = wayback_urls(
        domain
    )

    save_results(
        workspace,
        results
    )

    create_report(
        workspace,
        domain,
        results
    )

    return results


# ============================================================
# INDIVIDUAL MODULES
# ============================================================

def run_subdomains(domain, workspace):

    subdomains = subdomain_enumeration(
        domain
    )

    save_text(
        workspace.path("subdomains.txt"),
        subdomains
    )

    return subdomains


def run_dns(domain, workspace):

    subdomains = subdomain_enumeration(
        domain
    )

    dns = dns_resolution(
        domain,
        subdomains
    )

    save_json(
        workspace.path("dns.json"),
        dns
    )

    ips = extract_ips(dns)

    save_text(
        workspace.path("ips.txt"),
        ips
    )

    return dns


def run_http(domain, workspace):

    subdomains = subdomain_enumeration(
        domain
    )

    results = http_probe(
        subdomains
    )

    save_json(
        workspace.path("http.json"),
        results
    )

    save_text(
        workspace.path("live_urls.txt"),
        [
            x["url"]
            for x in results
        ]
    )

    return results


def run_urls(domain, workspace):

    urls = wayback_urls(
        domain
    )

    save_text(
        workspace.path("wayback_urls.txt"),
        urls
    )

    return urls


def run_headers(domain, workspace):

    subdomains = subdomain_enumeration(
        domain
    )

    http_results = http_probe(
        subdomains
    )

    headers = security_headers(
        http_results
    )

    save_json(
        workspace.path("security_headers.json"),
        headers
    )

    return headers


def run_nmap(domain, workspace):

    output = port_scan(
        domain
    )

    save_text(
        workspace.path("nmap.txt"),
        output
    )

    return output


def run_nuclei(domain, workspace):

    subdomains = subdomain_enumeration(
        domain
    )

    http_results = http_probe(
        subdomains
    )

    targets = [
        x["url"]
        for x in http_results
    ]

    return nuclei_scan(
        targets,
        workspace
    )


# ============================================================
# ARGUMENT PARSER
# ============================================================

def build_parser():

    parser = argparse.ArgumentParser(

        prog="solo-recon",

        description=(
            "SOLO RECON - Web Reconnaissance "
            "& Attack Surface Mapper"
        ),

        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "-d",
        "--domain",
        required=True,
        help="Target domain, e.g. example.com"
    )

    parser.add_argument(
        "-o",
        "--output",
        default="output",
        help="Output directory (default: output)"
    )

    parser.add_argument(
        "--full",
        action="store_true",
        help="Run complete reconnaissance"
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Alias for --full"
    )

    parser.add_argument(
        "--passive",
        action="store_true",
        help="Run passive reconnaissance"
    )

    parser.add_argument(
        "--subdomains",
        action="store_true",
        help="Enumerate subdomains"
    )

    parser.add_argument(
        "--dns",
        action="store_true",
        help="Resolve DNS records"
    )

    parser.add_argument(
        "--http",
        action="store_true",
        help="Probe HTTP/HTTPS services"
    )

    parser.add_argument(
        "--urls",
        action="store_true",
        help="Discover historical URLs"
    )

    parser.add_argument(
        "--headers",
        action="store_true",
        help="Analyze security headers"
    )

    parser.add_argument(
        "--nmap",
        action="store_true",
        help="Run Nmap top-100 TCP scan"
    )

    parser.add_argument(
        "--nuclei",
        action="store_true",
        help="Run Nuclei vulnerability templates"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"SOLO RECON {VERSION}"
    )

    return parser


# ============================================================
# MAIN
# ============================================================

def main():

    banner()

    parser = build_parser()

    args = parser.parse_args()

    domain = normalize_domain(
        args.domain
    )

    if not validate_domain(domain):

        log(
            f"Invalid domain: {domain}",
            "ERROR"
        )

        sys.exit(1)

    workspace = Workspace(
        args.output,
        domain
    )

    log(
        f"Target: {domain}",
        "INFO"
    )

    log(
        f"Workspace: {workspace.base}",
        "INFO"
    )

    # FULL
    if args.full or args.all:

        run_full_recon(
            domain,
            workspace
        )

        return

    # PASSIVE
    if args.passive:

        run_passive(
            domain,
            workspace
        )

        return

    # Individual modules
    if args.subdomains:

        run_subdomains(
            domain,
            workspace
        )

    if args.dns:

        run_dns(
            domain,
            workspace
        )

    if args.http:

        run_http(
            domain,
            workspace
        )

    if args.urls:

        run_urls(
            domain,
            workspace
        )

    if args.headers:

        run_headers(
            domain,
            workspace
        )

    if args.nmap:

        run_nmap(
            domain,
            workspace
        )

    if args.nuclei:

        run_nuclei(
            domain,
            workspace
        )

    # No module selected
    selected = any(
        [
            args.subdomains,
            args.dns,
            args.http,
            args.urls,
            args.headers,
            args.nmap,
            args.nuclei,
            args.passive,
            args.full,
            args.all
        ]
    )

    if not selected:

        parser.print_help()

        print()
        log(
            "Example: python3 run.py -d example.com --full",
            "INFO"
        )


if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print()

        log(
            "SOLO RECON stopped by user.",
            "WARN"
        )

        sys.exit(130)

    except Exception as e:

        log(
            f"Fatal error: {e}",
            "ERROR"
        )

        sys.exit(1)
