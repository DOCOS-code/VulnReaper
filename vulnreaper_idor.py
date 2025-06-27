import requests
import argparse
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def generate_test_urls(base_url, param_name, test_range):
    parsed = urlparse(base_url)
    query = parse_qs(parsed.query)
    test_urls = []
    for val in test_range:
        query[param_name] = str(val)
        new_query = urlencode(query, doseq=True)
        test_urls.append(urlunparse(parsed._replace(query=new_query)))
    return test_urls

def check_idor(base_url, param_name, test_range, cookies=None, auth_header=None, keyword=None):
    test_urls = generate_test_urls(base_url, param_name, test_range)
    headers = {}
    if auth_header:
        headers['Authorization'] = auth_header

    print(f"\n🔍 Scanning {len(test_urls)} variations on parameter '{param_name}'...")
    findings = []
    baseline = None

    for url in test_urls:
        try:
            response = requests.get(url, headers=headers, cookies=cookies)
            print(f"[{response.status_code}] {url}")
            
            if baseline is None:
                baseline = response.text

            if keyword and keyword.lower() in response.text.lower():
                findings.append((url, "⚠️ Keyword matched"))
            elif response.text != baseline:
                findings.append((url, "🔁 Response differed from baseline"))
        except requests.exceptions.RequestException as e:
            print(f"❌ Error with {url}: {e}")

    return findings

def main():
    parser = argparse.ArgumentParser(description="🔍 VulnReaper IDOR Scanner")
    parser.add_argument("-u", "--url", required=True, help="Target URL with parameter (e.g. https://host/api/user?id=1)")
    parser.add_argument("-p", "--param", required=True, help="Parameter to fuzz (e.g. id)")
    parser.add_argument("-r", "--range", default="1-10", help="ID range to scan (e.g. 1-100)")
    parser.add_argument("-k", "--keyword", help="Sensitive keyword to detect in response (e.g. email)")
    parser.add_argument("-t", "--token", help="Bearer token (optional)")
    parser.add_argument("-c", "--cookie", help="Session cookie (e.g. session=abc123)")

    args = parser.parse_args()
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

    print("\n🧾 === SCAN REPORT ===")
    if results:
