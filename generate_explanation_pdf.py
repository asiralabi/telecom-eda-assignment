"""
Generates an explanation PDF covering every term and logic block used in:
  - EDA_and_Preprocessing.ipynb
  - Assignment.ipynb
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.colors import HexColor, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, KeepTogether
)

OUT = r"D:\data science\Assignment\Assignment_datascience\Assignment_Explanation.pdf"

styles = getSampleStyleSheet()

H1 = ParagraphStyle('H1', parent=styles['Heading1'], fontSize=18,
                    textColor=HexColor('#0B3D91'), spaceAfter=10)
H2 = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=14,
                    textColor=HexColor('#0B3D91'), spaceAfter=6, spaceBefore=10)
H3 = ParagraphStyle('H3', parent=styles['Heading3'], fontSize=12,
                    textColor=HexColor('#1F4E79'), spaceAfter=4, spaceBefore=6)
BODY = ParagraphStyle('BODY', parent=styles['BodyText'], fontSize=10.5,
                      leading=14, alignment=TA_JUSTIFY, spaceAfter=6)
CODE = ParagraphStyle('CODE', parent=styles['Code'], fontSize=9,
                      leading=11, backColor=HexColor('#F4F4F4'),
                      borderColor=HexColor('#CCCCCC'), borderWidth=0.5,
                      borderPadding=6, leftIndent=4, rightIndent=4,
                      spaceAfter=8, spaceBefore=2)
BULLET = ParagraphStyle('BULLET', parent=BODY, leftIndent=14, bulletIndent=2,
                        spaceAfter=2)


def h1(text): return Paragraph(text, H1)
def h2(text): return Paragraph(text, H2)
def h3(text): return Paragraph(text, H3)
def p(text):  return Paragraph(text, BODY)
def code(text):
    safe = (text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                .replace('\n', '<br/>').replace(' ', '&nbsp;'))
    return Paragraph(f"<font face='Courier'>{safe}</font>", CODE)


def term_block(name, definition, example):
    """A consistent 'Term / Definition / Example' block."""
    rows = [
        [Paragraph(f"<b>{name}</b>", BODY)],
        [Paragraph(f"<b>Definition.</b> {definition}", BODY)],
        [Paragraph(f"<b>Example.</b> {example}", BODY)],
    ]
    t = Table(rows, colWidths=[16 * cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#E8EEF7')),
        ('BOX', (0, 0), (-1, -1), 0.5, HexColor('#9AB0D2')),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, HexColor('#C8D4E8')),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    return KeepTogether([t, Spacer(1, 6)])


story = []

# ---------------------------------------------------------------- TITLE PAGE
story += [
    Spacer(1, 4 * cm),
    h1("Telecom Market in Bangladesh<br/>EDA &amp; Preprocessing — Concept Guide"),
    Spacer(1, 0.4 * cm),
    p("A line-by-line explanation of every term, library function and logical "
      "step used in <b>EDA_and_Preprocessing.ipynb</b> and "
      "<b>Assignment.ipynb</b>. Each concept is given a plain-English "
      "definition followed by a worked example taken from the dataset."),
    Spacer(1, 1 * cm),
    p("<b>Dataset:</b> Telecom Market in Bangladesh — Monthly Subscribers "
      "(2008–2015). 6 operators × 96 months = 576 observations across 7 "
      "columns after tidying."),
    Spacer(1, 0.4 * cm),
    p("<b>Operators covered:</b> Grameenphone, Banglalink, Robi, Airtel, "
      "Citycell, Teletalk."),
    PageBreak(),
]

# ============================================================ PART 1: TERMS
story += [h1("Part 1 — Core Terms &amp; Definitions")]

story += [h2("1.1 Data &amp; Dataset Structure")]

story += [term_block(
    "Dataset",
    "A structured collection of related observations stored in rows and columns.",
    "The telecom dataset contains 576 rows where each row is one operator's "
    "subscriber count for one month."
)]

story += [term_block(
    "Row (Observation / Record)",
    "A single horizontal entry in a table — one real-world fact.",
    "Row 0 says: <i>Airtel, Jan-2008, 2.37 million subscribers, "
    "market share 6.51%</i>."
)]

story += [term_block(
    "Column (Feature / Variable / Attribute)",
    "A vertical slice of the table — one measured property repeated across "
    "every row.",
    "<b>Subscribers_Mn</b> is the column that holds subscriber count "
    "(in millions) for every operator-month combination."
)]

story += [term_block(
    "Tidy (Long) Format",
    "A data layout where each row is one observation and each column is one "
    "variable. Easier for grouping, plotting and modelling than 'wide' layouts.",
    "The raw spreadsheet had months as columns (Jan-2008 … Dec-2015). After "
    "tidying, every (Operator, Date) becomes its own row."
)]

story += [term_block(
    "Wide Format",
    "A layout where one variable is spread across many columns — typical of "
    "spreadsheet exports.",
    "The raw CSV has 96 month columns; tidying via <code>melt</code> reshapes "
    "them into a single <i>Date</i> column."
)]

story += [h2("1.2 Variable Types")]

story += [term_block(
    "Categorical Variable",
    "A variable that takes on labels/categories rather than numeric magnitudes.",
    "<b>Operator</b> has six categories: Grameenphone, Banglalink, Robi, "
    "Airtel, Citycell, Teletalk."
)]

story += [term_block(
    "Nominal Categorical",
    "Categories with no natural order.",
    "<b>Operator</b> — Robi is not 'greater than' Airtel; they are just names."
)]

story += [term_block(
    "Ordinal Categorical",
    "Categories with a meaningful order but no fixed spacing between them.",
    "<b>Month</b> (January &lt; February &lt; …) and <b>Year</b> are ordinal."
)]

story += [term_block(
    "Numerical Variable",
    "A variable measured on a numeric scale where arithmetic makes sense.",
    "<b>Subscribers_Mn</b>, <b>MoM_Growth_%</b>, <b>Market_Share_%</b>."
)]

story += [term_block(
    "Continuous Numerical",
    "Numerical variable that can take any real value within a range.",
    "<b>Market_Share_%</b> = 16.67 — fractions are legitimate."
)]

story += [term_block(
    "Discrete Numerical",
    "Numerical variable that takes only specific (often integer) values.",
    "<b>Year</b> (2008, 2009, …, 2015) — no values in between."
)]

story += [h2("1.3 Statistical Summary Terms")]

story += [term_block(
    "Count",
    "The number of non-missing values in a column.",
    "<code>MoM_Growth_%</code> has count = 570 (out of 576) because 6 first "
    "rows per operator are NaN — there is no 'previous month' to compute "
    "growth from."
)]

story += [term_block(
    "Mean (Average)",
    "Sum of values divided by the count. Sensitive to extreme values.",
    "Mean <b>Subscribers_Mn</b> ≈ 14.03 million across all rows."
)]

story += [term_block(
    "Median (50th percentile)",
    "The middle value when data are sorted. Robust to outliers.",
    "Median <b>Subscribers_Mn</b> ≈ 8.34 million — much lower than the mean, "
    "indicating right-skew (a few giant operators inflate the mean)."
)]

story += [term_block(
    "Minimum / Maximum",
    "Smallest and largest values observed.",
    "Min Subscribers = 0.84M (Teletalk early on); Max = 56.54M (Grameenphone, "
    "Dec-2015)."
)]

story += [term_block(
    "Standard Deviation (std)",
    "Average distance of values from the mean. Larger std = more spread.",
    "Std of <b>Subscribers_Mn</b> ≈ 14.11 — comparable to the mean, "
    "confirming a wide spread."
)]

story += [term_block(
    "Quartiles (Q1, Q2, Q3)",
    "Values that split sorted data into four equal parts. Q1 = 25th "
    "percentile, Q2 = median, Q3 = 75th percentile.",
    "For <b>MoM_Growth_%</b>: Q1 = 0.14, Q3 = 2.29."
)]

story += [term_block(
    "Interquartile Range (IQR)",
    "<code>IQR = Q3 - Q1</code>. Captures the middle 50% of the data.",
    "IQR for <b>MoM_Growth_%</b> = 2.29 − 0.14 = 2.15 percentage points."
)]

story += [term_block(
    "Skewness",
    "Asymmetry of the distribution. Right-skewed = long tail of high values.",
    "<b>Subscribers_Mn</b> is right-skewed (mean &gt; median) because "
    "Grameenphone's huge values pull the tail."
)]

story += [h2("1.4 Data-Quality Terms")]

story += [term_block(
    "Missing Value (NaN)",
    "An entry where no value is recorded.",
    "<b>MoM_Growth_%</b> is NaN for the very first month of every operator — "
    "growth requires a previous month."
)]

story += [term_block(
    "Duplicate Record",
    "Two or more rows that are identical (or share the same key).",
    "<code>df.duplicated().sum()</code> returns 0 — no operator-month appears "
    "twice."
)]

story += [term_block(
    "Outlier",
    "A value far from the bulk of the data. May indicate a special event or "
    "a measurement error.",
    "51 rows have <b>MoM_Growth_%</b> outside <code>[Q1−1.5·IQR, "
    "Q3+1.5·IQR]</code> = [−3.07, 5.50] — including Airtel's −41.7% jump "
    "(operator rebranding)."
)]

story += [term_block(
    "Interpolation",
    "Estimating missing values from neighbouring observations (commonly "
    "linear).",
    "<code>s.interpolate()</code> would fill a missing Robi value in "
    "Mar-2010 by linearly averaging Feb-2010 and Apr-2010."
)]

story += [term_block(
    "Forward-fill / Back-fill",
    "Filling NaNs using the last (ffill) or next (bfill) valid value.",
    "<code>.ffill().bfill()</code> handles leading/trailing NaNs that "
    "interpolation cannot."
)]

story += [h2("1.5 Engineered Features")]

story += [term_block(
    "Month-over-Month Growth (MoM_Growth_%)",
    "Percentage change of a value from the previous month: "
    "<code>(Vt − V(t−1)) / V(t−1) × 100</code>.",
    "Airtel went from 2.37M (Jan-2008) to 2.60M (Feb-2008): "
    "(2.60−2.37)/2.37 × 100 ≈ <b>9.70%</b>."
)]

story += [term_block(
    "Market Share",
    "An operator's subscribers expressed as a percentage of total sector "
    "subscribers in the same month.",
    "Jan-2008: total sector ≈ 36.43M; Grameenphone ≈ 16.88M → share "
    "≈ 16.88/36.43 ≈ <b>46.3%</b>."
)]

story += [term_block(
    "Correlation Coefficient",
    "A value between −1 and +1 measuring linear association between two "
    "variables. 0 = no linear relation.",
    "<b>Subscribers_Mn</b> vs <b>Market_Share_%</b> = 0.88 (strong positive) "
    "— bigger operators have higher share."
)]

story += [PageBreak()]

# =========================================================== PART 2: LIBRARIES
story += [h1("Part 2 — Libraries &amp; Key Functions Used")]

story += [h2("2.1 Libraries")]

story += [term_block(
    "pandas (pd)",
    "Python library for tabular data. Provides DataFrame (table) and Series "
    "(column) objects.",
    "<code>pd.read_csv(...)</code> loads the telecom CSV into a DataFrame."
)]

story += [term_block(
    "NumPy (np)",
    "Numerical computing library. Provides arrays and math utilities.",
    "<code>np.number</code> is used by "
    "<code>select_dtypes(include=np.number)</code> to pick all numeric "
    "columns."
)]

story += [term_block(
    "matplotlib.pyplot (plt)",
    "Foundational plotting library.",
    "<code>plt.figure(figsize=(11,5))</code> sets the canvas size before "
    "plotting subscriber trends."
)]

story += [term_block(
    "seaborn (sns)",
    "High-level statistical plotting library built on matplotlib.",
    "<code>sns.lineplot(data=df, x='Date', y='Subscribers_Mn', "
    "hue='Operator')</code> draws one coloured line per operator."
)]

story += [h2("2.2 pandas Functions in This Project")]

story += [term_block(
    "read_csv",
    "Loads a CSV file into a DataFrame.",
    "<code>pd.read_csv('telecom_clean.csv', parse_dates=['Date'])</code> "
    "— and <code>parse_dates</code> converts the Date string column to real "
    "datetime values."
)]

story += [term_block(
    "iloc",
    "Integer-position based indexing — selects rows/columns by number.",
    "<code>raw.iloc[4:10, 2:2+96]</code> selects rows 4–9 and 96 monthly "
    "value columns from the raw spreadsheet."
)]

story += [term_block(
    "melt",
    "Unpivots a wide DataFrame into long format.",
    "<code>df.melt(id_vars='Operator', var_name='Period', "
    "value_name='Subscribers_Mn')</code> turns 96 month columns into one "
    "<i>Period</i> column."
)]

story += [term_block(
    "to_datetime",
    "Parses a string column into Python datetime objects.",
    "<code>pd.to_datetime(df['Period'], format='%b-%Y')</code> turns "
    "<i>'Jan-2008'</i> into <i>2008-01-01</i>."
)]

story += [term_block(
    "dt accessor",
    "Convenience methods on a datetime Series (e.g. <code>.dt.year</code>, "
    "<code>.dt.month_name()</code>).",
    "<code>df['Date'].dt.month_name()</code> produces 'January', 'February', "
    "…"
)]

story += [term_block(
    "groupby",
    "Splits the DataFrame into groups based on a key column so an "
    "aggregation can be applied within each group.",
    "<code>df.groupby('Operator')['Subscribers_Mn'].mean()</code> returns "
    "the average subscribers <i>per</i> operator."
)]

story += [term_block(
    "transform",
    "Applies a function per group but returns a Series aligned with the "
    "original DataFrame (same length).",
    "<code>df.groupby('Date')['Subscribers_Mn'].transform('sum')</code> "
    "gives every row the sector total of its own month — used to compute "
    "market share."
)]

story += [term_block(
    "pct_change",
    "Returns the percentage change between consecutive values.",
    "<code>df.groupby('Operator')['Subscribers_Mn'].pct_change() * 100</code>"
    " produces <b>MoM_Growth_%</b>."
)]

story += [term_block(
    "isnull / sum",
    "<code>isnull()</code> flags NaNs as True; chaining <code>.sum()</code> "
    "counts them per column.",
    "<code>df.isnull().sum()</code> → MoM_Growth_% = 6 missing values."
)]

story += [term_block(
    "duplicated",
    "Marks rows that are duplicates of previous rows.",
    "<code>df.duplicated().sum()</code> = 0 → dataset is unique."
)]

story += [term_block(
    "describe",
    "Generates count, mean, std, min, quartiles and max for numeric columns.",
    "<code>df.describe().round(2)</code> produces the statistical summary "
    "table in Task 3.3."
)]

story += [term_block(
    "select_dtypes",
    "Filters columns by their dtype.",
    "<code>df.select_dtypes(include=np.number).columns</code> returns "
    "['Year','Subscribers_Mn','MoM_Growth_%','Market_Share_%']."
)]

story += [term_block(
    "quantile",
    "Returns the value at a given percentile.",
    "<code>df['MoM_Growth_%'].quantile([0.25, 0.75])</code> returns Q1 and "
    "Q3 used in the IQR rule."
)]

story += [term_block(
    "corr",
    "Computes pairwise Pearson correlation between numeric columns.",
    "<code>df[['Subscribers_Mn','MoM_Growth_%','Market_Share_%']].corr()"
    "</code> — Subscribers vs Share = 0.88."
)]

story += [term_block(
    "agg",
    "Applies multiple aggregation functions in one call.",
    "<code>df.groupby('Operator')['Subscribers_Mn'].agg(['min','mean',"
    "'max','std'])</code> compares operators side by side."
)]

story += [term_block(
    "to_csv",
    "Writes a DataFrame to a CSV file.",
    "<code>df.to_csv('telecom_clean.csv', index=False)</code> saves the "
    "tidy dataset for re-use in the assignment notebook."
)]

story += [h2("2.3 Plotting Functions")]

story += [term_block(
    "sns.lineplot",
    "Draws one or more line plots; <code>hue</code> creates a separate line "
    "per category.",
    "Used in Task 4.1 to show subscriber growth per operator over time."
)]

story += [term_block(
    "sns.boxplot",
    "Visualises distribution via the median, quartiles, whiskers and dots "
    "for outliers.",
    "Task 4.2 — Grameenphone's box is wide (huge growth); Citycell's is "
    "narrow."
)]

story += [term_block(
    "sns.barplot",
    "Displays a numeric value per category as bars.",
    "Task 4.3 — average market share per operator."
)]

story += [term_block(
    "sns.heatmap",
    "Renders a 2-D matrix as a colour grid; ideal for correlation matrices.",
    "Task 4.4 — annotated correlation heatmap with the coolwarm palette."
)]

story += [term_block(
    "hist",
    "pandas DataFrame method that plots a histogram for each numeric column.",
    "Task 3.4 — <code>df[[...]].hist(bins=30)</code> shows distribution "
    "shape of subscribers, growth and share."
)]

story += [PageBreak()]

# ============================================== PART 3: LOGIC OF NOTEBOOK 1
story += [h1("Part 3 — Logic of <i>EDA_and_Preprocessing.ipynb</i>")]
story += [p("This notebook converts the messy spreadsheet export into a clean, "
            "analysis-ready dataset. The logic flows in 10 stages.")]

story += [h2("Step 1. Import Libraries")]
story += [code("import pandas as pd\nimport numpy as np\n"
               "import matplotlib.pyplot as plt\nimport seaborn as sns")]
story += [p("<b>Why:</b> pandas handles the table, numpy supplies numeric "
            "helpers, matplotlib + seaborn are used later for charts. "
            "<code>sns.set_style('whitegrid')</code> sets a clean default "
            "look; <code>pd.set_option('display.max_columns', 20)</code> "
            "lets us see wide tables without truncation.")]

story += [h2("Step 2. Load Raw Data")]
story += [code("raw = pd.read_csv('GP Model.xlsx - Telecom Mkt. in "
               "Bangladesh.csv', header=None)")]
story += [p("<b>Why <code>header=None</code>?</b> The source spreadsheet has "
            "no clean header row — titles, blank rows and merged cells are "
            "scattered across the top. We load everything as raw cells and "
            "extract the block we need manually.")]
story += [p("<b>Result.</b> A 78×112 grid where rows 4–10 hold operator "
            "subscriber counts and columns 2 onward hold months Jan-2008 "
            "through Dec-2015.")]

story += [h2("Step 3. Extract the Subscriber Block")]
story += [code("years   = list(range(2008, 2016))\n"
               "months  = ['Jan','Feb',...,'Dec']\n"
               "date_cols = [f'{m}-{y}' for y in years for m in months]\n\n"
               "operators = ['Grameenphone','Banglalink','Robi',\n"
               "             'Airtel','Citycell','Teletalk']\n"
               "subs = raw.iloc[4:10, 2:2+96].copy()\n"
               "subs.columns = date_cols\n"
               "subs.index   = operators\n"
               "subs = subs.apply(pd.to_numeric, errors='coerce')")]
story += [p("<b>Logic.</b> We isolate the 6 operator rows and the 96 month "
            "columns, attach meaningful labels, then coerce every value to "
            "numeric. <code>errors='coerce'</code> means any stray text "
            "becomes NaN (so a bad cell does not crash the pipeline).")]

story += [h2("Step 4. Reshape to Long (Tidy) Format")]
story += [code("df = subs.reset_index().rename(columns={'index':'Operator'})\n"
               "df = df.melt(id_vars='Operator', var_name='Period',\n"
               "             value_name='Subscribers_Mn')\n"
               "df['Date']  = pd.to_datetime(df['Period'], format='%b-%Y')\n"
               "df['Year']  = df['Date'].dt.year\n"
               "df['Month'] = df['Date'].dt.month_name()")]
story += [p("<b>Why melt?</b> Statistical and plotting tools work best when "
            "each row is one observation. Melting collapses 96 month columns "
            "into a single <i>Period</i> column, multiplying rows by 96 and "
            "producing 6×96 = 576 records.")]
story += [p("<b>Why derive Year / Month from Date?</b> So we can group by "
            "year (yearly totals) or by calendar month (seasonality) without "
            "string parsing.")]

story += [h2("Step 5. Check Missing Values")]
story += [code("df.isnull().sum()")]
story += [p("<b>Logic.</b> Confirms that the raw extraction succeeded. The "
            "interpolation guard:")]
story += [code("df['Subscribers_Mn'] = df.groupby('Operator')['Subscribers_Mn']\\\n"
               "    .transform(lambda s: s.interpolate().ffill().bfill())")]
story += [p("…is a <b>defensive</b> step: <i>if</i> any month were missing "
            "for an operator, it would be linearly interpolated using only "
            "that operator's own time series. <code>groupby('Operator')</code> "
            "is critical — interpolating across operators would invent "
            "nonsense values.")]

story += [h2("Step 6. Check Duplicates")]
story += [code("df.duplicated().sum()\n"
               "df.duplicated(subset=['Operator','Date']).sum()")]
story += [p("Both return 0. The second call is a stronger check: it asks "
            "whether the same Operator–Date pair appears more than once "
            "(which would be a logical contradiction, even if other columns "
            "happened to differ).")]

story += [h2("Step 7. Feature Engineering")]
story += [code("df['MoM_Growth_%'] = df.groupby('Operator')['Subscribers_Mn']\\\n"
               "                       .pct_change() * 100\n\n"
               "sector_total = df.groupby('Date')['Subscribers_Mn']\\\n"
               "                  .transform('sum')\n"
               "df['Market_Share_%'] = df['Subscribers_Mn'] / sector_total * 100")]
story += [p("<b>MoM growth</b> uses <code>groupby('Operator')</code> so that "
            "Airtel's first month is compared with Airtel's previous month "
            "— not with Grameenphone's last month. The result is the "
            "percentage change in subscribers from one month to the next.")]
story += [p("<b>Market share</b> uses <code>groupby('Date').transform('sum')"
            "</code> to attach each row the sector total of <i>its own "
            "month</i>, then divides. <code>transform</code> (rather than "
            "<code>sum</code>) preserves the row count so the result aligns "
            "with the original DataFrame.")]

story += [h2("Step 8. Statistical Summary")]
story += [code("df.describe()\n"
               "df.groupby('Operator')['Subscribers_Mn']\\\n"
               "  .agg(['min','mean','max','std']).round(2)")]
story += [p("<b>Logic.</b> The first call summarises every numeric column "
            "across the whole dataset; the second shows the same statistics "
            "<i>per operator</i> so we can compare market positions directly "
            "(e.g. Grameenphone's mean = 36.03M vs Citycell's mean = 1.61M).")]

story += [h2("Step 9. Outlier Detection (IQR rule)")]
story += [code("q1 = df['MoM_Growth_%'].quantile(0.25)\n"
               "q3 = df['MoM_Growth_%'].quantile(0.75)\n"
               "iqr = q3 - q1\n"
               "lower, upper = q1 - 1.5*iqr, q3 + 1.5*iqr\n"
               "outliers = df[(df['MoM_Growth_%'] &lt; lower) |\n"
               "              (df['MoM_Growth_%'] &gt; upper)]")]
story += [p("<b>Rule.</b> Any value below Q1−1.5·IQR or above Q3+1.5·IQR is "
            "flagged. For MoM growth this gives bounds [−3.07%, 5.50%] and "
            "51 outlier rows — most are early-period high-growth months and "
            "operator rebranding events (e.g. Warid → Airtel produced a "
            "−41.7% drop).")]
story += [p("<b>Important.</b> The notebook <i>identifies</i> outliers but "
            "does not delete them — telecom growth spikes are real business "
            "signals, not data errors.")]

story += [h2("Step 10. Save Cleaned Dataset")]
story += [code("df.to_csv('telecom_clean.csv', index=False)")]
story += [p("The tidy dataset (576 × 7) becomes the input for "
            "<i>Assignment.ipynb</i>. Saving it ensures the EDA work is "
            "reproducible and decoupled from the messy original file.")]

story += [PageBreak()]

# ============================================== PART 4: LOGIC OF NOTEBOOK 2
story += [h1("Part 4 — Logic of <i>Assignment.ipynb</i>")]
story += [p("This notebook answers the five assignment tasks using the "
            "cleaned dataset produced above.")]

story += [h2("Task 1 — Explain the Dataset")]
story += [p("Documents the source (GP / BTRC), the purpose, the row/column "
            "structure, and the meaning of every column. This is qualitative "
            "context that any reader should know before reading any number.")]

story += [h2("Task 2 — Identify Categorical vs Numerical")]
story += [code("num_cols = df.select_dtypes(include=np.number).columns.tolist()\n"
               "cat_cols = df.select_dtypes(include='object').columns.tolist()")]
story += [p("<b>Logic.</b> Pandas knows each column's data type. "
            "<code>select_dtypes</code> filters them: numeric columns become "
            "candidates for arithmetic and correlations, object/string "
            "columns become grouping keys.")]
story += [p("<b>Note.</b> Although <i>Year</i> is stored as int, it is "
            "conceptually <b>ordinal categorical</b> — we usually group by "
            "it, we do not average it.")]

story += [h2("Task 3 — Exploratory Data Analysis")]

story += [h3("3.1 Missing values — <code>df.isnull().sum()</code>")]
story += [p("Reveals 6 NaNs in MoM_Growth_% (the first observation per "
            "operator). This is expected and harmless — pandas drops NaNs "
            "from aggregations automatically.")]

story += [h3("3.2 Duplicates — <code>df.duplicated().sum()</code>")]
story += [p("Returns 0. No row is repeated, so counts and means are honest.")]

story += [h3("3.3 Statistical summary — <code>df.describe().round(2)</code>")]
story += [p("Reads at a glance: subscribers span 0.84M → 56.54M, mean 14.03M, "
            "std 14.11M. Mean &gt; median for Subscribers_Mn confirms the "
            "right-skew driven by Grameenphone.")]

story += [h3("3.4 Distribution — <code>df[[…]].hist(bins=30)</code>")]
story += [p("Histograms show three shapes: <b>Subscribers_Mn</b> heavily "
            "right-skewed (most observations small, a few very large); "
            "<b>MoM_Growth_%</b> roughly symmetric and centred near 1% with "
            "fat tails; <b>Market_Share_%</b> multi-modal — each operator "
            "lives near its own share band.")]

story += [h3("3.5 Correlations — <code>.corr()</code>")]
story += [p("Subscribers vs Market_Share = 0.88 (strong, expected). MoM_Growth "
            "vs Subscribers ≈ 0.01 — large operators do <i>not</i> grow at a "
            "systematically different percentage rate.")]

story += [h3("3.6 Outliers — IQR rule")]
story += [p("Identical logic to Step 9 in the preprocessing notebook; "
            "confirms 51 outliers and keeps them in the data.")]

story += [h2("Task 4 — Visualisations")]

story += [h3("4.1 Line plot — subscribers over time per operator")]
story += [code("sns.lineplot(data=df, x='Date', y='Subscribers_Mn',\n"
               "             hue='Operator')")]
story += [p("<code>hue='Operator'</code> draws one line per operator, "
            "creating six time-series in one panel. Reading: Grameenphone "
            "leads throughout; Banglalink and Robi rise sharply; Citycell "
            "and Teletalk are flat.")]

story += [h3("4.2 Boxplot — subscriber distribution per operator")]
story += [p("Reveals the <b>spread</b> of each operator's monthly counts. "
            "A tall box = wide range over time (operator grew a lot). "
            "Grameenphone's box reaches from ~17M to 56M; Citycell's is "
            "tiny.")]

story += [h3("4.3 Bar chart — average market share per operator")]
story += [code("share = df.groupby('Operator')['Market_Share_%']\\\n"
               "          .mean().sort_values(ascending=False)\n"
               "sns.barplot(x=share.index, y=share.values, palette='viridis')")]
story += [p("Sorting before plotting makes the bars descend left-to-right, "
            "which is easier to read. Grameenphone ≈ 42% average share.")]

story += [h3("4.4 Correlation heatmap")]
story += [code("sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)")]
story += [p("<code>annot=True</code> writes the values inside cells; "
            "<code>cmap='coolwarm'</code> uses red/blue diverging colours; "
            "<code>center=0</code> anchors zero to white so the sign of the "
            "correlation is obvious.")]

story += [h3("4.5 Yearly sector total — bar chart")]
story += [code("yearly = df.groupby('Year')['Subscribers_Mn'].sum()\n"
               "sns.barplot(x=yearly.index, y=yearly.values)")]
story += [p("Summing within each year aggregates monthly data into one bar "
            "per year. The bars almost triple from 2008 to 2015 — the "
            "headline market growth story.")]

story += [h2("Task 5 — Insights")]
story += [p("The final markdown cell turns numbers into a story:")]
for bullet in [
    "<b>Leadership.</b> Grameenphone leads continuously and grew from ~17M "
    "to ~56M.",
    "<b>Challengers.</b> Banglalink and Robi rose steadily into clear #2 "
    "and #3 positions.",
    "<b>Decline.</b> Citycell shrank; Teletalk grew slowly.",
    "<b>Oligopoly.</b> Top-3 operators control roughly 90% of the market.",
    "<b>Growth signal.</b> Sector subscribers almost tripled in 8 years — "
    "consistent with rising mobile penetration in Bangladesh.",
]:
    story += [Paragraph(f"• {bullet}", BULLET)]

story += [PageBreak()]

# =========================================================== APPENDIX
story += [h1("Appendix — Quick Reference Cheat Sheet")]

ref = [
    ["Symbol / Term", "Meaning in one line"],
    ["NaN", "Not-a-Number; pandas' missing-value marker."],
    ["DataFrame", "A 2-D table (rows × columns) — the central pandas object."],
    ["Series", "A single column of a DataFrame."],
    ["dtype", "The data type of a column (int, float, object, datetime, …)."],
    ["IQR rule", "Outlier if value < Q1−1.5·IQR or > Q3+1.5·IQR."],
    ["Pearson corr", "Linear correlation; values in [-1, 1]."],
    ["hue=", "Seaborn parameter that splits a plot by a categorical column."],
    ["groupby", "Split-apply-combine on a key column."],
    ["transform", "Like groupby+apply but returns row-aligned output."],
    ["pct_change", "Element-wise percentage change vs previous row."],
    ["melt", "Wide → long reshape."],
    ["select_dtypes", "Pick columns by dtype family."],
    ["describe", "Five-number summary + count, mean, std."],
    ["MoM growth", "(Vt − V(t−1)) / V(t−1) × 100."],
    ["Market share", "Operator subscribers ÷ sector total × 100."],
]
ref_table = Table(ref, colWidths=[4.6 * cm, 11.4 * cm])
ref_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#0B3D91')),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#FFFFFF')),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9.5),
    ('GRID', (0, 0), (-1, -1), 0.4, HexColor('#777777')),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1),
     [HexColor('#FFFFFF'), HexColor('#F1F4FA')]),
]))
story += [ref_table]

# Build
doc = SimpleDocTemplate(
    OUT, pagesize=A4,
    leftMargin=2 * cm, rightMargin=2 * cm,
    topMargin=2 * cm, bottomMargin=2 * cm,
    title="Assignment Explanation",
    author="Generated by Claude Code"
)
doc.build(story)
print("Wrote:", OUT)
