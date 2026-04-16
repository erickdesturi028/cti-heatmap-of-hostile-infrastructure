from stix2 import Indicator, Bundle
from app.models import IOC

def export_iocs_to_stix(limit=1000):
    indicators = []

    # Performance fix:
    # Only export most recent indicators (limit to avoid heavy processing)
    iocs = IOC.query.order_by(IOC.first_seen.desc()).limit(limit).all()

    for ioc in iocs:
        if ioc.ioc_type == "ip":
            indicator = Indicator(
                name=f"Malicious IP {ioc.ioc_value}",
                pattern_type="stix",
                pattern=f"[ipv4-addr:value = '{ioc.ioc_value}']",
                labels=[ioc.threat_type],
                confidence=75
            )
            indicators.append(indicator)

    bundle = Bundle(objects=indicators)
    return bundle.serialize(pretty=True)
