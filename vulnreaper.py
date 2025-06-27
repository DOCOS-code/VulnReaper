import argparse
from modules.idor_scanner import check_idor
from modules.sqli_scanner import detect_sqli

def run_idor(args):
    from urllib.parse import urlparse, parse_qs
    start, end = map(int, args.range.split("-"))
    test_ids = range(start, end + 1)

    cookies = {}
    if args.cookie:
        name, value = args.cookie.split("=", 1)
        cookies[name.strip()] = value.strip()

    results = check_idor(
        args.url,
        args.param,
        test_ids,
        cookies=cookies,
        auth_header=args.token,
        keyword=args.keyword
    )

    print("\n🧾 === IDOR RESULTS ===")
    if results:
        for url, issue in results:
            print(f"{issue} → {url}")
    else:
        print("✅ No IDOR detected.")

def run_sqli(args):
    results = detect_sqli(args.url, args.param)
    print("\n🧾 === SQLi RESULTS ===")
    if results:
        for payload, issue in results:
            print(f"{issue}: {payload}")
    else:
        print("✅ No SQLi vulnerabilities found.")

def main():
    parser = argparse.ArgumentParser(description="🛡️ VulnReaper: Multi-Mode Vulnerability Scanner")
    parser.add_argument("--mode", required=True, choices=["idor", "sqli"], help="Scan mode")
    parser.add_argument("--url", required=True, help="Target URL")
    parser.add_argument("--param", help="Parameter to fuzz/test")
    parser.add_argument("--range", default="1-10", help="ID range (only for IDOR)")
    parser.add_argument("--token", help="Authorization token (Bearer...)")
    parser.add_argument("--cookie", help="Session cookie")
    parser.add_argument("--keyword", help="Keyword to detect in response (IDOR only)")

    args = parser.parse_args()

    if args.mode == "idor":
        if not args.param:
            print("❌ IDOR mode requires --param.")
            return
        run_idor(args)
    elif args.mode == "sqli":
        if not args.param:
            print("❌ SQLi mode requires --param.")
            return
        run_sqli(args)

if __name__ == "__main__":
    main()
