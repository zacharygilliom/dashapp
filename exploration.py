import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt 

from pandas.api.types import is_numeric_dtype

def summary(df):
	print(df.describe())
	print(list(df.columns))
	print(df.shape)
	print(df.isna().sum())
	print(df.count())
	print(df.dtypes)
	print('Percent of values that are NA in each column')
	print(((df.isna().sum()) / (df.count())) * 100)
	print(df['neighbourhood_group'].unique())

def histplots(df):
	df.dropna(axis=0, inplace=True)
	print(df.isna().sum())
	d = [i for i in df.columns if is_numeric_dtype(df[i])]
	a = list(range(1,len(d) + 1))
	b = d
	for i, j in zip(a, b):
		plt.subplot(len(b),1,i)
		sns.kdeplot(df[j])
	plt.savefig('image.png')

def scatterplots(df):
	df = df[df['price'] < 1250]
	x_axis = df['price']
	y_axis = df['number_of_reviews']
	sns.scatterplot(x=x_axis, y=y_axis, hue=df['neighbourhood_group'])
	plt.savefig('imagescatter.png')


df = pd.read_csv('AB_NYC_2019.csv')



# print(df.head())

summary(df)
print(df['last_review'])
print(df['reviews_per_month'])

# histplots(df)

scatterplots(df)

