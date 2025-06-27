# ⚔️ VulnReaper - Multi-Mode Vulnerability Scanner

**VulnReaper** is a powerful modular vulnerability scanner designed to assist bug bounty hunters and pentesters with automated detection of **OWASP Top 10** vulnerabilities. Built for **CLI warriors**, **TUI navigators**, and **GUI tacticians**, this tool unites automation with precision.

---

## 🔍 Features

- 🔐 **IDOR Scanner** – detects insecure direct object references
- 💉 **SQLi Scanner** – basic injection payloads for URL fuzzing
- 🧾 **TUI Interface** – Rich-powered terminal UI with report viewer
- 🌐 **React GUI** – Web-based scanner interface (in progress)
- 🔗 **Command Chaining** – Auto-run multiple modules
- 🛰️ **Passive Recon Engine** – JS link discovery, headers, DNS
- 🧬 **Burp Integration** – Send targets directly to VulnReaper from Burp

---

## 🛠️ Installation

### 1. Clone the repo

`bash
git clone https://github.com/nullecho/VulnReaper.git
cd VulnReaper
pip install -r requirements.txt 


⚔️ CLI Usage
python vulnreaper.py --mode <idor|sqli|all> --url TARGET_URL --param PARAM

🔹 IDOR Example
python vulnreaper.py --mode idor --url "https://site.com/profile?id=1" --param id --range 1-10 --keyword "username"

🔹 SQLi Example
python vulnreaper.py --mode sqli --url "https://site.com/product?item=1" --param item


🔹 All Modes (Command Chaining)
python vulnreaper.py --mode all --url "https://site.com/api/user?id=1" --param id


🖥️ TUI Mode
python vulnreaper_tui.py


vulnreaper/
├── vulnreaper.py               # Main CLI engine
├── vulnreaper_tui.py           # TUI interface
├── modules/                    # Scanner modules
│   ├── idor_scanner.py
│   └── sqli_scanner.py
├── scan_logs/                  # JSON results saved
├── logs/                       # Plaintext scan logs
├── frontend/                   # React GUI (WIP)
└── requirements.txt



