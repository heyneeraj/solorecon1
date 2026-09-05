# 🔴 SOLO RECON

### Web Reconnaissance & Attack Surface Mapping Tool

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-black.svg)](https://www.kali.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-3.0.0-red.svg)](https://github.com/YOUR-GITHUB-USERNAME/solo-recon)

**SOLO RECON** is a Python-based reconnaissance and attack-surface mapping framework for authorized security testing, bug bounty programs, CTF environments, penetration-testing labs, and security research.

It combines passive reconnaissance, DNS discovery, subdomain enumeration, HTTP/HTTPS probing, historical URL discovery, security-header analysis, Nmap scanning, and Nuclei integration into a single command-line workflow.

---

## ⚠️ Disclaimer

**SOLO RECON is intended for authorized security testing only.**

Use this tool only against:

* Systems you own
* Applications you are authorized to test
* Bug bounty targets within their defined scope
* CTF/laboratory environments
* Systems where you have explicit permission

Do **not** use SOLO RECON to scan or test systems without authorization.

The author is not responsible for damage, disruption, data loss, or unauthorized activity resulting from misuse of this project.

---

# ✨ Features

* 🔴 Red-themed CLI interface
* 🔎 Certificate Transparency enumeration
* 🌐 Subdomain discovery
* 🧭 DNS resolution
* 📡 IP address discovery
* 🌍 HTTP/HTTPS probing
* 📝 HTTP title detection
* 📊 HTTP status detection
* 🔐 Security-header analysis
* 🗃️ Wayback Machine URL discovery
* 🔭 Nmap top-100 TCP port scanning
* 🛡️ Nuclei integration
* 📄 JSON report generation
* 📁 Organized output structure
* ⚡ Passive reconnaissance mode
* 🚀 Full reconnaissance mode
* 🧩 Individual reconnaissance modules
* 🐍 Python-based
* 💻 Kali Linux friendly

---

# 🧰 Reconnaissance Workflow

```text
                         ┌──────────────────┐
                         │    TARGET DOMAIN │
                         └────────┬─────────┘
                                  │
                                  ▼
                     ┌────────────────────────┐
                     │   Certificate          │
                     │   Transparency         │
                     └───────────┬────────────┘
                                 │
                                 ▼
                     ┌────────────────────────┐
                     │   Subdomain Discovery   │
                     │   crt.sh + subfinder   │
                     └───────────┬────────────┘
                                 │
                                 ▼
                     ┌────────────────────────┐
                     │     DNS Resolution     │
                     └───────────┬────────────┘
                                 │
                                 ▼
                     ┌────────────────────────┐
                     │     IP Discovery       │
                     └───────────┬────────────┘
                                 │
                                 ▼
                     ┌────────────────────────┐
                     │    HTTP/HTTPS Probe    │
                     └───────────┬────────────┘
                                 │
                 ┌───────────────┼────────────────┐
                 ▼               ▼                ▼
             ┌───────┐      ┌──────────┐    ┌──────────┐
             │ Nmap  │      │ Wayback  │    │ Headers  │
             └───┬───┘      └────┬─────┘    └────┬─────┘
                 │               │               │
                 └───────────────┼───────────────┘
                                 ▼
                         ┌──────────────┐
                         │    Nuclei    │
                         └──────┬───────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │    JSON REPORT      │
                     └─────────────────────┘
```

---

# 📋 Requirements

## Operating System

Recommended:

* Kali Linux
* Debian
* Ubuntu

## Required

* Python 3
* `requests`

## Optional External Tools

* Nmap
* Subfinder
* Nuclei

---

# 🚀 Installation

## Clone the Repository

```bash
git clone https://github.com/YOUR-GITHUB-USERNAME/solo-recon.git
```

Enter the project:

```bash
cd solo-recon
```

---

# 🐍 Python Dependencies

Install the Python dependency:

```bash
python3 -m pip install -r requirements.txt
```

If Kali Linux prevents system-wide pip installation because of its externally-managed Python environment:

```bash
sudo apt update
sudo apt install -y python3-requests
```

---

# 🔧 Install Nmap

```bash
sudo apt update
sudo apt install -y nmap
```

Verify:

```bash
nmap --version
```

---

# 🔎 Install Subfinder

If available from your Kali package sources:

```bash
sudo apt install -y subfinder
```

Verify:

```bash
subfinder -version
```

If you don't have Subfinder installed, SOLO RECON can still use Certificate Transparency results.

---

# 🛡️ Install Nuclei

If available from your Kali package sources:

```bash
sudo apt install -y nuclei
```

Verify:

```bash
nuclei -version
```

Update templates when appropriate:

```bash
nuclei -update-templates
```

---

# ✅ Verify Installation

Run:

```bash
python3 -m py_compile run.py
```

If there is no output, the Python syntax check passed.

Then:

```bash
python3 run.py --help
```

---

# 🖥️ SOLO RECON CLI

```text
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

        Web Reconnaissance & Attack Surface Mapper
                     SOLO RECON
```

---

# 📖 Usage

## Show Help

```bash
python3 run.py --help
```

---

## Show Version

```bash
python3 run.py -d example.com --version
```

Example:

```text
SOLO RECON 3.0.0
```

---

# 🚀 Full Reconnaissance

Run the complete workflow:

```bash
python3 run.py -d example.com --full
```

Alternative:

```bash
python3 run.py -d example.com --all
```

The full workflow includes:

```text
Certificate Transparency
        ↓
Subdomain Enumeration
        ↓
DNS Resolution
        ↓
IP Discovery
        ↓
HTTP/HTTPS Probing
        ↓
Nmap
        ↓
Wayback URLs
        ↓
Security Headers
        ↓
Nuclei
        ↓
JSON Report
```

---

# 🕵️ Passive Reconnaissance

Run passive reconnaissance:

```bash
python3 run.py -d example.com --passive
```

Passive mode focuses on discovery sources such as:

* Certificate Transparency
* Subdomain enumeration
* DNS resolution
* IP discovery
* Historical URLs

---

# 🔎 Subdomain Enumeration

```bash
python3 run.py -d example.com --subdomains
```

Sources include:

```text
crt.sh
subfinder
```

Output:

```text
output/example.com/data/subdomains.txt
```

---

# 🌐 DNS Resolution

```bash
python3 run.py -d example.com --dns
```

Output:

```text
output/example.com/data/dns.json
output/example.com/data/ips.txt
```

---

# 📡 HTTP/HTTPS Probing

```bash
python3 run.py -d example.com --http
```

The HTTP module identifies:

* HTTP/HTTPS availability
* HTTP status codes
* Redirects
* Page titles
* Server headers
* Response size

Output:

```text
output/example.com/data/http.json
```

and:

```text
output/example.com/data/live_urls.txt
```

---

# 🗃️ Historical URL Discovery

```bash
python3 run.py -d example.com --urls
```

Uses the Internet Archive CDX endpoint to discover historical URLs.

Output:

```text
output/example.com/data/wayback_urls.txt
```

---

# 🔐 Security Header Analysis

```bash
python3 run.py -d example.com --headers
```

The tool checks for headers including:

```text
Strict-Transport-Security
Content-Security-Policy
X-Content-Type-Options
X-Frame-Options
Referrer-Policy
Permissions-Policy
```

Output:

```text
output/example.com/data/security_headers.json
```

---

# 🔭 Nmap

Run the top-100 TCP port scan:

```bash
python3 run.py -d example.com --nmap
```

The current implementation uses:

```text
-Pn
--top-ports 100
-T3
```

Output:

```text
output/example.com/data/nmap.txt
```

---

# 🛡️ Nuclei

Run Nuclei against discovered live HTTP targets:

```bash
python3 run.py -d example.com --nuclei
```

Output:

```text
output/example.com/data/nuclei.jsonl
```

Nuclei should only be used against systems for which you have authorization.

---

# 📁 Custom Output Directory

You can specify another output directory:

```bash
python3 run.py \
    -d example.com \
    --full \
    -o results
```

The resulting structure will be:

```text
results/
└── example.com/
    ├── data/
    ├── logs/
    └── reports/
        └── report.json
```

---

# 🧩 Individual Modules

| Option         | Function                      |
| -------------- | ----------------------------- |
| `--subdomains` | Subdomain enumeration         |
| `--dns`        | DNS resolution                |
| `--http`       | HTTP/HTTPS probing            |
| `--urls`       | Historical URL discovery      |
| `--headers`    | Security-header analysis      |
| `--nmap`       | Nmap top-100 TCP scan         |
| `--nuclei`     | Nuclei scanning               |
| `--passive`    | Passive reconnaissance        |
| `--full`       | Complete reconnaissance       |
| `--all`        | Alias for full reconnaissance |
| `--version`    | Display version               |

---

# 🧪 Example Workflow

For an authorized target:

```bash
cd solo-recon
```

Check dependencies:

```bash
which python3
which nmap
which subfinder
which nuclei
```

Check the program:

```bash
python3 run.py --help
```

Run passive discovery:

```bash
python3 run.py -d example.com --passive
```

Then run the complete workflow:

```bash
python3 run.py -d example.com --full
```

Review the generated report:

```bash
cat output/example.com/reports/report.json
```

---

# 📊 Output Structure

```text
output/
└── example.com/
    │
    ├── data/
    │   ├── subdomains.txt
    │   ├── dns.json
    │   ├── ips.txt
    │   ├── http.json
    │   ├── live_urls.txt
    │   ├── wayback_urls.txt
    │   ├── security_headers.json
    │   ├── nmap.txt
    │   ├── nuclei_targets.txt
    │   └── nuclei.jsonl
    │
    ├── logs/
    │
    └── reports/
        └── report.json
```

---

# 📄 JSON Report

The generated report contains information such as:

```json
{
    "tool": "SOLO RECON",
    "version": "3.0.0",
    "domain": "example.com",
    "timestamp": "...",
    "summary": {
        "subdomains": 10,
        "ips": 4,
        "live_http": 6,
        "wayback_urls": 100
    }
}
```

---

# 🧱 Project Structure

```text
solo-recon/
│
├── run.py
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
│
└── output/
    └── generated locally
```

Generated scan results should remain excluded from Git using `.gitignore`.

---

# 🔒 Security

Do not commit sensitive information to this repository.

Never upload:

```text
API keys
Passwords
Tokens
Private keys
SSH keys
.env files
Credentials
Authorization cookies
Private reconnaissance data
```

GitHub provides repository security features including secret scanning, push protection, Dependabot alerts, and code scanning.

---

# 🐛 Troubleshooting

## `ModuleNotFoundError: No module named 'requests'`

Install:

```bash
sudo apt install -y python3-requests
```

or:

```bash
python3 -m pip install requests
```

---

## `nmap: command not found`

```bash
sudo apt update
sudo apt install -y nmap
```

---

## `subfinder: command not found`

Install Subfinder or run SOLO RECON without depending on Subfinder.

The tool can still use Certificate Transparency results.

---

## `nuclei: command not found`

Install Nuclei or run:

```bash
python3 run.py -d example.com --passive
```

without the Nuclei stage.

---

## Permission denied

Make the script executable:

```bash
chmod +x run.py
```

Then:

```bash
./run.py -d example.com --full
```

---

## Python syntax check

```bash
python3 -m py_compile run.py
```

---

# 🔄 Updating SOLO RECON

If installed using Git:

```bash
cd solo-recon
git pull
```

Then:

```bash
python3 -m pip install -r requirements.txt
```

---

# 🧑‍💻 Development

Clone:

```bash
git clone https://github.com/YOUR-GITHUB-USERNAME/solo-recon.git
cd solo-recon
```

Create a branch:

```bash
git checkout -b feature/new-module
```

Make your changes.

Test:

```bash
python3 -m py_compile run.py
```

Commit:

```bash
git add .
git commit -m "Add new reconnaissance module"
```

Push:

```bash
git push -u origin feature/new-module
```

Then create a Pull Request.

---

# 🤝 Contributing

Contributions are welcome.

Possible contribution areas:

* New reconnaissance modules
* Better error handling
* Performance improvements
* Output/report improvements
* New data sources
* Testing
* Documentation
* Bug fixes
* CLI improvements

Before submitting a contribution:

1. Test your changes.
2. Do not include secrets.
3. Do not include real target reconnaissance data.
4. Keep changes focused.
5. Update documentation when necessary.
6. Explain the change clearly in the pull request.

---

# 🗺️ Roadmap

Future SOLO RECON improvements may include:

* [ ] Multi-threaded reconnaissance
* [ ] Advanced DNS enumeration
* [ ] ASN discovery
* [ ] Reverse DNS
* [ ] Technology fingerprinting
* [ ] WAF detection
* [ ] Cloud asset discovery
* [ ] JavaScript endpoint extraction
* [ ] API endpoint discovery
* [ ] Parameter discovery
* [ ] Screenshot collection
* [ ] Improved report generation
* [ ] HTML reports
* [ ] SQLite storage
* [ ] Configuration file
* [ ] Plugin architecture
* [ ] Recon pipeline profiles
* [ ] CI testing
* [ ] Docker support
* [ ] Web dashboard

---

# 📌 Project Status

**Current version:** `3.0.0`

**Status:** Active Development

SOLO RECON is continuously being improved with additional reconnaissance modules and reporting capabilities.

---

# 👨‍💻 Author

**Neeraj Rajeev**

Cybersecurity Researcher | Ethical Hacker | Offensive Security | VAPT | Web & API Security | AI & MCP Security | IoT & Hardware Security

GitHub:

https://github.com/YOUR-GITHUB-USERNAME

---

# 📜 License

SOLO RECON is released under the **MIT License**.

See [`LICENSE`](LICENSE) for the complete license text.

---

# ⭐ Support the Project

If SOLO RECON is useful for your authorized security research:

* ⭐ Star the repository
* 🐛 Report bugs
* 💡 Suggest improvements
* 🔧 Submit pull requests
* 📢 Share the project

---

# ⚠️ Responsible Disclosure

If you discover a security vulnerability in SOLO RECON itself, please do not publicly disclose exploitable details before giving the maintainer reasonable time to investigate and address the issue.

See [`SECURITY.md`](SECURITY.md) for the project's security-reporting process.

---

# 🔴 SOLO RECON

**Recon. Discover. Understand. Secure.**

> Built for security researchers, bug bounty hunters, penetration testers, CTF players, and authorized security testing.
