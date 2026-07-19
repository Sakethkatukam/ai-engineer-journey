import matplotlib.pyplot as plt
import pandas as pd

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

fig,ax= plt.subplots()  # fig = canvas, ax = the plot itself

#1. Line chart — trends over a continuous variable
ax.plot(df['Age'].sort_values().values)
ax.set_title("Age sorted")

#2. Bar chart — comparing categories
fig,ax= plt.subplots()
survival_by_class=df.groupby('Pclass')['Survived'].mean()
ax.bar(survival_by_class.index, survival_by_class.values)
ax.set_xlabel("Passenger Class")
ax.set_ylabel("Survival Rate")
ax.set_title("Survival Rate by Class")

#3. Histogram — distribution of a single numeric column
fig,ax= plt.subplots()
ax.hist(df['Age'].dropna(),bins=20,edgecolor='black')
ax.set_xlabel("Age")
ax.set_ylabel("Count")
ax.set_title("Age Distribution")

#4. Scatter plot — relationship between two numeric variables
fig,ax= plt.subplots()
ax.scatter(df['Age'],df['Fare'],alpha=0.5)
ax.set_xlabel("Age")
ax.set_ylabel("Fare")
ax.set_title("Age vs Fare")

import seaborn as sns

#5. Correlation heatmap
numeric_df=df.select_dtypes(include='number')
corr=numeric_df.corr()

fig,ax=plt.subplots(figsize=(8,6))
sns.heatmap(corr,annot=True,cmap='coolwarm',center=0,ax=ax)
ax.set_title("Correlation Heatmap")

plt.show()