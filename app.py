import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import os
import pandas as pd
import quandl

app = dash.Dash()
server = app.server
app.title = 'Crypto Pairing'

# Default conversion from ETH to BTC
default_inputs = ('ETH', 'BTC')

# Declare constant variables
convert_from = ['BTC', 'ETH', 'LTC']
convert_to = ['EUR', 'USD', 'GBP', 'CAD', 'BTC']
allowed_pairs = {('ETH', 'USD'): 'ETH_USD', ('ETH', 'EUR'): 'ETH_EUR', ('ETH', 'BTC'): 'ETH_BTC',
					('BTC', 'USD'): 'USD', ('BTC', 'EUR'): 'EUR', ('BTC', 'GBP'): 'GBP', ('BTC', 'CAD'): 'CAD',
					('LTC', 'EUR'): 'LTC_EUR', ('LTC', 'BTC'): 'LTC_BTC', ('LTC', 'USD'): 'LTC_USD'}

# Setup Layout of app
app.layout = html.Div([
	html.Div([
		dcc.Dropdown(
			id='cur-1',
			options=[{'label': i, 'value': i} for i in convert_from],
			value=default_inputs[0]
		)
	], style={'width': '48%', 'display': 'inline-block'}),

	html.Div([
		dcc.Dropdown(
			id='cur-2',
			options=[{'label': i, 'value': i} for i in convert_to],
			value=default_inputs[1]
		)
	], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

	html.H1(id='title',
		children=default_inputs[0] + ' to ' + default_inputs[1],
		style={'textAlign': 'center', 'margin-bottom': '0'}),
	html.Div(id='main-plot')
], className="container")

# Update Title when dropdown options are selected
@app.callback(
	Output(component_id='title', component_property='children'),
	[Input(component_id='cur-1', component_property='value'),
	 Input(component_id='cur-2', component_property='value')])
# Function that updates the title based on selected conversion
def update_title(cur_1, cur_2):
	# Determine if both currencies are valid
	if (cur_1, cur_2) not in allowed_pairs and (cur_2, cur_1) not in allowed_pairs:
		cur_1, cur_2 = default_inputs[0], default_inputs[1]

	return cur_1 + ' to ' + cur_2

# Update main graph when dropdown options are selected
@app.callback(
	Output(component_id='main-plot', component_property='children'),
	[Input(component_id='cur-1', component_property='value'),
	 Input(component_id='cur-2', component_property='value')])
# Function that updates the graph based on selected conversions
def update_graph(cur_1, cur_2):
	# Determine code for api call
	code = ""
	if (cur_1, cur_2) in allowed_pairs:
		code = allowed_pairs[(cur_1, cur_2)]
	elif (cur_2, cur_1) in allowed_pairs:
		code = allowed_pairs[(cur_2, cur_1)]
	else:
		code = allowed_pairs[default_inputs]

	print("GDAX/" + code)

	# Determine y-axis label name
	ylabel = "Dollars in " + cur_2
	if cur_2 == 'BTC':
		ylabel = "Ratio"

	df_temp = quandl.get("GDAX/" + code, authtoken=os.environ['API_TOKEN'])
	return dcc.Graph(
		id='graph',
		figure={
		'data': [go.Scatter(
			x=df_temp.index,
			y=df_temp['Open'],
			mode='lines'
		)],
		'layout': go.Layout(
			xaxis={
				'title': 'Time',
			},
			yaxis={
				'title': ylabel,
			},
		)
	})

external_css = ["https://codepen.io/chriddyp/pen/bWLwgP.css",
	"https://s3.amazonaws.com/static-files-dpang/stylesheet.css"]

for css in external_css:
	app.css.append_css({"external_url": css})

if __name__ == '__main__':
	app.run_server(debug=True)
