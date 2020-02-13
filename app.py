import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np

# print(df.head())
def get_summary(df):
	print(df.describe())
	print(df.isna().sum())
	print(df.shape)
	print(list(df.columns))
	return df

df = pd.read_csv('AB_NYC_2019.csv')

get_summary(df)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']},
	children=[
	html.H1(
		children='NYC AirBnBs in 2019 Analysis',
		style={'color': colors['text'], 'textAlign': 'center'}),
	html.H2(
		children='Neighborhood Analysis',
		style={'color': colors['text'], 'textAlign': 'center'}),
	html.Div(
		style={'backgroundColor': colors['background']},
		children=[
		html.Div(
			children=[
			dcc.Graph(
				id='Neighborhood vs Price'
			),
			dcc.Dropdown(
				id='Neighbourhoods',
				options=[
					{'label': i, 'value': i} for i in df.neighbourhood_group.unique()
				],
				value=df.neighbourhood_group.unique()
			),	
			html.H1('Empty Frame')
			]
	)]
)
]
)

@app.callback(
	Output('Neighborhood vs Price', 'figure'),
	[Input('Neighbourhoods', 'value')])
def update_neighborhood(selected_n):
	sliced_df = df[df['neighbourhood_group'] == selected_n]

	return {
		'data': [
		{'x': sliced_df['neighbourhood'], 'y': sliced_df['price'], 'type': 'bar'}
		],
		
		'layout': {
			'title': 'Neighbourhoods vs Prices'
		}
	}


if __name__ == '__main__':
	app.run_server(debug=True)
