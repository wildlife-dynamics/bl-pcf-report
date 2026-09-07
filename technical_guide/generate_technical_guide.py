"""
Generate the BL PCF Report Technical Guide as a PDF using ReportLab.
Run with: python3 generate_technical_guide.py
Output: bl_pcf_report_technical_guide.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak,
)
from datetime import date

OUTPUT_FILE = "bl_pcf_report_technical_guide.pdf"

# ── Colour palette ─────────────────────────────────────────────────────────────
GREEN_DARK  = colors.HexColor("#115631")
GREEN_MID   = colors.HexColor("#2d6a4f")
AMBER       = colors.HexColor("#e7a553")
SLATE       = colors.HexColor("#3d3d3d")
LIGHT_GREY  = colors.HexColor("#f5f5f5")
MID_GREY    = colors.HexColor("#cccccc")
WHITE       = colors.white

# ── Styles ─────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def _style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=styles[parent], **kw)
    styles.add(s)
    return s

TITLE    = _style("DocTitle",    fontSize=26, leading=32, textColor=GREEN_DARK,
                  spaceAfter=6,  alignment=TA_CENTER, fontName="Helvetica-Bold")
SUBTITLE = _style("DocSubtitle", fontSize=13, leading=18, textColor=SLATE,
                  spaceAfter=4,  alignment=TA_CENTER)
META     = _style("Meta",        fontSize=9,  leading=13, textColor=colors.grey,
                  alignment=TA_CENTER, spaceAfter=2)
H1       = _style("H1", fontSize=15, leading=20, textColor=GREEN_DARK,
                  spaceBefore=18, spaceAfter=6, fontName="Helvetica-Bold")
H2       = _style("H2", fontSize=12, leading=16, textColor=GREEN_MID,
                  spaceBefore=12, spaceAfter=4, fontName="Helvetica-Bold")
H3       = _style("H3", fontSize=10, leading=14, textColor=SLATE,
                  spaceBefore=8,  spaceAfter=3, fontName="Helvetica-Bold")
BODY     = _style("Body", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=6, alignment=TA_JUSTIFY)
BULLET   = _style("BulletItem", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=3, leftIndent=14, firstLineIndent=-10, bulletIndent=4)
CODE     = _style("InlineCode", fontSize=8, leading=12, fontName="Courier",
                  backColor=LIGHT_GREY, textColor=colors.HexColor("#c0392b"),
                  spaceAfter=4, leftIndent=10, rightIndent=10, borderPad=3)
NOTE     = _style("Note", fontSize=8.5, leading=13,
                  textColor=colors.HexColor("#555555"),
                  backColor=colors.HexColor("#fff8e1"),
                  leftIndent=10, rightIndent=10, spaceAfter=6, borderPad=4)


def hr():                return HRFlowable(width="100%", thickness=1, color=MID_GREY, spaceAfter=6)
def p(text, style=BODY): return Paragraph(text, style)
def h1(text):            return Paragraph(text, H1)
def h2(text):            return Paragraph(text, H2)
def h3(text):            return Paragraph(text, H3)
def sp(n=6):             return Spacer(1, n)
def bullet(text):        return Paragraph(f"• {text}", BULLET)
def note(text):          return Paragraph(f"<b>Note:</b> {text}", NOTE)

def c(text):
    return Paragraph(str(text), BODY)

def make_table(data, col_widths, header_row=True):
    wrapped = [[c(cell) if isinstance(cell, str) else cell for cell in row]
               for row in data]
    t = Table(wrapped, colWidths=col_widths, repeatRows=1 if header_row else 0)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0 if header_row else -1), GREEN_DARK),
        ("TEXTCOLOR",     (0, 0), (-1, 0 if header_row else -1), WHITE),
        ("FONTNAME",      (0, 0), (-1, 0 if header_row else -1), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
        ("GRID",          (0, 0), (-1, -1), 0.4, MID_GREY),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
    ]))
    return t


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(A4[0] / 2, 1.5 * cm,
                             f"BL PCF Report — Technical Guide  |  Page {doc.page}")
    canvas.restoreState()


# ── Document ───────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT_FILE,
    pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm,
)

W = A4[0] - 4*cm   # usable width

story = []

# ══════════════════════════════════════════════════════════════════════════════
# COVER
# ══════════════════════════════════════════════════════════════════════════════
story += [
    sp(60),
    p("BL PCF Report", TITLE),
    p("Technical Guide", SUBTITLE),
    sp(4),
    p("Predator Compensation Fund — Livestock Predation Incident Analysis", SUBTITLE),
    sp(4),
    p("Version 2.0", META),
    p(f"Generated {date.today().strftime('%B %d, %Y')}", META),
    p("Workflow id: <b>bl-pcf-report</b>", META),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 1. OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("1. Overview"),
    hr(),
    p("The <b>bl-pcf-report</b> workflow ingests livestock predation events "
      "(event type <b>hwc_lvstprd</b>) from EarthRanger for the Amboseli "
      "ecosystem and produces a comprehensive Predator Compensation Fund (PCF) "
      "incident analysis report and dashboard. The workflow covers three target "
      "ranches — <b>Eselengei</b>, <b>Mbirikani</b>, and <b>Kimana</b> — and "
      "restricts analysis to <b>valid claims</b> only."),
    sp(4),
    note(
        "Version 2.1 removes the <code>gee_client</code> connection field, which "
        "was dropped from <code>spec.yaml</code> — this workflow never used it "
        "(it never performed NDVI or other Earth-Engine analysis). Version 2.0 "
        "rewrote this guide against the (then-current) <code>spec.yaml</code>, "
        "correcting the dependency list (migrated to <code>ecoscope-platform</code>), "
        "the actual chart/task names (several task and function names in the "
        "original version did not match any task in <code>spec.yaml</code>), the "
        "previous-period mechanism (a flexible Custom/Preset/Calendar offset, "
        "not a simple integer), the Word report's fixed <code>\"Ecoscope\"</code> "
        "author field and <code>overall_report.docx</code> filename, and the "
        "dashboard, which wires up 24 widgets rather than an empty list."
    ),
    sp(4),
    p("For each run the workflow delivers:"),
    bullet("14 distinct chart-drawing steps, producing 19 chart files (some fan out per ranch) — pie, stacked bar, time-of-day bar, multi-line and multi-bar time series, and a faceted historic comparison chart per ranch"),
    bullet("3 maps — overall predation density grid, boma-attack density grid, and a livestock-species scatter map"),
    bullet("13 summary/breakdown tables (GeoParquet + HTML) — an overall summary, one per-ranch summary per ranch, and breakdowns by claim type, predator, attack location, and boma type"),
    bullet("2 raw event data files (CSV) — cleaned current- and previous-period events"),
    bullet("A Word document report (overall_report.docx) — every chart, map, and table assembled into the Big Life PCF report template"),
    bullet("A 24-widget interactive dashboard"),
    sp(6),
    h2("Output summary"),
    make_table(
        [
            ["Output type", "Count", "Description"],
            ["Pie charts", "5", "Killed & compensation by predator, compensation by ranch, attack location, boma type targeted"],
            ["Stacked bar charts", "3", "Killed & claim count by claim type × ranch; 100%-stacked killed by predator × ranch"],
            ["Time-of-day bar chart", "1", "Predation incidents by 4-hour time bin"],
            ["Multi-line time series", "3", "Killed over time by ranch, by attack location, and claim count over time by type"],
            ["Multi-bar time series", "1", "Animals killed over time per predator (faceted, 2-column grid)"],
            ["Historic comparison chart", "1 task → 3 files", "Current vs. historic mean with 95% CI, faceted by predator, one file per ranch"],
            ["Density grid maps", "2", "All predation incidents; boma attacks only"],
            ["Scatter map", "1", "Livestock species scatter map"],
            ["Summary/breakdown tables (GeoParquet + HTML)", "13", "Overall, 3× per-ranch, claim type, predator, location, predator×location, boma"],
            ["Raw event data (CSV)", "2", "current_events.csv, previous_events.csv"],
            ["Word document", "1", "overall_report.docx"],
            ["Dashboard widgets", "24", "Every chart, map, and table above; ranch-level charts/tables merged into 2 switchable widgets"],
        ],
        [5*cm, 3*cm, W - 8*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 2. DEPENDENCIES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("2. Dependencies"),
    hr(),
    h2("2.1  Python packages"),
    p("The workflow declares eight versioned packages, resolved from the "
      "Ecoscope prefix.dev channels:"),
    make_table(
        [
            ["Package", "Version", "Channel"],
            ["ecoscope-platform",                  "2.18.0",       "ecoscope-workflows"],
            ["ecoscope-workflows-ext-custom",       "0.1.0rc14.*",  "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-ste",          "0.0.0rc1.*",   "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-mnc",          "1.0.0.*",      "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-wwf-virunga",  "0.0.0rc9.*",   "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-big-life",     "1.0.0.*",      "ecoscope-workflows-custom"],
            ["pydeck",                              "0.9.2",        "conda-forge"],
            ["opentelemetry-sdk",                   "&gt;=1.20.0,&lt;2.0.0", "conda-forge"],
        ],
        [7*cm, 3.5*cm, W - 10.5*cm],
    ),
    p(
        "The chart-drawing tasks (pie, bar, multi-line, multi-bar, faceted "
        "historic time series) come from <code>ecoscope-workflows-ext-wwf-virunga</code>. "
        "<code>fill_missing_values</code> and the integer-conversion helper come from "
        "<code>ecoscope-workflows-ext-mnc</code>. The Dropbox fetch, previous-period "
        "calculation, envelope/view-state, and map-layer combination tasks come from "
        "<code>ecoscope-workflows-ext-ste</code>. The Word-report generation task "
        "comes from <code>ecoscope-workflows-ext-big-life</code>."
    ),
    sp(6),
    h2("2.2  External data — static Amboseli layers"),
    p("Three GeoPackage files are downloaded from Dropbox at run time and "
      "cached locally (<code>overwrite_existing: false</code>, 3 retries):"),
    make_table(
        [
            ["File", "Purpose"],
            ["amboseli_ranch_conservancies_layers.gpkg",
             "Land-use styling layer overlaid on all maps"],
            ["amboseli_group_ranch_boundaries_x_electric_fence.gpkg",
             "Ranch boundaries and electric fence overlay"],
            ["amboseli_group_ranch_boundaries.gpkg",
             "Conservancy boundary polygons (reprojected, not otherwise used downstream)"],
        ],
        [8*cm, W - 8*cm],
    ),
    sp(6),
    h2("2.3  Base map tiles"),
    p("Two ESRI tile layers are composited for every map:"),
    make_table(
        [
            ["Layer", "Opacity", "Max zoom"],
            ["ESRI World Hillshade", "1.0", "20"],
            ["ESRI World Street Map", "0.15", "20"],
        ],
        [5*cm, 3*cm, W - 8*cm],
    ),
    sp(6),
    h2("2.4  EarthRanger connection"),
    p("A single EarthRanger connection (<code>set_er_connection</code>) is "
      "required and reused for both the current- and previous-period event fetches."),
    sp(6),
    h2("2.5  Grouper"),
    p("The workflow groups data by the <b>Ranch</b> column (fixed via "
      "<code>set_groupers</code>, not user-configurable). This grouper drives "
      "every per-ranch table split and the ranch-level historic chart fan-out."),
    sp(6),
    h2("2.6  Time frequency"),
    p("A user-selectable <code>time_frequency</code> parameter "
      "(<code>select_time_frequency</code> — Annual / Monthly / Weekly / Daily) "
      "controls the temporal aggregation unit used by all multi-line and "
      "multi-bar time-series charts, and by the historic comparison chart."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 3. DATA INGESTION AND PROCESSING
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("3. Data Ingestion and Processing"),
    hr(),
    h2("3.1  Dual pipeline — current and previous period"),
    p(
        "Events of type <code>hwc_lvstprd</code> are fetched twice: once for the "
        "selected time range (<code>get_current_events</code>, "
        "<code>raise_on_empty: true</code>) and once for the comparison period "
        "(<code>get_previous_events</code>, <code>raise_on_empty: false</code>, "
        "so an empty previous period doesn't fail the run). Both event sets pass "
        "through an identical transformation chain before diverging into the "
        "overall/per-ranch summaries and the historic comparison chart."
    ),
    sp(6),
    h2("3.2  Previous period calculation"),
    p(
        "The comparison window is computed by "
        "<code>ecoscope_workflows_ext_ste.tasks.filter.flexible_previous_period</code> "
        "(task id <code>set_previous_period</code>), which always ends the "
        "comparison period on the current time range's start date, then works "
        "backward. The user chooses one of three offset modes in the form: "
        "<b>Custom</b> (Years/Months/Weeks/Days, default 1 month), <b>Preset</b> "
        "(e.g. 1/3/6 months or 1 year back), or <b>Calendar</b> (an exact start date)."
    ),
    sp(6),
    h2("3.3  Field normalisation"),
    p("Each pipeline (current and previous) applies the same sequence:"),
    make_table(
        [
            ["Step", "Task", "Purpose"],
            ["1", "process_events_details",
             "Maps EarthRanger detail keys to their display titles (map_to_titles: true, ordered: true)"],
            ["2", "normalize_json_column",
             "Flattens the event_details JSON column into individual event_details__&lt;title&gt; columns"],
            ["3", "drop_column_prefix (×2)",
             "Strips the event_details__ prefix, then the hwc_lvstprd__ prefix, duplicate_strategy: keep_original"],
            ["4", "map_columns",
             "Drops ~30 unused detail columns (herder info, verification metadata, boma coordinates, etc.); retains the rest as-is"],
        ],
        [1.3*cm, 3.5*cm, W - 4.8*cm],
    ),
    sp(6),
    h2("3.4  Filtering"),
    p("Two filters are applied in sequence, via <code>filter_row_values</code>:"),
    bullet("<b>Ranch filter</b> — retains only rows where <code>Ranch</code> is one of Eselengei, Mbirikani, or Kimana"),
    bullet('<b>Validity filter</b> — retains only rows where <code>"Validity of claim"</code> == <code>"Valid"</code>'),
    sp(6),
    h2("3.5  Livestock-kill totals"),
    p(
        "The adult and young kill counts are each combined from two possible "
        "source columns via <code>create_combined_column</code> (primary column, "
        "with a fallback if the primary is null, <code>fill_remaining: 0</code>):"
    ),
    make_table(
        [
            ["Output column", "Primary column", "Fallback column"],
            ["total_adult_livestock_killed", "Adults killed", "hwc_lvstpd_number_adults killed"],
            ["total_young_livestock_killed", "Young (&lt;1yr) killed", "hwc_lvstprd_&lt;1yr"],
        ],
        [5*cm, 4.5*cm, W - 9.5*cm],
    ),
    p(
        "<code>convert_column_values_to_numeric</code> then casts "
        "<code>Compensation value to owner</code>, "
        "<code>total_adult_livestock_killed</code>, and "
        "<code>total_young_livestock_killed</code> to numeric, and "
        "<code>fill_missing_values</code> fills any remaining nulls in those three "
        "columns with <code>0</code>."
    ),
    p(
        "A second <code>fill_missing_values</code> pass fills nulls in "
        "<code>Animal responsible</code>, <code>Boma type</code>, "
        "<code>Livestock species</code>, <code>Type of claim</code>, and "
        "<code>Where were the livestock when the attack happened</code> with the "
        "string <code>\"Unknown\"</code>."
    ),
    p(
        "Finally, <code>apply_arithmetic_operation_over_rows</code> (operation: add) "
        "computes the column every downstream chart and table is built from:"
    ),
    p("<i>total_animals_killed = total_adult_livestock_killed + total_young_livestock_killed</i>", CODE),
    p(
        "The cleaned current- and previous-period tables are persisted as "
        "<code>current_events.csv</code> and <code>previous_events.csv</code>."
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 4. SUMMARY TABLES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("4. Summary Tables"),
    hr(),
    h2("4.1  Overall predation summary"),
    p(
        "Three crosstabs — incidents (count), animals killed (sum), and "
        "compensation value (sum), each indexed by <code>Animal responsible</code> "
        "with <code>Livestock species</code> as columns and a Total margin — are "
        "computed from the current-period events via <code>crosstab_summary</code> "
        "and combined into one table by <code>summarize_predation_table</code> "
        "(<code>overall_summary_table</code>), then persisted as GeoParquet "
        "(<code>overall_predation_summary</code>)."
    ),
    sp(6),
    h2("4.2  Per-ranch summaries"),
    p(
        "<code>split_groups</code> partitions the current-period events by "
        "<code>Ranch</code> (<code>split_by_ranch</code>). For each ranch, the "
        "same three crosstabs are computed via <code>mapvalues</code> and combined "
        "with <code>summarize_predation_table</code>. The ranch name for each "
        "partition is extracted with <code>column_first_unique_value</code> and "
        "zipped onto its summary table (<code>groupbykey</code>), so each ranch's "
        "table is persisted under a filename equal to the ranch name itself "
        "(e.g. a file literally named <code>Eselengei</code>)."
    ),
    sp(6),
    h2("4.3  Breakdown tables"),
    p("All computed from the current-period events via <code>crosstab_summary</code>, then formatted with <code>convert_columns_to_int</code> and <code>format_numbers_with_commas</code>:"),
    make_table(
        [
            ["Output id", "Rows × Columns", "Value"],
            ["livestock_killed_by_claim_type", "Type of claim × Ranch", "sum(total_animals_killed)"],
            ["livestock_killed_by_predator_species", "Animal responsible × Ranch", "sum(total_animals_killed)"],
            ["livestock_attacks_by_location", "attack location (single dimension)", "count + percentage"],
            ["predation_incidents_by_predator_and_location", "Animal responsible × attack location", "count of id, merged with per-predator incident totals and percentages"],
            ["predation_incidents_by_boma_type", "Boma type (single dimension)", "count + percentage"],
        ],
        [5.5*cm, 6*cm, W - 11.5*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 5. COLOR MAPPING
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("5. Color Mapping"),
    hr(),
    p(
        "Six colour maps are assigned via <code>map_column_value</code>, each "
        "adding a dedicated hex-colour column to the current-period events "
        "GeoDataFrame. <code>add_rgba_columns_from_hex</code> then converts all "
        "six into <code>&lt;column&gt;_rgba</code> variants — it is the "
        "<code>_rgba</code> columns, not the raw hex columns, that are wired into "
        "the chart and map <code>color_column</code> parameters."
    ),
    sp(6),
    h2("5.1  Animal responsible"),
    make_table(
        [
            ["Animal", "Hex color", "Animal", "Hex color"],
            ["Caracal",   "#fd7f6f", "Leopard",  "#ffee65"],
            ["Cheetah",   "#7eb0d5", "Lion",     "#beb9db"],
            ["Elephant",  "#b2e061", "Unknown",  "#cfcfc4"],
            ["Hyena",     "#bd7ebe", "Wild dog", "#4cc9b0"],
            ["Jackal",    "#ffb55a", "—",        "—"],
        ],
        [3.5*cm, 2.8*cm, 3.5*cm, 2.8*cm],
    ),
    sp(6),
    h2("5.2  Other color maps"),
    make_table(
        [
            ["Color map", "Key", "Hex color"],
            ["Boma type",         "Permanent",                      "#fd7f6f"],
            ["Boma type",         "Temporary",                      "#7eb0d5"],
            ["Livestock location","Inside Boma",                    "#fd7f6f"],
            ["Livestock location","More than 200m from Boma",       "#7eb0d5"],
            ["Livestock location","Within 200m of Boma",            "#b2e061"],
            ["Claim type",        "Bad Boma",                       "#beb9db"],
            ["Claim type",        "No Penalty",                     "#b2e061"],
            ["Claim type",        "Lost in the Bush",               "#7eb0d5"],
            ["Ranch",             "Eselengei",                      "#fd7f6f"],
            ["Ranch",             "Kimana",                         "#7eb0d5"],
            ["Ranch",             "Mbirikani",                      "#b2e061"],
            ["Livestock species", "Shoat",                          "#0000ff"],
            ["Livestock species", "Cow",                            "#8b0000"],
            ["Livestock species", "Donkey",                         "#ffff00"],
        ],
        [4*cm, 6*cm, W - 10*cm],
    ),
    p("Any category value not present in a mapping falls back to <code>#f0f8ff</code> (<code>keep_unmapped: false</code> drops rows whose value has no explicit mapping and isn't the default)."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 6. CHARTS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("6. Charts"),
    hr(),
    h2("6.1  Pie charts"),
    p(
        "All five pie charts use "
        "<code>ecoscope_workflows_ext_wwf_virunga.tasks.plot._plot.draw_pie_chart</code> "
        "with <code>textinfo: \"percent+label+value\"</code>, <code>font_size: 12</code>, "
        "<code>showlegend: true</code>."
    ),
    make_table(
        [
            ["Output file", "Value column", "Label / colour column"],
            ["livestock_killed_by_predator_pie",
             "total_animals_killed",
             "Animal responsible / animal_responsible_colors_rgba"],
            ["compensation_value_by_predator_pie",
             "Compensation value to owner",
             "Animal responsible / animal_responsible_colors_rgba"],
            ["compensation_value_by_ranch_pie",
             "Compensation value to owner",
             "Ranch / ranch_colors_rgba"],
            ["livestock_attack_location_pie",
             "Where were the livestock&hellip; (categorical)",
             "livestock_attack_colors_rgba"],
            ["boma_type_targeted_pie",
             "Boma type (categorical)",
             "boma_type_colors_rgba"],
        ],
        [5*cm, 5*cm, W - 10*cm],
    ),
    sp(6),
    h2("6.2  Stacked bar charts"),
    p(
        "Three charts use <code>ecoscope_workflows_ext_wwf_virunga.tasks.plot.draw_bar_chart</code> "
        "(<code>mode: stacked</code> or <code>percent_stacked</code>), category axis "
        "<code>Ranch</code>, <code>plot_bgcolor: #f5f5f5</code>, <code>bargap/bargroupgap: 0.05</code>."
    ),
    make_table(
        [
            ["Output file", "Y axis / agg", "Stack column", "Stack order"],
            ["livestock_killed_by_claim_type_bar",
             "total_animals_killed / sum",
             "Type of claim",
             "Lost in the Bush &rarr; No Penalty &rarr; Bad Boma"],
            ["claim_count_by_type_bar",
             "id / count",
             "Type of claim",
             "Lost in the Bush &rarr; No Penalty &rarr; Bad Boma"],
            ["livestock_killed_by_predator_pct_bar",
             "total_animals_killed / sum (percent_stacked)",
             "Animal responsible",
             "Hyena &rarr; Jackal &rarr; Lion"],
        ],
        [5.5*cm, 3.5*cm, 3*cm, W - 12*cm],
    ),
    sp(6),
    h2("6.3  Time-of-day bar chart"),
    p(
        "Built with <code>draw_bar_chart</code> (<code>mode: grouped</code>, "
        "<code>category: \"Time of attack\"</code>, agg_func count, "
        "<code>showlegend: false</code>, bar colour <code>#6495ed</code>)."
    ),
    make_table(
        [
            ["Time bin", "Hours covered"],
            ["Morning",   "06:00 – 11:59"],
            ["Afternoon", "12:00 – 16:59"],
            ["Evening",   "17:00 – 19:59"],
            ["Night",     "20:00 – 05:59"],
        ],
        [4*cm, W - 4*cm],
    ),
    p("Output: <b>predation_incidents_by_time_of_day_bar</b>"),
    sp(6),
    h2("6.4  Multi-line time-series charts"),
    p(
        "Three charts use <code>draw_grouped_line_time_series_chart</code>, all "
        "driven by the user-selected <code>time_frequency</code>."
    ),
    make_table(
        [
            ["Output file", "Group column", "Y / agg", "Fill", "Group order"],
            ["livestock_killed_over_time_by_ranch_chart",
             "Ranch", "total_animals_killed / sum", "No",
             "Eselengei &rarr; Mbirikani &rarr; Kimana"],
            ["livestock_killed_over_time_by_attack_location_chart",
             "attack location", "total_animals_killed / sum", "Yes",
             "Inside Boma &rarr; Within 200m &rarr; More than 200m"],
            ["claim_count_over_time_by_type_chart",
             "Type of claim", "id / count", "Yes",
             "Lost in the Bush &rarr; No Penalty &rarr; Bad Boma"],
        ],
        [5.5*cm, 3*cm, 3*cm, 1.3*cm, W - 12.8*cm],
    ),
    sp(6),
    h2("6.5  Multi-bar time-series chart (faceted per predator)"),
    p(
        "Built with <code>draw_faceted_bar_time_series_chart</code>: "
        "<code>total_animals_killed</code> summed per <code>Animal responsible</code>, "
        "in a 2-column subplot grid (<code>ncols: 2</code>, "
        "<code>row_height: 350</code>, <code>shared_yaxes: false</code>), bar colour "
        "<code>#6495ed</code>. Screenshot: 1280 &times; 2000 px."
    ),
    p("Output: <b>livestock_killed_over_time_by_predator_mulit_bar_chart</b>"),
    sp(6),
    h2("6.6  Historic comparison chart (per ranch)"),
    p(
        "<code>generate_grouped_historical_stats_table</code> is mapped once per "
        "ranch over the current/previous partitions (<code>group_ranch_level_groupers</code> "
        "zips <code>split_by_ranch</code> with <code>split_previous_by_ranch</code>), "
        "producing a stats table per ranch with a 95% confidence interval "
        "(<code>band_method: ci_mean</code>, <code>band_level: 0.95</code>) around "
        "the historic mean of <code>total_animals_killed</code>, grouped by "
        "<code>Animal responsible</code>. <code>draw_faceted_historic_timeseries</code> "
        "then renders one faceted chart per ranch (facet = predator, "
        "<code>ncols: 2</code>, <code>row_height: 300</code>):"
    ),
    make_table(
        [
            ["Visual element", "Column", "Colour"],
            ["Current value line", "current_value", "rgb(0, 0, 139) — dark blue"],
            ["Historic mean line", "historic_mean", "#ff8c00 — dark orange"],
            ["Historic 95% CI band", "historic_min / historic_max", "rgb(143, 188, 139, 0.5) — translucent sage green"],
        ],
        [4.5*cm, 4.5*cm, W - 9*cm],
    ),
    p(
        "Outputs: <b>ranch_level_historic_time_series_chart_&lt;ranch&gt;</b> — "
        "one file per ranch, filename suffixed with the ranch name (via "
        "<code>groupbykey</code> zipping the ranch name onto the rendered chart). "
        "Screenshot: 1280 &times; 2000 px."
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 7. MAPS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("7. Maps"),
    hr(),
    p(
        "All three maps share the same base-tile stack (Hillshade + Street Map) "
        "and the same three Amboseli overlay layers (land use, ranch boundaries, "
        "electric fence) as static layers, framed by a shared view state "
        "(<code>envelope_gdf</code>, expansion factor 1.05; "
        "<code>compute_view_state_from_gdf</code>, pitch 0, bearing 0, max zoom 15). "
        "Map screenshots use <code>device_scale_factor: 2.0</code> and "
        "<code>wait_for_timeout: 40000</code> ms to allow the base tiles to fully render."
    ),
    sp(6),
    h2("7.1  Livestock predation event map"),
    p(
        "<code>create_scatterplot_layer</code> plots every current-period event "
        "as a point, coloured by <code>livestock_species_colors_rgba</code> "
        "(<code>get_radius: 4</code>, opacity 0.75). Legend sorted ascending by "
        "livestock species."
    ),
    make_table(
        [
            ["Livestock species", "Colour"],
            ["Shoat",   "#0000ff (blue)"],
            ["Cow",     "#8b0000 (dark red)"],
            ["Donkey",  "#ffff00 (yellow)"],
        ],
        [4*cm, W - 4*cm],
    ),
    p("Output: <b>livestock_predation_event_map</b>"),
    sp(6),
    h2("7.2  Predation incident density map"),
    p(
        "All current-period events are gridded into a 2000 m mesh "
        "(<code>create_meshgrid</code>, EPSG:3857) and a per-cell point count "
        "(<code>calculate_feature_density</code>). Zero-density cells are dropped, "
        "and the remaining density values are classified into 5 equal-interval "
        "bins (<code>apply_classification</code>) and coloured yellow-to-dark-red:"
    ),
    make_table(
        [
            ["Bin rank", "Hex colour"],
            ["1 (lowest)", "#FFF7BC"],
            ["2",          "#FD8D3C"],
            ["3",          "#F03B20"],
            ["4",          "#BD0026"],
            ["5 (highest)","#99000D"],
        ],
        [4*cm, W - 4*cm],
    ),
    p(
        "Grid cells are rendered as filled GeoJSON polygons (opacity 0.55, black "
        "outline, 0.35 px line width). Output: <b>predation_incident_density_map</b>"
    ),
    sp(6),
    h2("7.3  Boma predation density map"),
    p(
        "Identical pipeline to &sect;7.2, but events are first filtered to "
        "<code>\"Where were the livestock when the attack happened\" == \"Inside Boma\"</code> "
        "before gridding. Same 2000 m mesh, equal-interval k=5 classification, and "
        "colour ramp."
    ),
    p("Output: <b>boma_predation_density_map</b>"),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 8. WORD REPORT & DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("8. Word Report &amp; Dashboard"),
    hr(),
    h2("8.1  Template"),
    p(
        "The Word template <code>pcf_report_template.docx</code> is downloaded "
        "from Dropbox at run time (<code>overwrite_existing: false</code>, 3 "
        "retries) via <code>fetch_and_persist_file</code>."
    ),
    sp(6),
    h2("8.2  Report generation"),
    p("<code>generate_pcf_report</code> populates the template with every chart, map, and table:"),
    make_table(
        [
            ["Field",          "Value"],
            ["template_path",  "downloaded pcf_report_template.docx"],
            ["output_dir",     "$ECOSCOPE_WORKFLOWS_RESULTS"],
            ["filename",       "overall_report.docx"],
            ["time_period",    "the workflow's current time range"],
            ["generated_by",   "\"Ecoscope\" (fixed string — not resolved from the EarthRanger user)"],
            ["validate_images","true — verifies every expected image exists before populating"],
        ],
        [3.5*cm, W - 3.5*cm],
    ),
    sp(6),
    h2("8.3  Dashboard"),
    p(
        "<code>gather_dashboard</code> registers <b>24 widgets</b> — every chart, "
        "map, and table produced by the run. Two of them are merged multi-view "
        "widgets built with <code>merge_widget_views</code>:"
    ),
    bullet("<b>Historic Predation Trend by Ranch</b> — the 3 per-ranch historic comparison charts, merged into a single widget the viewer can switch between"),
    bullet("<b>Predation Summary by Ranch</b> — the 3 per-ranch summary tables, merged the same way"),
    p(
        "The remaining 22 widgets are single-view plot, map, and table widgets — "
        "one per chart/map/breakdown table described in &sect;6 and &sect;7, plus "
        "the overall summary table and the four breakdown tables from &sect;4.3."
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 9. OUTPUT FILES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("9. Output Files"),
    hr(),
    p("All outputs are written to <b>$ECOSCOPE_WORKFLOWS_RESULTS</b>:"),
    make_table(
        [
            ["File", "Description"],
            ["current_events.csv / previous_events.csv",
             "Cleaned, filtered current- and previous-period event tables"],
            ["overall_predation_summary (GeoParquet + .html)",
             "Incidents, killed, compensation by predator, overall"],
            ["&lt;ranch&gt; (GeoParquet + .html, one per ranch, named after the ranch)",
             "The same summary, per ranch"],
            ["livestock_killed_by_claim_type (GeoParquet + .html)",
             "Animals killed by claim type × ranch"],
            ["livestock_killed_by_predator_species (GeoParquet + .html)",
             "Animals killed by predator × ranch"],
            ["livestock_attacks_by_location (GeoParquet + .html)",
             "Incident count/pct by attack location"],
            ["predation_incidents_by_predator_and_location (GeoParquet + .html)",
             "Incident count/pct by predator × attack location"],
            ["predation_incidents_by_boma_type (GeoParquet + .html)",
             "Incident count/pct by boma type"],
            ["livestock_killed_by_predator_pie / compensation_value_by_predator_pie / "
             "compensation_value_by_ranch_pie / livestock_attack_location_pie / "
             "boma_type_targeted_pie (.html + .png)",
             "5 pie charts — see &sect;6.1"],
            ["livestock_killed_by_claim_type_bar / claim_count_by_type_bar / "
             "livestock_killed_by_predator_pct_bar (.html + .png)",
             "3 stacked bar charts — see &sect;6.2"],
            ["predation_incidents_by_time_of_day_bar (.html + .png)",
             "Time-of-day bar chart — see &sect;6.3"],
            ["livestock_killed_over_time_by_ranch_chart / "
             "livestock_killed_over_time_by_attack_location_chart / "
             "claim_count_over_time_by_type_chart (.html + .png)",
             "3 multi-line time series — see &sect;6.4"],
            ["livestock_killed_over_time_by_predator_mulit_bar_chart (.html + .png)",
             "Faceted multi-bar time series — see &sect;6.5"],
            ["ranch_level_historic_time_series_chart_&lt;ranch&gt; (.html + .png, one per ranch)",
             "Historic comparison chart — see &sect;6.6"],
            ["livestock_predation_event_map (.html + .png)",
             "Scatter map — see &sect;7.1"],
            ["predation_incident_density_map (.html + .png)",
             "Density grid — see &sect;7.2"],
            ["boma_predation_density_map (.html + .png)",
             "Density grid — see &sect;7.3"],
            ["overall_report.docx",
             "Final populated Word PCF report"],
            ["amboseli_ranch_conservancies_layers.gpkg / "
             "amboseli_group_ranch_boundaries_x_electric_fence.gpkg / "
             "amboseli_group_ranch_boundaries.gpkg / pcf_report_template.docx",
             "Cached inputs downloaded from Dropbox"],
        ],
        [7*cm, W - 7*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 10. WORKFLOW EXECUTION LOGIC
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("10. Workflow Execution Logic"),
    hr(),
    h2("10.1  Skip conditions"),
    p(
        "Every task carries the two default skip conditions from "
        "<code>task-instance-defaults</code>: <b>any_is_empty_df</b> (skip if any "
        "input DataFrame is empty) and <b>any_dependency_skipped</b> (skip if an "
        "upstream task was skipped). This propagates gracefully through the "
        "pipeline — if no valid events exist for a ranch or for the previous "
        "period, all downstream tasks in that branch are skipped rather than "
        "raising an error."
    ),
    p(
        "The current-period event fetch sets <code>raise_on_empty: true</code> "
        "(a zero-event current period is treated as a configuration/data problem "
        "worth surfacing), while the previous-period fetch sets "
        "<code>raise_on_empty: false</code> (a missing comparison period is "
        "expected and handled gracefully)."
    ),
    sp(6),
    h2("10.2  mapvalues / map fan-out"),
    p("<code>mapvalues</code> and <code>map</code> directives fan several steps out per ranch:"),
    bullet("<b>split_by_ranch</b> / <b>split_previous_by_ranch</b> — partition the current/previous events by <code>Ranch</code>"),
    bullet("<b>predation_ranch_incidents / _killed / _compensation</b> — the three crosstabs, computed once per ranch partition"),
    bullet("<b>get_ranch_name</b> — extracts the ranch name string from each partition, later zipped onto that ranch's table/chart output to control its filename suffix"),
    bullet("<b>hist_curr_prev_table</b> / <b>draw_ranch_level_historic_chart</b> — the historic stats table and chart, computed once per ranch from the zipped current+previous partitions"),
    bullet("<b>widget_ranch_historic_chart</b> / <b>widget_ranch_summary_table</b> — per-ranch dashboard widgets, later merged into 2 switchable widgets via <code>merge_widget_views</code>"),
    sp(6),
    h2("10.3  Screenshot timing"),
    make_table(
        [
            ["Task(s)", "wait_for_timeout", "Notes"],
            ["convert_chart_html_png (12 charts, batched)",
             "1 ms", "1280&times;720; static Plotly HTML renders essentially instantly"],
            ["convert_pred_killed_multibar_png",
             "10 ms", "1280&times;2000"],
            ["convert_ranch_historic_chart_png (×3, one per ranch)",
             "10 ms", "1280&times;2000"],
            ["convert_livestock_map_png / convert_density_map_png / convert_density_boma_map_png",
             "40 000 ms", "Maps require full basemap tile rendering before capture"],
        ],
        [5.5*cm, 3.5*cm, W - 9*cm],
    ),
    note(
        "The batched <code>convert_chart_html_png</code> task's "
        "<code>html_path</code> list contains "
        "<code>persist_killed_pred_stacked_bar</code> twice in <code>spec.yaml</code> "
        "— a harmless duplicate entry, not a second distinct chart."
    ),
    sp(6),
    h2("10.4  Geometry cleaning"),
    p(
        "No outlier or null-geometry filtering is applied before the livestock "
        "scatter map in the current pipeline — every valid-claim event with a "
        "point geometry is plotted directly via <code>create_scatterplot_layer</code>."
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 11. SOFTWARE VERSIONS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("11. Software Versions"),
    hr(),
    make_table(
        [
            ["Package", "Version pinned", "Channel"],
            ["ecoscope-platform",                 "2.18.0",              "ecoscope-workflows"],
            ["ecoscope-workflows-ext-custom",     "0.1.0rc14.*",         "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-ste",        "0.0.0rc1.*",          "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-mnc",        "1.0.0.*",             "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-wwf-virunga","0.0.0rc9.*",          "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-big-life",   "1.0.0.*",             "ecoscope-workflows-custom"],
            ["pydeck",                             "0.9.2",              "conda-forge"],
            ["opentelemetry-sdk",                  "&gt;=1.20.0,&lt;2.0.0", "conda-forge"],
        ],
        [7*cm, 4*cm, W - 11*cm],
    ),
    sp(6),
    note(
        "All Ecoscope packages are resolved from the prefix.dev "
        "<code>ecoscope-workflows</code> / <code>ecoscope-workflows-custom</code> "
        "channels. Wildcard patch/prerelease pins (<code>.*</code>) allow "
        "bug-fix releases to be picked up automatically while keeping the "
        "major/minor version — and, for the <code>rc</code>-pinned packages, the "
        "prerelease line — locked. The runtime environment is managed by <b>pixi</b>."
    ),
]

# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"Written → {OUTPUT_FILE}")
