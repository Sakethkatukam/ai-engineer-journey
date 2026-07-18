## Day 12 — Data Visualization + SQL Foundations

## Key concepts learned:

- Matplotlib OO API: fig, ax = plt.subplots() as default pattern over plt.plot() directly
- Bar chart (categories), histogram (single-column distribution), scatter (two-variable relationship)
- Seaborn sns.heatmap() requires a correlation matrix (.corr()) first, not raw data
- Debugged a stale-ax issue causing a bar chart to render incorrectly — fixed by ensuring a fresh fig, ax = plt.subplots() per plot
- SQL JOINs: INNER vs LEFT vs RIGHT; SQLite has no native RIGHT JOIN (flip table order + LEFT JOIN instead)
- Reinforced via LeetCode SQL: self-joins, LEFT JOIN + IS NULL for "missing" pattern, HAVING for aggregate filters, subqueries in DELETE

### Code patterns worth remembering:

## matplotlib
fig, ax = plt.subplots(figsize=(8,6))
sns.heatmap(df.select_dtypes(include='number').corr(), annot=True, cmap='coolwarm', center=0, ax=ax)

## sql
-- "missing" pattern
LEFT JOIN ... WHERE right_table.key IS NULL

-- self-join pattern
FROM Employee e JOIN Employee m ON e.managerId = m.id