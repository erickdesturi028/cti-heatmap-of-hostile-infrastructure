# CTI Hostile Infrastructure Heatmap

## Overview

The CTI Hostile Infrastructure Heatmap is a web-based Cyber Threat Intelligence (CTI) platform designed to collect, analyze, and visualize malicious infrastructure using open-source intelligence (OSINT) data.

The system ingests malicious IP indicators from public threat feeds, enriches them with contextual intelligence such as threat type and MITRE ATT&CK mapping, and presents the results through an interactive dashboard and global heatmap.

This project demonstrates how raw threat data can be transformed into actionable intelligence for security operations and threat analysis.

---

## Features

- OSINT-based ingestion of malicious IP indicators
- Automatic deduplication and structured storage
- Threat classification (botnet, malware, scanning, bruteforce)
- MITRE ATT&CK technique mapping
- Global heatmap visualization of hostile infrastructure
- Region-based threat percentage and severity classification
- Interactive dashboard with analytics (Plotly)
- STIX 2.1 export for intelligence sharing
- Fast ingestion pipeline optimized for performance

---

## Technology Stack

- Backend: Python, Flask
- Database: PostgreSQL, SQLAlchemy
- Visualization: Folium, Plotly
- CTI Standards: MITRE ATT&CK, STIX 2.1
- OSINT Sources: Abuse.ch (Feodo Tracker), FireHOL

---

## Project Structure

hostile_infra_heatmap/
│
├── app/
│   ├── **init**.py
│   ├── models.py
│   └── routes.py
│
├── services/
│   ├── collector.py
│   ├── heatmap.py
│   ├── analytics.py
│   ├── mitre_mapper.py
│   └── stix_exporter.py
│
├── templates/
│   └── dashboard.html
│
├── run.py
├── requirements.txt
└── README.md

````

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/cti-heatmap-project.git
cd cti-heatmap-project
````

### 2. Create and activate virtual environment

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

* Create a database (e.g., `cti_heatmap`)
* Update database connection string in the project if needed

### 5. Initialize database

```bash
python
```

```python
from app import create_app, db
app = create_app()

with app.app_context():
    db.create_all()
```

### 6. Run the application

```bash
python run.py
```

---

## Usage

### Collect OSINT data

```
http://127.0.0.1:5000/collect
```

### View IoCs (JSON)

```
http://127.0.0.1:5000/ioc
```

### View dashboard

```
http://127.0.0.1:5000/dashboard
```

### View heatmap

```
http://127.0.0.1:5000/map
```

### Export STIX

```
http://127.0.0.1:5000/stix
```

---

## How It Works

1. The system collects malicious IPs from OSINT feeds.
2. Indicators are filtered, deduplicated, and stored in PostgreSQL.
3. Each IoC is classified by threat type and mapped to MITRE ATT&CK techniques.
4. The dashboard visualizes threat distribution using charts.
5. The heatmap shows global concentration of hostile infrastructure.
6. Regional markers display percentage and severity levels.
7. STIX export enables structured threat intelligence sharing.

---

## Example Output

* Heatmap showing global threat concentration
* Dashboard displaying IoC counts and threat distribution
* Region-based markers with:

  * Indicator count
  * Percentage of total threats
  * Threat level (High, Medium, Low)

---

## Reset Database (For Demo)

To clear all collected data:

```sql
TRUNCATE TABLE ioc RESTART IDENTITY;
```

---

## Limitations

* Uses public OSINT feeds only
* No real-time attack telemetry
* Geolocation is region-based, not precise IP mapping
* Limited threat attribution

---

## Future Improvements

* Real GeoIP integration (MaxMind)
* Scheduled ingestion automation
* Time-based trend analysis
* Threat intelligence correlation
* User authentication and access control
* Cloud deployment support

---

## References

* MITRE ATT&CK: [https://attack.mitre.org](https://attack.mitre.org)
* STIX Standard: [https://oasis-open.github.io/cti-documentation/stix/intro](https://oasis-open.github.io/cti-documentation/stix/intro)
* Feodo Tracker: [https://feodotracker.abuse.ch](https://feodotracker.abuse.ch)
* FireHOL IP Lists: [https://iplists.firehol.org](https://iplists.firehol.org)
* Flask: [https://flask.palletsprojects.com](https://flask.palletsprojects.com)
* Folium: [https://python-visualization.github.io/folium/](https://python-visualization.github.io/folium/)
* Plotly: [https://plotly.com/python/](https://plotly.com/python/)
* PostgreSQL: [https://www.postgresql.org/docs/](https://www.postgresql.org/docs/)

---

## License

This project is developed for educational and research purposes.



Watch My Demo Video

Click the link below to view the demo:

<https://github.com/user-attachments/assets/a/d0add1-650f-49d3-a560-a6f692247ff5>
