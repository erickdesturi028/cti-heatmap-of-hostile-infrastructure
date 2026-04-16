import requests
from app import db
from app.models import IOC
from services.mitre_mapper import map_to_attack

# Multiple OSINT IP feeds mapped to threat categories
OSINT_FEEDS = {
    "botnet": "https://feodotracker.abuse.ch/downloads/ipblocklist.txt",
    "malware": "https://raw.githubusercontent.com/stamparm/ipsum/master/ipsum.txt",
    "scanning": "https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/firehol_level1.netset",
    "bruteforce": "https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/firehol_level2.netset"
}

# Different ingestion limits per threat type (creates visual variation)
THREAT_LIMITS = {
    "botnet": 300,
    "malware": 700,
    "scanning": 1200,
    "bruteforce": 500
}

def collect_malicious_ips():
    added = 0
    headers = {"User-Agent": "CTI-Research-Project/1.0"}

    for threat_type, feed_url in OSINT_FEEDS.items():
        try:
            response = requests.get(feed_url, headers=headers, timeout=10)
            response.raise_for_status()
        except Exception:
            continue

        lines = response.text.splitlines()
        count_per_threat = 0
        limit = THREAT_LIMITS.get(threat_type, 500)

        for line in lines:
            line = line.strip()

            # Skip comments and empty lines
            if not line or line.startswith("#"):
                continue

            #  Handle CIDR ranges instead of skipping them
            if "/" in line:
                line = line.split("/")[0]

            # Stop when limit for this threat type is reached
            if count_per_threat >= limit:
                break

            # Deduplicate globally
            existing = IOC.query.filter_by(ioc_value=line).first()
            if existing:
                continue

            country = "Unknown"
            attack = map_to_attack(threat_type)

            ioc = IOC(
                ioc_value=line,
                ioc_type="ip",
                country=country,
                threat_type=threat_type,
                attack_technique=attack
            )

            db.session.add(ioc)
            added += 1
            count_per_threat += 1

    db.session.commit()
    return added
