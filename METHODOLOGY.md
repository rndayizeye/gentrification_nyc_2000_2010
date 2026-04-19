# Methodology: Measuring Gentrification in Brooklyn, NY

This document describes the analytical framework, variable definitions, data sources, and classification logic used in the Brooklyn gentrification analysis. For project setup and usage, see [README.md](./README.md).

---

## Theoretical Framework

This study follows the operationalization of gentrification proposed by **Freeman (2005)**, which views gentrification as a process of *class-based succession* — the in-movement of higher-income, more educated households into neighborhoods that had previously experienced sustained disinvestment.

Freeman's framework is chosen because it:
1. Focuses on observable, census-measurable indicators rather than qualitative assessment
2. Distinguishes between tracts that are *eligible* for gentrification and those that actually *experienced* it
3. Has been widely replicated and critiqued in the urban sociology literature, providing a stable methodological baseline

The central concern being measured is whether long-time residents — typically lower-income renters — may be priced out as new investment and higher-income households move in, resulting in rapid shifts in educational attainment and property values.

---

## Data Sources

| Dataset | Source | Year | Geography |
|---|---|---|---|
| Decennial Census SF3 | U.S. Census Bureau API | 2000 | Census tract |
| American Community Survey (ACS) 5-Year | U.S. Census Bureau API | 2010 | Census tract |
| NYC Census Tract Boundaries | NYC OpenData / TIGER/Line | 2000, 2010 | Shapefile |

All data was retrieved programmatically via the U.S. Census Bureau API. No manual downloads were used.

---

## Unit of Analysis

**Census tract**, Brooklyn (Kings County), New York.

Census tracts are the standard unit for neighborhood-level analysis because they are:
- Designed to have roughly equal population (~4,000 residents)
- Stable enough across decennial periods for longitudinal comparison
- The smallest geography with reliable income and housing data from the Census

---

## Analysis Structure

Gentrification is assessed across two distinct periods using a two-stage classification.

---

### Stage 1: Identifying "Gentrifiable" Tracts (Reference Year: 2000)

A census tract is classified as **Gentrifiable** if it lagged behind the broader New York–Newark–Jersey City Metropolitan Statistical Area (MSA) in 2000 on *both* of the following criteria:

#### Criterion 1 — Low Income
```
Tract Median Household Income (2000) < MSA Median Household Income (2000)
```
Tracts falling below the MSA median are considered economically disadvantaged relative to the metro area, indicating potential vulnerability to gentrification pressure.

#### Criterion 2 — Low Recent Construction
```
% Housing Units Built 1980–2000 (tract) < % Housing Units Built 1980–2000 (MSA)
```
A low share of recently constructed housing indicates aging, potentially deteriorating housing stock — a hallmark of disinvested neighborhoods that attract speculative reinvestment.

**Both criteria must be satisfied** for a tract to be classified as Gentrifiable.

---

### Stage 2: Identifying "Gentrifying" Tracts (Change Period: 2000–2010)

A tract is classified as **Gentrifying** if it was *Gentrifiable in 2000* **AND** met both of the following between 2000 and 2010:

#### Criterion 3 — Educational Shift
```
Δ% Bachelor's Degree or Higher (tract, 2000→2010) > Δ% Bachelor's Degree or Higher (MSA, 2000→2010)
```
An above-average increase in educational attainment at the tract level, relative to the MSA, signals the in-movement of higher-education households — a key indicator of gentrification in Freeman's framework.

#### Criterion 4 — Real Property Value Growth
```
Inflation-Adjusted Median Home Value (tract, 2010) > Median Home Value (tract, 2000)
```
Home values are deflated to 2000 dollars using a **CPI deflator of 1.2612** to account for general inflation between 2000 and 2010. A real (inflation-adjusted) increase in home values indicates genuine neighborhood appreciation beyond general price-level changes.

**Both criteria must be satisfied**, in addition to Gentrifiable status, for a tract to be classified as Gentrifying.

---

## Variable Dictionary

| Variable | Census Table | Description | Period |
|---|---|---|---|
| `mhi_tract` | SF3: P053001 | Median Household Income, tract | 2000 |
| `mhi_msa` | SF3: P053001 | Median Household Income, MSA | 2000 |
| `pct_new_housing_tract` | SF3: H034 | % units built 1980–2000, tract | 2000 |
| `pct_new_housing_msa` | SF3: H034 | % units built 1980–2000, MSA | 2000 |
| `pct_bachelors_tract_2000` | SF3: P037 | % pop 25+ with Bachelor's+, tract | 2000 |
| `pct_bachelors_tract_2010` | ACS B15003 | % pop 25+ with Bachelor's+, tract | 2010 |
| `pct_bachelors_msa_2000` | SF3: P037 | % pop 25+ with Bachelor's+, MSA | 2000 |
| `pct_bachelors_msa_2010` | ACS B15003 | % pop 25+ with Bachelor's+, MSA | 2010 |
| `median_home_value_2000` | SF3: H085001 | Median home value, tract | 2000 |
| `median_home_value_2010` | ACS B25077 | Median home value, tract | 2010 |
| `cpi_deflator` | BLS CPI-U | 2000→2010 inflation adjustment | — |

---

## Classification Logic (Summary)

```python
# Stage 1: Gentrifiable
gentrifiable = (
    (tract.mhi_2000 < msa.mhi_2000) &
    (tract.pct_new_housing_2000 < msa.pct_new_housing_2000)
)

# Stage 2: Gentrifying (must be gentrifiable first)
delta_bachelors_tract = tract.pct_bachelors_2010 - tract.pct_bachelors_2000
delta_bachelors_msa   = msa.pct_bachelors_2010  - msa.pct_bachelors_2000

real_home_value_2010 = tract.median_home_value_2010 / CPI_DEFLATOR  # = 1.2612

gentrifying = (
    gentrifiable &
    (delta_bachelors_tract > delta_bachelors_msa) &
    (real_home_value_2010 > tract.median_home_value_2000)
)
```

---

## Limitations

1. **Cross-sectional snapshots:** The analysis uses 2000 and 2010 as fixed endpoints. Gradual or interrupted processes may be missed.
2. **Ecological fallacy:** Tract-level aggregates do not capture within-tract heterogeneity — a tract classified as gentrifying may have pockets of stability.
3. **ACS margin of error:** ACS estimates carry sampling error, particularly in small tracts. High-MOE estimates should be interpreted cautiously.
4. **Displacement not directly measured:** This framework identifies *signs* of gentrification (educational and value change) but does not directly measure resident displacement, which would require longitudinal individual-level data.
5. **CPI deflator:** A single national CPI deflator (1.2612) is used for simplicity. A NYC-specific housing price index would be more precise.

---

## Reference

Freeman, Lance. 2005. "Displacement or Succession?: Residential Mobility in Gentrifying Neighborhoods." *Urban Affairs Review* 40(4): 463–491. https://doi.org/10.1177/1078087404273341
