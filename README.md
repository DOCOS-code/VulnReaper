# Basic test
python vulnreaper_idor.py -u "https://target.com/user?id=1" -p id

# Test with keyword detection
python vulnreaper_idor.py -u "https://target.com/user?id=1" -p id -k email

# Authenticated test
python vulnreaper_idor.py -u "https://api.site.com/profile?id=1" -p id -t "Bearer ey..."

# With cookies
python vulnreaper_idor.py -u "https://secure.site/api/data?id=1" -p id -c "sessionid=xyz"
