# Source code for interactive choropleth map / dashboard 
# Followed tutorials here https://towardsdatascience.com/build-an-interactive-choropleth-map-with-plotly-and-dash-1de0de00dce0
# https://towardsdatascience.com/interactive-choropleth-maps-with-plotly-46c34fba0e48
# https://towardsdatascience.com/how-to-build-a-complex-reporting-dashboard-using-dash-and-plotl-4f4257c18a7f
# Steps:

# 1: Arrange/Combine different Elements together on a defined campus
# 2: Combine all elements in one container like fig=go.Figure (data=trace2 + trace1, layout=layout);
# 3: Pass the container to dcc.Graph, dcc is dash core components, dash will create web-base web app for dashboard 


#####################################################
# Initial Set Up

# for dash and plotting capabilities
import dash
import dash_core_components as dcc # for accessing interactive data visualization with plotly.js
import dash_html_components as html # for accessing html elements h1 h2
import plotly.graph_objs as go # for designing Chloropleth map

# for reading in data
import pandas as pd
import json

# read in csv file for data analysis
df = pd.read_csv('../data_set/M_Landings_cleaned.csv')
print(df.head(10))

# Read in geojson data
with open('../data_set/coordinates.json', 'r') as json_data:
    df_coordinates = json.load(json_data)
print(type(df_coordinates))
# print(df_coordinates['features'][:])
# mapbox token for mapping choropleth map
mapbox_accesstoken = 'pk.eyJ1IjoiY3JhaWdtYXJpYW5pIiwiYSI6ImNrNTMyM2l4MDA0NHMzbHF2NTI0aHdoMzQifQ.l4cSBnBuWaV49cs1XF4MoA'

##################################################################
# Create plotly figure


# for names in our bar chart
meteors = df['name'].str.title().tolist()

# for drop down menu so we can see different parts of the data set
selection = ['mass (g)', 'recclass', 'year', 'fall']


# colorscale for choropleth map
pl_deep=[[0.0, 'rgb(253, 253, 204)'],
         [0.1, 'rgb(201, 235, 177)'],
         [0.2, 'rgb(145, 216, 163)'],
         [0.3, 'rgb(102, 194, 163)'],
         [0.4, 'rgb(81, 168, 162)'],
         [0.5, 'rgb(72, 141, 157)'],
         [0.6, 'rgb(64, 117, 152)'],
         [0.7, 'rgb(61, 90, 146)'],
         [0.8, 'rgb(65, 64, 123)'],
         [0.9, 'rgb(55, 44, 80)'],
         [1.0, 'rgb(39, 26, 44)']]
# first trace for bar chart
trace_bar = []

for current in selection:
	trace_bar.append(go.Bar(
		x=df.sort_values([current], ascending=False).head(10)[current],
		y=df.sort_values([current], ascending=False).head(10)['name'].str.title().tolist(),
		xaxis='x2',
		yaxis='y2',
		marker=dict(
			color='blue',
			line=dict(
				color='black',
				width=0.5
				)
			),
		visible=False,
		name='Meterorites with attribute {} '.format(current),
		orientation='h'
		))

trace_bar[0]['visible']=True

# second trace for choropleth map
trace_map = []

for current in selection:
	trace_map.append(go.Choroplethmapbox(
		geojson = df_coordinates,
		# geojson= df_coordinates['features'][:],
		locations=df['GeoLocation'].tolist(),
		z = df[current].tolist(),
		colorscale=pl_deep,
		text=meteors,
		colorbar=dict(
			thickness=20,
			ticklen=3),
		marker_line_width=0,
		marker_opacity=0.7,
		visible=False,
		subplot='mapbox1',
		hovertemplate = "<b>%{text}</b><br><br>" +
                        "Price: %{z}<br>" +
                        "<extra></extra>"
                    )
    ) # "<extra></extra>" means we don't display the info in the secondary box, such as trace id.

trace_map[0]['visible']=True


# latitude = -33.892319
# longitude = 151.146167
# latitude=0
# longitude=0
# ###########################################################################
# For creating the dash app
layout = go.Layout(
	title= {'text': "NASA's Meteorite Landings",
		'font' : {'size' : 28,
				'family' :'Arial'}},

		autosize=True,

		mapbox1 = dict(
			domain = {'x': [0.3, 1],'y': [0, 1]},
	        # center = dict(lat=latitude, lon=longitude),
	        accesstoken = mapbox_accesstoken, 
	        # zoom = 12
	      	),

		xaxis2={
			'zeroline': False,
	        "showline": False,
	        "showticklabels":True,
	        'showgrid':True,
	        'domain': [0, 0.25],
	        'side': 'right',
	        'anchor': 'x2',
	        },
	    yaxis2={
	    	'domain': [0.4, 0.9],
	        'anchor': 'y2',
	        'autorange': 'reversed',
	     	},
	)

layout.update(
	updatemenus=list([
		dict(x=0,
			y=1,
			xanchor='left',
			yanchor='middle',
			buttons=list([
				dict(
					args=['visible', [True, False, False, False]],
					label='Attribute type: Mass in Grams',
					method='restyle'
					),
				dict(
					args=['visible', [False, True, False, False]],
					label='Attribute type: Classification',
					method='restyle'
					),
				dict(
					args=['visible', [False, False, True, False]],
					label='Atribute type: Year',
					method='restyle'
					),
				dict(
					args=['visible', [False, False, False, True]],
					label='Attribute type: Fall',
					method='restyle'
					)


				])
			)
		])
	)

fig=go.Figure(data=trace_bar + trace_map, 
	layout=layout)



app = dash.Dash() # initialize app 
app.layout = html.Div(children=[
	html.H1(children=''),

    dcc.Graph(
        id='example-graph-1',
        figure=fig
    ),
])
# interpreter starts at __name__ == "__main__"
# if we try importing this file as a seperate module it will not run 
if __name__ == "__main__":
	app.run_server(debug=False)