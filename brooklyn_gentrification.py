import marimo

__generated_with = "0.23.1"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import os
    import pandas as pd
    import geopandas as gpd
    import matplotlib.pyplot as plt
    import requests
    from dotenv import load_dotenv

    load_dotenv()
    return gpd, mo, os, pd, plt, requests


@app.cell
def _(mo, os):
    # Config & Keys
    API_KEY = os.getenv("CENSUS_API_KEY")
    STATE = "36"
    COUNTY = "047"
    SHAPE_URL = "https://www2.census.gov/geo/pvs/tiger2010st/36_New_York/36047/tl_2010_36047_tract00.zip"

    # Validation
    if not API_KEY:
        status = mo.md("❌ **API Key Missing**")
    else:
        status = mo.md("✅ **Environment Ready**")

    return API_KEY, COUNTY, SHAPE_URL, STATE


@app.cell
def _(pd, requests):
    def fetch_census_data(base_url, variables, state, county, api_key):
        """Generic function to fetch Census data for a specific county."""
        params = {
            "get": ",".join(variables),
            "for": "tract:*",
            "in": f"state:{state} county:{county}",
            "key": api_key
        }
        response = requests.get(base_url, params=params)

        if response.status_code != 200:
            return None, f"Error {response.status_code}: {response.text}"

        try:
            data = response.json()
            df = pd.DataFrame(data[1:], columns=data[0])
            return df, None
        except Exception as e:
            return None, str(e)


    return (fetch_census_data,)


@app.cell
def _(API_KEY, COUNTY, STATE, fetch_census_data, mo):
    if not API_KEY:
        mo.stop(True)

    # --- 2000 Decennial Census (SF3) ---
    vars_2000 = ["GEO_ID", "P053001", "H034001", "P037001", "H085001", 
                 "P037015", "P037016", "P037017", "P037018", 
                 "P037032", "P037033", "P037034", "P037035"]

    df_2000, err_2000 = fetch_census_data(
        "http://api.census.gov/data/2000/dec/sf3", 
        vars_2000, STATE, COUNTY, API_KEY
    )

    # --- 2012 ACS 5-Year Survey ---
    # B15003_022-025 = BA, Masters, Professional, Doctorate
    # B25077_001E = Median Value
    vars_2012 = ["GEO_ID", "B19013_001E", "B15003_001E", "B25077_001E",
                 "B15003_022E", "B15003_023E", "B15003_024E", "B15003_025E"]

    df_2012, err_2012 = fetch_census_data(
        "http://api.census.gov/data/2012/acs/acs5", 
        vars_2012, STATE, COUNTY, API_KEY
    )

    if err_2000 or err_2012:
        mo.stop(True, mo.md(f"Fetch Error: {err_2000 or err_2012}"))
    return df_2000, df_2012


@app.cell
def _(df_2000, df_2012, pd):
    # --- Cleaning & Merging ---

    # 2000 Logic
    d00 = df_2000.copy()
    d00['geoid'] = d00['GEO_ID'].str[-11:]
    d00 = d00.rename(columns={"P053001": "mhi_00", "H085001": "med_val_00"})

    edu_cols_00 = ["P037015", "P037016", "P037017", "P037018", "P037032", "P037033", "P037034", "P037035"]
    d00[edu_cols_00] = d00[edu_cols_00].apply(pd.to_numeric)
    d00["pct_ba_00"] = (d00[edu_cols_00].sum(axis=1) / pd.to_numeric(d00["P037001"])) * 100

    # 2012 Logic
    d12 = df_2012.copy()
    d12['geoid'] = d12['GEO_ID'].str[-11:]
    d12 = d12.rename(columns={"B19013_001E": "mhi_12", "B25077_001E": "med_val_12"})

    edu_cols_12 = ["B15003_022E", "B15003_023E", "B15003_024E", "B15003_025E"]
    d12[edu_cols_12] = d12[edu_cols_12].apply(pd.to_numeric)
    d12["pct_ba_12"] = (d12[edu_cols_12].sum(axis=1) / pd.to_numeric(d12["B15003_001E"])) * 100

    # Combine
    combined = pd.merge(d00[['geoid', 'mhi_00', 'med_val_00', 'pct_ba_00']], 
                        d12[['geoid', 'mhi_12', 'med_val_12', 'pct_ba_12']], 
                        on='geoid')

    # Inflation Adjustment (2000 to 2012 factor approx 1.26)
    combined['med_val_00_adj'] = pd.to_numeric(combined['med_val_00']) * 1.26

    return (combined,)


@app.cell
def _(SHAPE_URL, combined, gpd, mo):
    # Spatial Join
    with mo.status.spinner(title="Loading Map..."):
        gdf = gpd.read_file(SHAPE_URL)
        gdf['geoid'] = "36047" + gdf['TRACTCE00']

    final_gdf = gdf.merge(combined, on='geoid', how='left')
    return (final_gdf,)


@app.cell
def _(final_gdf, pd, plt):
    # Gentrification Logic: Did property values grow more than inflation?
    final_gdf['val_growth'] = pd.to_numeric(final_gdf['med_val_12']) > final_gdf['med_val_00_adj']

    fig, ax = plt.subplots(figsize=(10, 8))
    final_gdf.plot(column='val_growth', cmap='OrRd', legend=True, ax=ax)
    ax.set_title("Tracts where Home Values Outpaced Inflation (2000-2012)")
    ax.axis("off")
    plt.show()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
