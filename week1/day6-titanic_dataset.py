import pandas as pd

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# Q1 - Shape
print("Q1 - Shape:", df.shape)

# Q2 - First 8 rows
print("\nQ2 - First 8 rows:")
print(df.head(8))

# Q3 - Missing values
print("\nQ3 - Missing values:")
print(df.isnull().sum())

# Q4 - Average age
print("\nQ4 - Average age:", df['Age'].mean())

# Q5 - Survivors count
print("\nQ5 - Survivors:", (df['Survived'] == 1).sum()) #df['Survived'].value_counts().get(1)

# Q6 - Select 3 columns
print("\nQ6 - Name, Age, Survived:")
print(df[['Name', 'Age', 'Survived']].head())

# Q7 - Passengers older than 60
print("\nQ7 - Passengers over 60:")
print(df[df['Age'] > 60])

# Q8 - Survival rate by class
print("\nQ8 - Survival rate by Pclass:")
print(df.groupby('Pclass')['Survived'].mean())

# Q9 - Oldest 5 passengers
print("\nQ9 - Top 5 oldest:")
print(df.sort_values('Age', ascending=False).head())

# Q10 - Gender counts
print("\nQ10 - Gender counts:")
print(df['Sex'].value_counts())