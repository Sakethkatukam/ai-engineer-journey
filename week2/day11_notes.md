## Day 11 — Advanced Pandas: GroupBy, Merge, Apply, Pipelines

---

### 1. Display Options
pd.set_option('display.max_columns', 85)
pd.set_option('display.max_rows', 85)
# Use these at the top of every notebook to avoid truncated output

---

### 2. Loading Data
df = pd.read_csv('data.csv')
df = pd.read_csv('data.csv', index_col='column_name')  # set index on load

---

### 3. Basic Inspection
df.shape          # (rows, columns)
df.dtypes         # data type of each column
df.info()         # dtypes + non-null counts together
df.describe()     # stats summary: count, mean, std, min, max, quartiles
df.head()         # first 5 rows
df.tail()         # last 5 rows
df.columns        # list of column names
df['col'].value_counts()   # count of each unique value in a column

---

### 4. Indexing — iloc vs loc

# iloc: integer position based (0-indexed, end is EXCLUSIVE)
df.iloc[0]              # first row
df.iloc[[0, 1, 2]]      # rows 0,1,2
df.iloc[[0, 1], [0, 1]] # rows 0,1 and columns 0,1

# loc: label based (end is INCLUSIVE)
df.loc[0:2, 'col']              # rows 0,1,2 of one column
df.loc[0:2, 'col1':'col4']      # rows 0,1,2 of col1 through col4
df.loc[[0,1,2], 'col']          # same as above, explicit list

# Key difference:
# iloc[0:2] gives rows 0,1 (exclusive end — standard Python)
# loc[0:2]  gives rows 0,1,2 (inclusive end — label based)

---

### 5. Setting and Resetting Index
df.set_index('column')                    # temporary
df.set_index('column', inplace=True)      # permanent
df.reset_index(inplace=True)              # push index back to column

---

### 6. Sorting
df.sort_index()                           # sort by index ascending
df.sort_index(ascending=False)            # sort by index descending
df.sort_values(by='column')               # sort by column value ascending
df.sort_values(by='column', ascending=False)    # descending
df.sort_values(by=['col1', 'col2'])       # sort by multiple columns

---

### 7. Filtering — Conditionals
# Single condition
df[df['col'] > 50]
df[df['col'] == 'value']

# Multiple conditions — use & (and) | (or), ALWAYS wrap each in ()
df[(df['col1'] > 50) & (df['col2'] == 'value')]
df[(df['col1'] > 50) | (df['col2'] == 'value')]

# Filter using isin() — match against a list of values
df[df['col'].isin(['val1', 'val2'])]

# Negation — ~ means NOT
df[~df['col'].isin(['val1', 'val2'])]

# String methods for filtering
df[df['col'].str.contains('pattern')]     # contains substring
df[df['col'].str.contains('pat', na=False)]  # na=False avoids NaN errors

---

### 8. Adding and Removing Columns
df['new_col'] = df['col1'] + df['col2']   # add column
df.drop(columns=['col1', 'col2'], inplace=True)   # remove columns
df.drop(index=[0, 1], inplace=True)               # remove rows by index

---

### 9. Handling Missing Values (NaN)
df.isnull()               # True/False mask of nulls
df.isnull().sum()         # count of nulls per column
df.dropna()               # drop ALL rows with any null
df.dropna(axis='columns') # drop columns with any null
df.dropna(subset=['col']) # drop rows where specific column is null

df.fillna('value')              # fill all nulls with a value
df['col'].fillna(df['col'].mean(), inplace=True)  # fill with column mean
# Common strategy: fill numeric nulls with median, categorical with mode

---

### 10. Data Types
df.dtypes                         # show all column types
df['col'].astype(int)             # convert type
df['col'].astype(float)
df['col'].astype(str)

# Casting on load
df = pd.read_csv('data.csv', dtype={'col': int})

---

### 11. GroupBy
# Split → Apply → Combine pattern
df.groupby('col')['target'].mean()     # mean of target per group
df.groupby('col')['target'].sum()
df.groupby('col')['target'].count()
df.groupby('col')['target'].max()
df.groupby('col')['target'].min()

# Multiple aggregations at once
df.groupby('col').agg({'col1': 'mean', 'col2': 'sum'})

# Group by multiple columns
df.groupby(['col1', 'col2'])['target'].mean()

# Named aggregations (cleaner output)
df.groupby('col').agg(
    avg_val=('target', 'mean'),
    total=('target', 'sum'),
    count=('target', 'count')
)

---

### 12. Merge (SQL-style JOINs in Pandas)
# Inner join — only rows where key exists in BOTH
pd.merge(df1, df2, on='key_col', how='inner')

# Left join — all rows from df1, matched rows from df2
pd.merge(df1, df2, on='key_col', how='left')

# Right join — all rows from df2, matched rows from df1
pd.merge(df1, df2, on='key_col', how='right')

# Outer join — all rows from both, NaN where no match
pd.merge(df1, df2, on='key_col', how='outer')

# Merge on different column names
pd.merge(df1, df2, left_on='col_df1', right_on='col_df2', how='inner')

---

### 13. Apply — Custom Functions on Columns/Rows
# Apply a function to every value in a column
df['new_col'] = df['col'].apply(lambda x: x * 2)

# Apply a named function
def clean_name(name):
    return name.strip().lower()
df['col'] = df['col'].apply(clean_name)

# Apply across rows (axis=1 means row-wise)
df['new_col'] = df.apply(lambda row: row['col1'] + row['col2'], axis=1)

# apply vs map vs applymap
# .apply()    → works on Series or DataFrame (most flexible)
# .map()      → works on a Series only, element-wise
# .applymap() → works on entire DataFrame element-wise (renamed to .map() in Pandas 2.x)

---

### 14. Pipelines (Method Chaining)
# Chain multiple operations cleanly instead of creating temp variables
result = (df
    .dropna(subset=['col1'])
    .rename(columns={'old_name': 'new_name'})
    .assign(new_col=lambda x: x['col1'] * 2)
    .groupby('col2')['new_col']
    .mean()
    .reset_index()
)
# Use parentheses around the whole chain to allow line breaks

---

### Key Patterns to Remember
- Always use na=False inside .str.contains() to avoid NaN errors
- Use & and | for multi-condition filters, never 'and'/'or'
- iloc end is EXCLUSIVE, loc end is INCLUSIVE — this trips everyone up
- groupby alone does nothing — always chain .mean()/.sum()/.agg() after it
- Method chaining with () wrapper = clean, readable pipeline code

## SUMMARY

### Key Concepts

**Copy-on-Write (Pandas 2.x) — Critical:**
- NEVER use df['col'].method(inplace=True) — creates a copy, 
  original df unchanged, raises ChainedAssignmentError
- ALWAYS use: df['col'] = df['col'].method()
- Or: df.fillna({'col': value}, inplace=True) — dict style is safe

**Null Handling Strategy:**
- Numeric columns → fill with median (robust to outliers)
- Categorical columns → fill with mode (most frequent value)
- >70% null → drop the column entirely (e.g. Cabin: 77% null)
- df['col'] = df['col'].fillna(value)  ← correct Pandas 2.x pattern

**Feature Engineering:**
- Extract title from name using regex:
  df['Title'] = df['Name'].str.extract(r',\s*([^\.]+)\.')
  - ,     → literal comma
  - \s*   → zero or more whitespace
  - ([^\.]+) → capture group: one or more chars that are NOT a dot
  - \.    → literal dot
- Map rare titles to groups using dict + .map()
- FamilySize = SibSp + Parch + 1  (always +1 for the passenger)
- IsAlone = (FamilySize == 1).astype(int)

**GroupBy Pattern:**
- df.groupby('col')['target'].mean()   ← single group, single agg
- df.groupby(['col1','col2'])['target'].mean()  ← multi-column group
- df.groupby('col').agg(                ← named multi-aggregation
      mean_fare=('Fare', 'mean'),
      max_fare=('Fare', 'max')
  )
- groupby alone does nothing — always chain aggregation after it

**SQL ↔ Pandas Bridge:**
- GROUP BY     = .groupby()
- AVG()        = .mean()
- COUNT(*)     = .count()
- ORDER BY     = .sort_values()
- WHERE        = df[df['col'] condition]
- JOIN         = pd.merge()

**SQLite in Python:**
- conn = sqlite3.connect(':memory:')   ← in-memory DB, no file needed
- df.to_sql('table_name', conn, index=False, if_exists='replace')
- pd.read_sql_query("SELECT ...", conn)
- Always conn.close() when done

### Titanic EDA Insights
- Class 1 survival 63% vs Class 3 only 24% — deck proximity to lifeboats
- Female survival 74.2% vs male 18.9% — "women and children first" policy
- Mrs title had highest survival at 79.4%
- FamilySize 4 had highest survival (72.4%) — small families coordinated best
- FamilySize 8 and 11 had 0% survival — large families couldn't evacuate
- 537/891 passengers (60%) travelled alone

### Regex Pattern Worth Remembering
r',\s*([^\.]+)\.'
- r prefix = raw string in Python (backslashes not interpreted by Python)
- Use str.extract() for regex capture groups on Pandas Series
- () in regex = capture group = what actually gets extracted

### Code Patterns Worth Remembering
# Load dataframe into SQLite
conn = sqlite3.connect(':memory:')
df.to_sql('titanic', conn, index=False, if_exists='replace')
result = pd.read_sql_query("SELECT ...", conn)
conn.close()

# Feature engineering
df['Title'] = df['Name'].str.extract(r',\s*([^\.]+)\.')
df['Title'] = df['Title'].map(title_mapping)
df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
df['IsAlone'] = (df['FamilySize'] == 1).astype(int)

### Resources Used
- Kaggle Learn Pandas — Chapters 5-6 (Grouping, Data Types, Missing Values)
- Corey Schafer Pandas Series — Videos 1-6
- Titanic dataset from datasciencedojo GitHub

### Open Questions
- None