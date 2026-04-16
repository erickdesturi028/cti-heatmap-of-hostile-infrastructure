from collections import Counter
from app.models import IOC
import plotly.graph_objects as go

def threat_type_distribution():
    iocs = IOC.query.all()

    threat_types = [ioc.threat_type for ioc in iocs if ioc.threat_type]
    counts = Counter(threat_types)

    return counts

def threat_type_bar_chart():
    counts = threat_type_distribution()

    threat_types = list(counts.keys())
    values = list(counts.values())

    fig = go.Figure(
        data=[go.Bar(x=threat_types, y=values)]
    )

    fig.update_layout(
        title="Threat Type Distribution",
        xaxis_title="Threat Type",
        yaxis_title="Number of IoCs"
    )

    return fig
def threat_severity(threat_type):
    severity_map = {
        "botnet": "High",
        "malware": "High",
        "bruteforce": "Medium",
        "scanning": "Low"
    }
    return severity_map.get(threat_type, "Medium")
