import marimo as mo

app = mo.App(title="Brooklyn Gentrification Analysis", iterable_update=False)

@app.cell
def __():
    import marimo as mo
    import os
    import pandas as pd
    import geopandas as gpd
    import matplotlib.pyplot as plt
    import requests
    from dotenv import load_dotenv

    # Load environment variables from .env
    load_dotenv()
    return gpd, load_dotenv, mo, os, pd, plt, requests

@app.cell
def __(mo):
    mo.md(
        r"""
        # 🏙️ Brooklyn Gentrification Analysis (2000-2010)
        This notebook uses U.S. Census data to operationalize gentrification using the Freeman (2005) methodology.
        
        **Process:**
        1. Identify **Gentrifiable** tracts in 2000 (Low income, low new housing).
        2. Identify **Gentrifying** tracts by 2010 (Rapid increase in education & property value).
        """
    )
    return

@app.cell
def __(mo, os):
    # Security check for API Key
    API_KEY = os.getenv("CENSUS_API_KEY")
    
    if API_KEY:
        status = print("✅ Census API Key detected from .env")
    else:
        status = print("❌ **API Key Missing**: Ensure CENSUS_API_KEY is in your .env file.")
    
    STATE = "36"   # New York
    COUNTY = "047" # Kings County (Brooklyn)
    BASE_URL = "http://api.census.gov/data/2000/dec/sf3"
    
    return API_KEY, BASE_URL, COUNTY, STATE, status

@app.cell
def __():
    # Census Variable Mapping
    VARIABLES = [
        "NAME", "GEO_ID", "P053001", "H034001", "H034002", "H034003", 
        "H034004", "H034005", "P037001", "P037015", "P037016", 
        "P037017", "P037018", "P037032", "P037033", "P037034", "P037035"
    ]
    
    COLUMN_NAMES = {
        "P053001": "mhi",             # Median Household Income
        "H034001": "total_units",     # Total Housing Units
        "P037001": "total_pop_over25",# Pop for Education
        "GEO_ID": "geoid"
    }
    return COLUMN_NAMES, VARIABLES

@app.cell
def __(API_KEY, BASE_URL, COLUMN_NAMES, COUNTY, STATE, VARIABLES, mo, pd, requests):
    if not API_KEY:
        mo.stop(True, mo.md("Please provide an API key to continue."))
        
    params = {
        "get": ",".join(VARIABLES),
        "for": "tract:*",
        "in": f"state:{STATE} county:{COUNTY}",
        "key": API_KEY
    }
    
    response = requests.get(BASE_URL, params=params)
    
    # --- Robust Error Handling ---
    if response.status_code != 200:
        # This will show you exactly what the Census API says (e.g., "Invalid Key")
        error_msg = f"**API Error {response.status_code}:** {response.text}"
        mo.stop(True, mo.md(error_msg))

    try:
        raw_data = response.json()
    except Exception as e:
        # This catches the JSONDecodeError and displays the non-JSON text
        mo.stop(True, mo.md(f"**JSON Parsing Error:** {str(e)} \n\n **Raw Response:** {response.text}"))
        
    # Process the data if JSON was successful
    df = pd.DataFrame(raw_data[1:], columns=raw_data[0])
    df = df.rename(columns=COLUMN_NAMES)
    df['geoid'] = df['geoid'].str[-11:]
    
    # Convert numeric columns
    numeric_cols = [c for c in df.columns if c not in ['NAME', 'state', 'county', 'tract', 'geoid']]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    
    return df,

@app.cell
def __(df):
    # 1. Calculate Educational Attainment (% BA or higher)
    _edu_cols = ["P037015", "P037016", "P037017", "P037018", "P037032", "P037033", "P037034", "P037035"]
    df["pct_higher_ed"] = (df[_edu_cols].sum(axis=1) / df["total_pop_over25"]) * 100
    
    # 2. Calculate Recent Housing (% built 1980-2000)
    _recent_cols = ["H034002", "H034003", "H034004", "H034005"]
    df["pct_recent_housing"] = (df[_recent_cols].sum(axis=1) / df["total_units"]) * 100
    
    # 3. Define Thresholds (compared to Brooklyn Median)
    median_mhi = df["mhi"].median()
    median_recent_housing = df["pct_recent_housing"].median()
    
    # 4. Identify Gentrifiable Tracts
    df["is_gentrifiable"] = (df["mhi"] < median_mhi) & (df["pct_recent_housing"] < median_recent_housing)
    
    return df, median_mhi, median_recent_housing

@app.cell
def __(df, mo, status):
    # Output UI
    return mo.vstack([
        status,
        mo.md("### Results: Gentrification Metrics (2000)"),
        mo.ui.table(
            df[['geoid', 'mhi', 'pct_higher_ed', 'pct_recent_housing', 'is_gentrifiable']], 
            pagination=True,
            label="Brooklyn Census Tracts"
        )
    ])

if __name__ == "__main__":
    app.run()