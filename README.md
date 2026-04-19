Analysis of Gentrification in Brooklyn, NY
This repository contains a reactive spatial analysis of neighborhood change in Brooklyn, New York. Using U.S. Census Bureau data (Decennial Census and ACS), this project operationalizes the concept of gentrification into measurable criteria to identify tracts that were "gentrifiable" in 2000 and those that "gentrified" by 2010.

🏙 Background: What is Gentrification?
Gentrification is a complex process occurring in urban neighborhoods that have experienced decades of disinvestment, middle-class flight, and deteriorating housing stock. Despite these challenges, the urban core often remains a locus of employment and culture.

This study follows the methodology proposed by Freeman (2005), viewing gentrification as a process of class-based succession. It focuses on the concern that long-time residents may be priced out as new investment and higher-income households move in, leading to a rapid shift in educational attainment and property values.

📊 Methodology
Gentrification is measured across two distinct time periods.

1. Identifying "Gentrifiable" Tracts (Period 1: 2000)
A Census tract is classified as Gentrifiable if it lagged behind the New York Metropolitan Area in 2000 based on two criteria:

Low Income: Median Household Income (MHI) less than the Metropolitan Statistical Area (MSA) median.

Low Construction: Percentage of housing built in the previous 20 years (1980–2000) less than the MSA-level percentage.

2. Identifying "Gentrifying" Tracts (Period 2: 2010)
A tract is considered Gentrifying if it was gentrifiable in 2000 AND met the following between 2000 and 2010:

Educational Shift: The percentage of the population with a Bachelor’s degree or higher increased faster than the MSA-level increase.

Property Value Growth: House values increased significantly, even after accounting for inflation (using a CPI deflator of 1.2612).

🛠 Tech Stack
Language: Python 3.11

Notebook Environment: Marimo (A reactive, reproducible notebook format)

Spatial Data: GeoPandas, Matplotlib

Data Ingestion: Census API, Requests

Deployment: Docker (containerized for environment consistency)

🚀 Getting Started
Prerequisites
Docker installed on your machine.

A U.S. Census API Key. You can request one for free here.

Installation
Clone the repository:

Bash
git clone https://github.com/yourusername/brooklyn-gentrification.git
cd brooklyn-gentrification
Set up your Environment Variables:
Create a .env file in the root directory:

Bash
touch .env
Add your API key to the file:

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