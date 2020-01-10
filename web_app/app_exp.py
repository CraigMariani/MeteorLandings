# experimentation with dashes core components and graphing capabilities 

import dash
import dash_core_components as dcc # for accessing interactive data visualization with plotly.js
import dash_html_components as html # for accessing html elements h1 h2
import pandas as pd
import plotly.graph_objs as go # for designing Chloropleth map
# import plotly.plotly as py
# import sys
# print(sys.executable) # prints the interpreter you are using

# read in the cleaned data into a data frame
df = pd.read_csv('../data_set/M_Landings_cleaned.csv')
df_coords = pd.read_json('../data_set/coordinates.json')

print(df.head())
# we first use html componenets to render 

app = dash.Dash() # initializes app

# create a list of elements that we are going to use
colors = {
	'background' : '#FFFFFF',
	'text' : '#000000',
	'size' : 18
}

markdown_text='''
Orange = Found 

Blue = Fell

Found means that  the meteorite was not 
seen as it entered the atmosphere.

Fell means that the meteortie was seen 
as it entered the atmosphere.

'''


# app.layout contains all of our html elements inside of our dash app
app.layout = html.Div(
    style={'backgroundColor' : colors['background']},

    children=[

    	# html component for title 
	    html.H1(
	    	# children = text displayed 
	    	children='Meterorite Landings',
	    	# style = css used to modify the html
	    	style={
	    		'color' : colors['text'],
	    		'textAlign' : 'center' 
	    	}
	    ),

	    # html component for description
	    html.Div(
	    	children="An Analytics Dashboard of NASA's Meterorite Landings",
	    	style={
	    		'color' : colors['text'],
	    		'textAlign' : 'center'
	    	}
	    ),

	    # create a single trace scatter plot 
	    # but make it color coded for fall values (Fell, Found)
	    dcc.Graph(
	    	id='Graph1',

	    	figure={
	    		'data' : [
	    			dict(
	    				x = df[df['fall'] == i]['year'],
	    				y = df[df['fall'] == i]['mass (g)'],
	    				text = df[df['fall'] == i]['fall'], 
	    				mode = 'markers', 
	    				opacity = 0.8,
	    				marker={
	    					'size' : 15,
	    					'line' : {'width': 0.5, 'color': 'white'}
	    				},
	    				name=1
	    			) for i in df.fall.unique()
	    		],

	    		'layout' : dict(
	    			title='Year vs Mass',
	    			xaxis={'type': 'log', 'title': 'Year'},
	    			yaxis={'title': 'Mass in Grams'},
	    			margin={'l' : 60, 'b' : 40, 't' : 60, 'r' : 10},
	    			legend={'x' : 0, 'y' : 1},
	    			hovermode='closest'
	    			)
	    		
	    	}

	    ),

	    html.Div(

	    	dcc.Markdown(
	    		children=markdown_text,
	    		style={
	    		'color' : colors['text'],
	    		'textAlign' : 'center'
	    		}
	    		)

	    	),

	    # drop down that allows you to select what hemisphere 
	    # of the data you want to look at for the chloropleth map
	    dcc.Dropdown(
	    	options=[

	    		{'label' : 'Northern Hemisphere', 'value' : 'NH'},
	    		{'label' : 'Southern Hemisphere', 'value' : 'SH'},
	    		{'label' : 'Northern and Southern', 'value' : 'ALL'}
	    	],

	    	value='ALL'

	    	),

	    #create the choropleth map here

		
    ] 
)


# fig = go.Figure(data=go.Choropleth(
# 	locations = df_coords,
# 	z = df['mass (g)'],
# 	text = df['recclass'],
# 	colorscale = 'Blues',

# ))

# fig.update_layout(
# 	title_text='Landings',
# 	geo=dict(
# 		showframe=False,
# 		showcoastlines=False,
# 		projection_type='equirectangular'

# 		)
# )

# fig.show()


# interpreter starts at name == main
if __name__ == "__main__":
    app.run_server(debug=False) # runs server