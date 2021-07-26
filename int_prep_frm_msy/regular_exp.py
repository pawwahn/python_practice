import re
ip="241.1.1.112,10.0.0.12.1sfh hghrh a45.53.35.35.35 this string contains ips"
ip_candidates = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", ip)
print(ip_candidates)