import requests

def get_country_from_ip(ip_address):
    try:
        url = f"https://ipinfo.io/{ip_address}/json"
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        data = response.json()
        return data.get("country", "Unknown")

    except Exception:
        return "Unknown"
