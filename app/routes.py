from flask import Blueprint, request, render_template
from app.models import IOC
from services.collector import collect_malicious_ips
from services.heatmap import generate_heatmap
from services.analytics import threat_type_distribution, threat_type_bar_chart
from services.stix_exporter import export_iocs_to_stix

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return "CTI Heatmap Flask app is running"

@main.route("/collect")
def collect_iocs():
    count = collect_malicious_ips()
    return {"message": f"{count} malicious IPs collected"}

@main.route("/ioc")
def list_iocs():
    iocs = IOC.query.all()
    result = []

    for ioc in iocs:
        result.append({
            "id": ioc.id,
            "ioc_value": ioc.ioc_value,
            "ioc_type": ioc.ioc_type,
            "country": ioc.country,
            "threat_type": ioc.threat_type,
            "first_seen": ioc.first_seen.isoformat(),
            "attack_technique": ioc.attack_technique
        })

    return {"iocs": result}

@main.route("/map")
def show_map():
    threat = request.args.get("threat")
    days = request.args.get("days")

    heatmap = generate_heatmap(threat_type=threat, days=days)
    return heatmap._repr_html_()

@main.route("/dashboard")
def dashboard():
    threat_filter = request.args.get("threat")

    # Filter IoCs if threat selected
    query = IOC.query
    if threat_filter:
        query = query.filter_by(threat_type=threat_filter)

    total_iocs = query.count()
    threat_counts = threat_type_distribution()

    # Heatmap (respects filter)
    heatmap = generate_heatmap(threat_type=threat_filter)
    heatmap_html = heatmap._repr_html_()

    # Plotly chart
    fig = threat_type_bar_chart()
    chart_html = fig.to_html(full_html=False)

    return render_template(
        "dashboard.html",
        total_iocs=total_iocs,
        threat_counts=threat_counts,
        heatmap_html=heatmap_html,
        chart_html=chart_html,
        selected_threat=threat_filter
    )

    

@main.route("/charts")
def charts():
    fig = threat_type_bar_chart()
    return fig.to_html(full_html=True)

@main.route("/stix")
def stix_feed():
    return export_iocs_to_stix(), 200, {"Content-Type": "application/json"}
