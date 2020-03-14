import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import dash_table as dt 
# import plotly_express as px
import plotly.graph_objects as go

# print(df.head())
def get_summary(df):
	print(df.describe())
	print(df.isna().sum())
	print(df.shape)
	print(list(df.columns))
	return df

def slice_dataframe_by_neighbourhood_group(df, i):
	df = df[df['neighbourhood_group'] == i]
	return df

df = pd.read_csv('AB_NYC_2019.csv')
# Quick summary of our dataset
get_summary(df)

# Creating our neighbourhood group slices first so that they don't have to be created everytime we select data in our app
df_manhattan = slice_dataframe_by_neighbourhood_group(df, 'Manhattan')
df_brooklyn = slice_dataframe_by_neighbourhood_group(df, 'Brooklyn')
df_statenIsland = slice_dataframe_by_neighbourhood_group(df, 'Staten Island')
df_queens = slice_dataframe_by_neighbourhood_group(df, 'Queens')
df_bronx = slice_dataframe_by_neighbourhood_group(df, 'Bronx')

# adding the neighbourhoods to a dictionary so we can easily access them by using the neighbourhood group name.
neighbourhood_groups = {'Manhattan':df_manhattan, 'Bronx':df_bronx, 'Brooklyn':df_brooklyn, 'Staten Island':df_statenIsland, 'Queens': df_queens}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# Setting our colors to a dark theme and a light blue text


colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']},
	children=[
		# Our main title on our page
		html.H1(
			children='NYC AirBnBs in 2019 Analysis',
			style={'color': colors['text'], 'textAlign': 'center'}),
		# Subheader and description of what we are analyzing on this page.
		html.H2(
			children='Neighborhood Analysis',
			style={'color': colors['text'], 'textAlign': 'center'}),
		# This is where we will create our graph, data table, and input value
		html.Div(
			style={'backgroundColor': colors['background']},
			children=[
				html.Div(
					children=[
						dcc.Graph(
							id='Neighbourhood vs Price'
						),
						# List of availabel neighbourhood groups to slice our data.
						dcc.Markdown('''
							Available Neighbourhood Groups to Select
							* Brooklyn
							* Queens
							* Staten Island
							* Manhattan
							* Bronx
						''',
						style={'backgroundColor': colors['background'], 'color': colors['text']}
						),
						html.Datalist(
							id='n_list', 
							children=[
								html.Option(value='Manhattan'),
								html.Option(value='Brooklyn'),
								html.Option(value='Queens'),
								html.Option(value='Bronx'),
								html.Option(value='Staten Island')
								],
							style={'backgroundColor': colors['background'], 'color': colors['text']}
						),
						# Our main Input that will control all of our visuals.
						dcc.Input(
							id='Neighbourhoods',
							type= 'text',
							required='required',
							autoComplete='on',
							value='Bronx',
							# placeholder='',
							debounce=True,
							list='n_list',
							style={	
								'backgroundColor': colors['background'], 'color': colors['text']
								}							
						)
					],
							style={'textAlign': 'center', 'plot_bgcolor':colors['background']}
				),
			]
		),
		html.Div(
			children=[
				dt.DataTable(
					# this is our datatable
					id='table',
					columns=[{'name': i, 'id': i} for i in df[['host_name','neighbourhood','neighbourhood_group','price']].columns],
					sort_mode='single',
					filter_query='',
					page_size=10,
					style_header={
						'backgroundColor': colors['background'],
						'color': colors['text']
					},
					style_cell={
						'backgroundColor': 'rgb(50, 50, 50)',
						'color': colors['text']
					}
					# 'layout': {
					# 	'title': 'Neighbourhoods vs Prices',
					# 	'plot_bgcolor': colors['background'],
					# 	'paper_bgcolor': colors['background'],
					# 	'font': {
					# 		'color': colors['text']
					# 	}

				),
				# this is our scatter plot
				dcc.Graph(
					id='scatter_reviews'
				)
			]
		)
	]	
)

@app.callback(
	Output('Neighbourhood vs Price', 'figure'),
	[Input('Neighbourhoods', 'value')])
def update_neighborhood(selected_n):
	sliced_df = neighbourhood_groups[selected_n]
	traces = []
	traces.append(dict(
		x = sliced_df['neighbourhood'],
		y = sliced_df['price'],
		type = 'bar',
		# template='plotly_dark',
		))
	return {
		'data': traces,		
		'layout': {
			'title': 'Neighbourhoods vs Prices',
			# 'template': 'plotly_dark'
			'plot_bgcolor': colors['background'],
			'paper_bgcolor': colors['background'],
			'yaxis': {
				'gridwith': 3,
				'gridcolor': 'rgb(120, 120, 120)',
			},
			'xaxis': {
				'gridwidth': 2,
				'showgrid': False
			},
			'font': {
				'color': colors['text']
			}
		}
	}


@app.callback(
	Output('table', 'data'),
	[Input('Neighbourhoods', 'value')])
def update_table(selected_n):
	# Slice data on our neighbourhood group and also by out top ten largest vales by price
	sliced_df = neighbourhood_groups[selected_n]
	sliced_df = sliced_df[sliced_df['price'] > 150].nlargest(10, 'price')
	data = sliced_df.to_dict("rows")
	return 	data
	

@app.callback(
	Output('scatter_reviews', 'figure'),
	[Input('Neighbourhoods', 'value')])
def update_scatter(selected_n):
	sliced_df = neighbourhood_groups[selected_n]
	sliced_df = sliced_df[sliced_df['price'] < 600]

	return {
		'data': [
		{'x': sliced_df['price'], 'y': sliced_df['number_of_reviews'], 'type': 'scatter', 'mode': 'markers'
		}],		
		'layout': {
			'title': 'Prices vs number of reviews',
			'plot_bgcolor': colors['background'],
			'paper_bgcolor': colors['background'],
			'yaxis': {
				'gridwidth': 1.0,
				'gridcolor': 'rgb(120, 120, 120)'
			},
			'xaxis': {
				'gridwidth': 1.0,
				'gridcolor': 'rgb(120, 120, 120)'
			},
			'font': {
				'color': colors['text']
			}

		}
	}

if __name__ == '__main__':
	app.run_server(debug=True)
