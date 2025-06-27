import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def generate_test_urls(base_url, param_name, test_range):
    """
    Generates test URLs by modifying the specified parameter
    """
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

    print(f"🔎 Scanning {len(test_urls)} endpoints for IDOR...")
    findings = []
    baseline = None

    for url in test_urls:
        response = requests.get(url, headers=headers, cookies=cookies)
        print(f"[{response.status_code}] Checked {url}")
        
        # Save first response as baseline
        if baseline is None:
            baseline = response.text

        if keyword and keyword in response.text:
            findings.append((url, "⚠️ Sensitive Keyword Found"))
        elif response.text != baseline:
            findings.append((url, "🔁 Response Differed From Baseline"))

    return findings


if __name__ == "__main__":
    # === CONFIGURATION ===
    target_url = "https://example.com/api/user?id=1"  # 🧠 Input endpoint
    param_to_test = "id"
    test_ids = range(1, 10)  # 🧪 Adjust range as needed
    session_cookies = {"session": "your-session-id"}  # 🍪 Optional
    auth_token = "Bearer your-api-token"  # 🔐 Optional
    secret_keyword = "email"  # 🕵️ e.g., detecting if response leaks sensitive info

    results = check_idor(
        target_url,
        param_to_test,
        test_ids,
        cookies=session_cookies,
        auth_header=auth_token,
        keyword=secret_keyword
    )

    print("\n🧾 === RESULTS ===")
    for url, issue in results:
        print(f"{issue} → {url}")
