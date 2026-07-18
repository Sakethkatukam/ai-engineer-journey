import pandas as pd
import numpy as np

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

print(df.shape)
print(df.dtypes)
print(df.isnull().sum())

print(f"Median Age: {df['Age'].median()}")
print(f"Mode Embarked: {df['Embarked'].mode()[0]}")
# Pattern 1: reassignment
df['Age'] = df['Age'].fillna(df['Age'].median())
df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])
# Pattern 2: df.fillna() with dict (modern recommended style)
# df.fillna({'Age': df['Age'].median(), 'Embarked': df['Embarked'].mode()[0]}, inplace=True)

df.drop(columns=['Cabin'],inplace=True)

print("\nNull counts after cleaning:")
print(df.isnull().sum())
print(f"\nShape after cleaning: {df.shape}")

# Feature 1: Extract title from Name column
# Name format is: "Braund, Mr. Owen Harris" — title sits between ", " and "."
df['Title']=df['Name'].str.extract(r',\s*([^\.]+)\.')
print("Unique titles found:")
print(df['Title'].value_counts())

# --- Now clean rare titles into 4 groups ---
title_mapping = {
    'Mr': 'Mr',
    'Mrs': 'Mrs',
    'Miss': 'Miss',
    'Master': 'Master',
    'Dr': 'Rare',
    'Rev': 'Rare',
    'Major': 'Rare',
    'Mlle': 'Miss',    # French for Mademoiselle = Miss
    'Col': 'Rare',
    'Don': 'Rare',
    'Mme': 'Mrs',      # French for Madame = Mrs
    'Ms': 'Miss',
    'Lady': 'Rare',
    'Sir': 'Rare',
    'Capt': 'Rare',
    'the Countess': 'Rare',
    'Jonkheer': 'Rare'
}
df['Title']=df['Title'].map(title_mapping)
print("Titles after grouping:")
print(df['Title'].value_counts())

# --- Feature 2: Family Size ---
# SibSp = number of siblings/spouses aboard
# Parch = number of parents/children aboard
# +1 to include the passenger themselves
df['FamilySize']=df['SibSp']+df['Parch']+1
# Bonus: IsAlone flag — useful for ML models
df['IsAlone']=(df['FamilySize']==1).astype(int)
print("\nFamily size distribution:")
print(df['FamilySize'].value_counts().sort_index())
print(f"\nTravelling alone: {df['IsAlone'].sum()} passengers")

# --- GroupBy Analysis ---

# 1. Survival rate by Passenger Class
print("\nSurvival rate by Pclass:")
print(df.groupby('Pclass')['Survived'].mean().round(3))

# 2. Survival rate by Sex
print("\nSurvival rate by Sex:")
print(df.groupby('Sex')['Survived'].mean().round(3))

# 3. Survival rate by Title
print("\nSurvival rate by Title:")
print(df.groupby('Title')['Survived'].mean().round(3))

# 4. Average age by Pclass and Sex combined
print("\nAverage age by Pclass and Sex:")
print(df.groupby(['Pclass','Sex'])['Age'].mean().round(1))

# 5. Multiple aggregations — fare stats by Pclass
print("\nFare stats by Pclass:")
print(df.groupby('Pclass')['Fare'].agg(
    mean_fare='mean',
    median_fare='median',
    max_fare='max'
).round(2))

# 6. Family size vs survival
print("\nSurvival rate by FamilySize:")
print(df.groupby('FamilySize')['Survived'].mean().round(3))

import sqlite3
conn=sqlite3.connect(':memory:')
df.to_sql('titanic',conn,index=False,if_exists='replace')

def run_query(description,query):
    print(f"\n{description}")
    print('-'*40)
    result=pd.read_sql_query(query,conn)
    print(result)

# SQL 1: Survival rate by Pclass
# Pandas equivalent: df.groupby('Pclass')['Survived'].mean()
run_query(
    "1. Survival rate by class",
    """
    SELECT Pclass,
        ROUND(AVG(Survived),3) AS survival_rate
    FROM titanic
    GROUP BY Pclass
    ORDER BY Pclass
    """
)

# SQL 2: Survival rate by Sex
# Pandas equivalent: df.groupby('Sex')['Survived'].mean()
run_query(
    "2. Survival rate by sex",
    """
    SELECT Sex,
        ROUND(AVG(Survived),3) AS survival_rate
    FROM titanic
    GROUP BY Sex
    """
)

# SQL 3: Average age by Pclass and Sex
# Pandas equivalent: df.groupby(['Pclass','Sex'])['Age'].mean()
run_query(
    "3. Average age by Pclass and Sex",
    """
    SELECT Pclass, Sex,
        ROUND(AVG(Age),1) AS avg_age
    FROM titanic
    GROUP BY Pclass,Sex
    ORDER BY Pclass,Sex
    """
)

# SQL 4: Fare stats by Pclass
# Pandas equivalent: df.groupby('Pclass')['Fare'].agg(...)
run_query(
    "4. Fare stats by Pclass",
    """
    SELECT Pclass,
        ROUND(AVG(Fare),2) AS mean_fare,
        ROUND(MAX(Fare),2) AS max_fare,
        COUNT(*) AS passenger_count
    FROM titanic
    GROUP BY Pclass
    ORDER BY Pclass
    """
)

# SQL 5: Survival rate by FamilySize
# Pandas equivalent: df.groupby('FamilySize')['Survived'].mean()
run_query(
    "5. Survival rate by FamilySize",
    """
    SELECT FamilySize,
        COUNT(*) AS count,
        ROUND(AVG(Survived),3) AS survival_rate
    FROM titanic
    GROUP BY FamilySize
    ORDER BY FamilySize
    """
)
conn.close()