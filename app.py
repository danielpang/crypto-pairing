import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

import pandas as pd
import quandl

app = dash.Dash()
app.title = 'Crypto Pairing'

default_inputs = ('ETH', 'BTC')
df = quandl.get("GDAX/ETH_BTC", authtoken="ZHJDdS31ZueeYzkeFDsb")
convert_from = ['BTC', 'ETH', 'LTC']
convert_to = ['EUR', 'USD', 'GBP', 'CAD', 'BTC']
#currencies = {'BTC': 'Bitcoin', 'ETH': 'Ethereum', 'LTC': 'Litecoin', 'EUR': 'Euros', 'USD': 'USD', 'GBP': 'British pound', 'CAD': 'Canadian'}
allowed_pairs = {('ETH', 'USD'): 'ETH_USD', ('ETH', 'EUR'): 'ETH_EUR', ('ETH', 'BTC'): 'ETH_BTC',
					('BTC', 'USD'): 'USD', ('BTC', 'EUR'): 'EUR', ('BTC', 'GBP'): 'GBP', ('BTC', 'CAD'): 'CAD',
					('LTC', 'EUR'): 'LTC_EUR', ('LTC', 'BTC'): 'LTC_BTC', ('LTC', 'USD'): 'LTC_USD'}

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
	dcc.Graph(id='main-plot')
])

# Update Title
@app.callback(
	Output(component_id='title', component_property='children'),
	[Input(component_id='cur-1', component_property='value'),
	 Input(component_id='cur-2', component_property='value')])
# Callback function should never mutate variables outside their scope
def update_title(cur_1, cur_2):
	if (cur_1, cur_2) not in allowed_pairs and (cur_2, cur_1) not in allowed_pairs:
		cur_1, cur_2 = default_inputs[0], default_inputs[1]

	return cur_1 + ' to ' + cur_2

@app.callback(
	Output(component_id='main-plot', component_property='figure'),
	[Input(component_id='cur-1', component_property='value'),
	 Input(component_id='cur-2', component_property='value')])
# Callback function should never mutate variables outside their scope
def update_graph(cur_1, cur_2):
	code = ""
	if (cur_1, cur_2) in allowed_pairs:
		code = allowed_pairs[(cur_1, cur_2)]
	elif (cur_2, cur_1) in allowed_pairs:
		code = allowed_pairs[(cur_2, cur_1)]
	else:
		code = allowed_pairs[default_inputs]

	print("GDAX/" + code)
	ylabel = "Dollars in " + cur_2
	if cur_2 == 'BTC':
		ylabel = "Ratio"

	df_temp = quandl.get("GDAX/" + code, authtoken="ZHJDdS31ZueeYzkeFDsb")
	return {
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
	}

external_css = ["https://codepen.io/chriddyp/pen/bWLwgP.css",
	"https://cdn.rawgit.com/plotly/dash-app-stylesheets/2cc54b8c03f4126569a3440aae611bbef1d7a5dd/stylesheet.css"]

for css in external_css:
	app.css.append_css({"external_url": css})

if __name__ == '__main__':
	app.run_server(debug=True)