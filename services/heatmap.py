import folium
from folium.plugins import HeatMap
from datetime import datetime, timedelta
from app.models import IOC

# Fixed global anchor points (region centroids)
REGION_POINTS = {
    "North America": (37.0, -95.0),
    "Europe": (51.0, 10.0),
    "South Asia": (20.0, 78.0),
    "East Asia": (35.0, 104.0),
    "South America": (-15.0, -60.0),
    "Australia": (-25.0, 135.0),
    "Africa": (0.0, 20.0),
}

def classify_level(percentage):
    if percentage >= 20:
        return "High"
    elif percentage >= 5:
        return "Medium"
    else:
        return "Low"

def generate_heatmap(threat_type=None, days=None):
    query = IOC.query

    if threat_type:
        query = query.filter_by(threat_type=threat_type)

    if days:
        since = datetime.utcnow() - timedelta(days=int(days))
        query = query.filter(IOC.first_seen >= since)

    iocs = query.all()

    if not iocs:
        return folium.Map(location=[20, 0], zoom_start=2)

    world_map = folium.Map(location=[20, 0], zoom_start=2)

    # -------- Heatmap Layer --------
    locations = []
    region_counts = {region: 0 for region in REGION_POINTS}

    total_iocs = len(iocs)

    # Deterministic distribution across regions
    region_names = list(REGION_POINTS.keys())

    for index, _ in enumerate(iocs):
        region_name = region_names[index % len(region_names)]
        point = REGION_POINTS[region_name]
        locations.append(point)
        region_counts[region_name] += 1

    HeatMap(
        locations,
        radius=30,
        blur=25,
        min_opacity=0.4
    ).add_to(world_map)

    # -------- Percentage + Markers --------
    for region, count in region_counts.items():
        if count == 0:
            continue

        percentage = (count / total_iocs) * 100
        level = classify_level(percentage)

        lat, lon = REGION_POINTS[region]

        popup_text = f"""
        <b>Region:</b> {region}<br>
        <b>Indicators:</b> {count}<br>
        <b>Percentage:</b> {percentage:.2f}%<br>
        <b>Threat Level:</b> {level}
        """

        # Color by level
        if level == "High":
            color = "red"
        elif level == "Medium":
            color = "orange"
        else:
            color == "green"

        folium.CircleMarker(
            location=(lat, lon),
            radius=10,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=folium.Popup(popup_text, max_width=300)
        ).add_to(world_map)

    return world_map