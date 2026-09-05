# solorecon1cat > README.md <<'EOF'
# 🔴 SOLO RECON

**SOLO RECON** is a Python-based web reconnaissance and attack-surface mapping tool designed for authorized security testing, bug bounty programs, CTFs, and security labs.

## Features

- Certificate Transparency discovery
- Subdomain enumeration
- DNS resolution
- IP discovery
- HTTP/HTTPS probing
- HTTP title detection
- Nmap top-100 TCP port scanning
- Wayback Machine URL discovery
- Security header analysis
- Nuclei integration
- JSON reporting
- Modular CLI
- Passive reconnaissance mode
- Full reconnaissance mode
- Colored terminal interface

## Requirements

- Python 3
- requests
- Nmap
- Subfinder
- Nuclei

## Installation

```bash
git clone https://github.com/YOUR-USERNAME/solo-recon.git
cd solo-recon

python3 -m pip install -r requirements.txt


2. Full reconnaissance
python3 run.py -d example.com --full

or:

python3 run.py -d example.com --all

This runs:

SOLO RECON
   │
   ├── Certificate Transparency
   ├── Subdomain Enumeration
   ├── DNS Resolution
   ├── IP Discovery
   ├── HTTP/HTTPS Probe
   ├── Nmap
   ├── Wayback URLs
   ├── Security Headers
   ├── Nuclei
   └── JSON Report

Only run this against systems you own or are explicitly authorized to assess.

3. Passive reconnaissance
python3 run.py -d example.com --passive

This performs the passive portions without the active Nmap/Nuclei stages.

4. Individual modules

Subdomains

python3 run.py -d example.com --subdomains

DNS

python3 run.py -d example.com --dns

HTTP probing

python3 run.py -d example.com --http

Historical URLs

python3 run.py -d example.com --urls

Security headers

python3 run.py -d example.com --headers

Nmap

python3 run.py -d example.com --nmap

Nuclei

python3 run.py -d example.com --nuclei
5. Custom output directory
python3 run.py -d example.com --full -o results

Output:

results/
└── example.com/
    ├── data/
    ├── logs/
    └── reports/
        └── report.json
6. Version
python3 run.py -d example.com --version

Expected:

SOLO RECON 3.0.0
7. Recommended first test

Use a domain you are authorized to test:

cd /home/kali/Documents/solorecon

python3 -m py_compile run.py

python3 run.py -d YOUR-AUTHORIZED-DOMAIN.com --full

Then inspect:

find output -type f

And the main report:

cat output/YOUR-AUTHORIZED-DOMAIN.com/reports/report.json
