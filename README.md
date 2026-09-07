# BL PCF Report — User Guide

This guide walks you through configuring and running the Big Life PCF Report workflow, which ingests livestock predation events from EarthRanger and produces a comprehensive Predator Compensation Fund incident analysis report and dashboard for the Amboseli ecosystem.

---

## Overview

The workflow delivers, for each run:

- **Charts** — pie charts by predator, ranch, and attack location; stacked bar charts by claim type and predator; a time-of-day bar chart; multi-line and multi-bar time-series charts; and per-ranch historic (current vs. previous period) comparison charts
- **Maps** — an overall predation-incident density grid, a boma-attack density grid, and a livestock-species scatter map, all overlaid on the Amboseli land use, ranch boundary, and electric fence layers
- **Summary tables** — an overall predation summary, per-ranch summaries, and breakdown tables by claim type, predator species, attack location, and boma type
- **Data files** — the underlying current- and previous-period event tables, plus a GeoParquet file for every summary/breakdown table
- A **Word document report** (`overall_report.docx`) — every chart, map, and table assembled into the Big Life PCF report template, downloaded automatically from Dropbox
- An **interactive dashboard** — 24 widgets covering every chart, map, and table produced by the run (including a single merged, ranch-switchable widget for the historic comparison charts and another for the per-ranch summary tables)

The analysis is restricted to three target ranches — **Eselengei**, **Mbirikani**, and **Kimana** — and to events marked as **valid claims** only.

The three Amboseli geospatial layers and the Word report template are downloaded automatically from Dropbox at run time. No additional setup is required for these.

---

## Prerequisites

Before running the workflow, ensure you have:

- Access to an **EarthRanger** instance with `hwc_lvstprd` (livestock predation) events logged for the analysis period

---

## Step-by-Step Configuration

### Step 1 — Add the Workflow Template

In the workflow runner, go to **Workflow Templates** and click **Add Workflow Template**. Paste the GitHub repository URL into the **Github Link** field:

```
https://github.com/wildlife-dynamics/bl-pcf-report.git
```

Then click **Add Template**.

---

### Step 2 — Add an EarthRanger Connection

Navigate to **Data Sources** and click **Connect**. Select **EarthRanger** from the data source type dialog, then fill in the connection form:

- **Data Source Name** — a label to identify this connection
- **EarthRanger URL** — your instance URL (e.g. `your-site.pamdas.org`)
- **EarthRanger Username** and **EarthRanger Password**

> Credentials are not validated at setup time. Any authentication errors will appear when the workflow runs.

Click **Connect** to save.

---

### Step 3 — Select the Workflow

After the template is added, it appears in the **Workflow Templates** list as **bl-pcf-report**. Click it to open the workflow configuration form.

> The card may show **Initializing…** briefly while the environment is set up.

---

### Step 4 — Set Workflow Details and Report Time Range

The configuration form opens with two sections at the top.

**Set Workflow Details**

| Field | Description |
|-------|-------------|
| Workflow Name | A short name to identify this run |
| Workflow Description | Optional notes (e.g. month, ranch, or reporting period) |

**Set Report Time Range**

| Field | Description |
|-------|-------------|
| Timezone | Select the local timezone (e.g. `Africa/Nairobi UTC+03:00`) |
| Since | Start date and time of the analysis period |
| Until | End date and time of the analysis period |

All livestock predation events are fetched within this window. The analysis covers incidents from the three target ranches — Eselengei, Mbirikani, and Kimana — restricted to valid claims only.

---

### Step 5 — Connect to EarthRanger

Select the EarthRanger data source configured in Step 2 from the **Data Source** dropdown (e.g. `Amboseli Trust for Elephants`).

---

### Step 6 — Previous Period

Define the comparison ("previous") period used by the per-ranch historic charts. Every option computes a period that ends on your selected time range's **Start Date** (so it never overlaps with the current period) — only the comparison period's own start date changes:

| Mode | Behaviour |
|------|-----------|
| **Custom** | Enter your own Years / Months / Weeks / Days offset (defaults to 1 month back) |
| **Preset** | Choose a common lookback — e.g. 1, 3, or 6 months, or 1 year back |
| **Calendar** | Pick an exact Start Date for the comparison period |

If no previous-period events are found, the workflow continues gracefully — downstream charts and tables for that branch are simply skipped rather than the run failing.

---

### Step 7 — Select Time Frequency

Choose the temporal aggregation unit used by all multi-line and multi-bar time-series charts, and by the per-ranch historic comparison charts:

| Option | Description |
|--------|-------------|
| **Annual** | Aggregate by year — best for multi-year trend comparisons |
| **Monthly** | Aggregate by calendar month |
| **Weekly** | Aggregate by ISO week number |
| **Daily** | Aggregate by individual day |

Once all sections are filled, click **Submit**.

---

## Running the Workflow

Once submitted, the runner will:

1. Download the Amboseli land-use, ranch boundary, and electric fence layers from Dropbox and reproject them to EPSG:4326.
2. Fetch `hwc_lvstprd` events from EarthRanger for the selected time range, and separately for the previous-period window.
3. Normalise event details for both periods (field titles, JSON flattening, column renaming), then filter to the three target ranches and to valid claims only.
4. Combine the digital adult/young livestock-kill counts (with fallbacks) into a single total per event, for both periods.
5. Compute the overall and per-ranch summary tables (incidents, animals killed, compensation value), and the claim-type, predator, attack-location, and boma-type breakdown tables.
6. Assign a colour to every relevant category (predator, boma type, attack location, claim type, ranch, livestock species) and render all pie, stacked-bar, time-of-day, and multi-line/multi-bar charts.
7. Build the per-ranch historic comparison chart (current period vs. the previous period's mean and 95% confidence band).
8. Build the livestock-species scatter map, the overall predation density grid, and the boma-attack density grid — each overlaid on the Amboseli base layers.
9. Convert every chart and map to PNG.
10. Download the Big Life PCF Word template from Dropbox and populate it with every chart, map, and table.
11. Assemble the 24-widget dashboard.
12. Save all outputs to the directory specified by `ECOSCOPE_WORKFLOWS_RESULTS`.

---

## Output Files

All outputs are written to `$ECOSCOPE_WORKFLOWS_RESULTS/`:

### Event data

| File | Description |
|------|-------------|
| `current_events.csv` | Cleaned, filtered current-period events, one row per valid claim |
| `previous_events.csv` | Cleaned, filtered previous-period events, one row per valid claim |

### Summary tables (GeoParquet, plus an equivalent `.html` for each dashboard table widget)

| File | Description |
|------|-------------|
| `overall_predation_summary` | Incidents, animals killed, and compensation value by predator, overall |
| `<ranch>` (one file per ranch, named after the ranch) | The same summary, computed separately for each ranch |
| `livestock_killed_by_claim_type` | Animals killed, by claim type × ranch |
| `livestock_killed_by_predator_species` | Animals killed, by predator species × ranch |
| `livestock_attacks_by_location` | Incident count and percentage, by attack location |
| `predation_incidents_by_predator_and_location` | Incident count and percentage, by predator × attack location |
| `predation_incidents_by_boma_type` | Incident count and percentage, by boma type |

### Charts (`.html` + `.png`)

| File | Description |
|------|-------------|
| `livestock_killed_by_predator_pie` | Pie — animals killed by predator |
| `compensation_value_by_predator_pie` | Pie — compensation value by predator |
| `compensation_value_by_ranch_pie` | Pie — compensation value by ranch |
| `livestock_killed_by_claim_type_bar` | Stacked bar — animals killed by claim type × ranch |
| `claim_count_by_type_bar` | Stacked bar — claim count by claim type × ranch |
| `livestock_killed_by_predator_pct_bar` | 100%-stacked bar — animals killed share by predator × ranch |
| `livestock_attack_location_pie` | Pie — attack location distribution |
| `boma_type_targeted_pie` | Pie — boma type targeted (Permanent vs. Temporary) |
| `predation_incidents_by_time_of_day_bar` | Bar — incidents by time-of-day bin |
| `livestock_killed_over_time_by_ranch_chart` | Multi-line — animals killed over time, by ranch |
| `livestock_killed_over_time_by_attack_location_chart` | Multi-line — animals killed over time, by attack location |
| `claim_count_over_time_by_type_chart` | Multi-line — claim count over time, by claim type |
| `livestock_killed_over_time_by_predator_mulit_bar_chart` | Multi-bar (faceted per predator) — animals killed over time |
| `ranch_level_historic_time_series_chart_<ranch>` (one per ranch) | Current period vs. historic mean/95% CI, faceted by predator |

### Maps (`.html` + `.png`)

| File | Description |
|------|-------------|
| `livestock_predation_event_map` | Scatter map of individual events, coloured by livestock species |
| `predation_incident_density_map` | Density grid of all valid predation incidents |
| `boma_predation_density_map` | Density grid of incidents inside a boma only |

### Report

| File | Description |
|------|-------------|
| `overall_report.docx` | Final populated Big Life PCF Word document |

For more detail on how each output is built, see the [Technical Guide](docs/technical-guide.html).
