# Gentrification in Brooklyn, NY: A Spatial Analysis 🏙️

> A reproducible geospatial study measuring neighborhood gentrification in Brooklyn using U.S. Census data — operationalizing a peer-reviewed sociological framework into quantifiable, tract-level indicators.

**Python · Marimo · GeoPandas · Census API · Docker**

---

## Overview

Gentrification — the displacement of long-time, lower-income residents as higher-income households and investment move into historically disinvested neighborhoods — is one of the most consequential urban processes affecting health equity, housing stability, and community cohesion.

This project follows the methodology of **Freeman (2005)** to classify Brooklyn census tracts as *gentrifiable* (eligible for gentrification based on 2000 conditions) and *gentrifying* (showing measurable change by 2010) using two decades of U.S. Census Bureau data.

The result is an interactive, reactive spatial analysis that maps which neighborhoods changed, by how much, and by what measurable indicators.

---

## Why This Matters

Gentrification is a **social determinant of health**. Displacement disrupts:
- Access to primary care and trusted providers
- Chronic disease management continuity
- Mental health and social support networks
- School stability for children

Identifying where gentrification has occurred — and by what mechanisms — is the first step toward targeted policy intervention and equitable resource allocation.

*This project builds directly on the geospatial cluster analysis methods used professionally in STI/HIV morbidity hotspot identification at the Virginia Department of Health.*

---

## Key Questions

1. Which Brooklyn census tracts were "gentrifiable" in 2000 — lagging behind the NYC metro area in income and housing investment?
2. Which of those tracts showed measurable gentrification between 2000 and 2010?
3. What does the spatial distribution of gentrifying tracts reveal about neighborhood change patterns across Brooklyn?

For the full analytical framework, data dictionary, and variable definitions, see **[METHODOLOGY.md](./METHODOLOGY.md)**.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.11 | Core analysis |
| [Marimo](https://marimo.io) | Reactive, reproducible notebook environment |
| GeoPandas | Spatial data processing and tract-level mapping |
| Matplotlib | Visualization |
| U.S. Census Bureau API | Decennial Census (2000) and ACS (2010) data |
| Docker | Containerized reproducible environment |

---

## Getting Started

### Prerequisites
- [Docker](https://www.docker.com/get-started) installed
- A free [U.S. Census API Key](https://api.census.gov/data/key_signup.html)

### Run with Docker

```bash
# 1. Clone the repo
git clone https://github.com/rndayizeye/gentrification_nyc_2000_2010.git
cd gentrification_nyc_2000_2010

# 2. Set up environment variables
cp .env.example .env
# Edit .env and add: CENSUS_API_KEY=your_key_here

# 3. Build and run
docker build -t brooklyn-analysis .
docker run --env-file .env -p 2718:2718 brooklyn-analysis
```

Open **http://localhost:2718** in your browser.

---

## Project Structure

```
gentrification_nyc_2000_2010/
├── brooklyn_gentrification.py   # Main Marimo reactive notebook
├── Dockerfile                   # Reproducible container config
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variable template
├── README.md                    # This file
└── METHODOLOGY.md               # Full analytical framework and variable definitions
```

---

## Reference

Freeman, Lance. 2005. "Displacement or Succession?: Residential Mobility in Gentrifying Neighborhoods." *Urban Affairs Review* 40(4): 463–491.

---

## Author

**Remy Ndayizeye, MPH, MD**
Epidemiologist | Data Scientist | Virginia Department of Health
[LinkedIn](https://www.linkedin.com/in/remynd) · [DataCamp Portfolio](https://www.datacamp.com/portfolio/remyndayizeye) · [GitHub](https://github.com/rndayizeye)Add your API key to the file:

Plaintext
CENSUS_API_KEY=your_key_here
Build and Run with Docker:

Bash
# Build the image
docker build -t brooklyn-analysis .

# Run the container
docker run --env-file .env -p 2718:2718 brooklyn-analysis
View the Analysis:
Open your browser and navigate to http://localhost:2718.

📂 Project Structure
brooklyn_gentrification.py: The main Marimo notebook file.

Dockerfile: Configuration for the reproducible environment.

requirements.txt: Python dependencies.

.env.example: Template for required environment variables.

Reference: Freeman, Lance. 2005. “Displacement or Succession?: Residential Mobility in Gentrifying Neighborhoods.” Urban Affairs Review 40 (4): 463–91.
