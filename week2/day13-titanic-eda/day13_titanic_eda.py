import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

fig,ax= plt.subplots(2,3,figsize=(15,8))  # plt.subplots(rows,cols)

#1. Bar chart — comparing categories
survival_by_class=df.groupby('Pclass')['Survived'].mean()
ax[0,0].bar(survival_by_class.index, survival_by_class.values)
ax[0,0].set_xlabel("Passenger Class")
ax[0,0].set_ylabel("Survival Rate")
ax[0,0].set_title("Survival Rate by Class")

#2. Histogram — distribution of a single numeric column
ax[0,1].hist(df['Age'].dropna(),bins=20,edgecolor='black')
ax[0,1].set_xlabel("Age")
ax[0,1].set_ylabel("Count")
ax[0,1].set_title("Age Distribution")

#3. Scatter plot — relationship between two numeric variables
ax[0,2].scatter(df['Age'],df['Fare'],alpha=0.5)
ax[0,2].set_ylabel("Fare")
ax[0,2].set_title("Age vs Fare")
ax[0,2].set_xlabel("Age")

#4. Correlation heatmap
numeric_df=df.select_dtypes(include='number')
corr=numeric_df.corr()
sns.heatmap(corr,annot=True,cmap='coolwarm',center=0,ax=ax[1,0])
ax[1,0].set_title("Correlation Heatmap")


df['Title'] = df['Name'].str.extract(r' ([A-Za-z]+)\.', expand=False)
df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
df['IsAlone'] = (df['FamilySize'] == 1).astype(int)

# print(df['Title'].value_counts())

rare_titles = ['Dr', 'Rev', 'Major', 'Mlle', 'Col', 'Don', 'Mme', 
               'Ms', 'Lady', 'Sir', 'Capt', 'Countess', 'Jonkheer']
df['Title']=df['Title'].replace(rare_titles,'Rare')
# print(df['Title'].value_counts())
 
#5. Survival by sex
survival_by_sex=df.groupby('Sex')['Survived'].mean()
ax[1,1].bar(survival_by_sex.index,survival_by_sex.values)
ax[1,1].set_xlabel('Sex')
ax[1,1].set_ylabel('Survival Rate')
ax[1,1].set_title('Survival Rate by Sex')

#6. Survival by title 
survival_by_title=df.groupby('Title')['Survived'].mean().sort_values(ascending=False)
ax[1,2].bar(survival_by_title.index,survival_by_title.values)
ax[1,2].set_xlabel('Title')
ax[1,2].set_ylabel('Survival Rate')
ax[1,2].set_title('Survival Rate by Title')

print(survival_by_class)
print(survival_by_sex)
print(survival_by_title)

plt.tight_layout()
plt.savefig('titanic_eda.png')
plt.show()