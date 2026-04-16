def map_to_attack(threat_type):
    mapping = {
        "botnet": "T1071",
        "malware": "T1059",
        "phishing": "T1566",
        "ransomware": "T1486"
    }

    return mapping.get(threat_type, "Unknown")
