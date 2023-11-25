# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


# Create a dash application
app = dash.Dash(__name__)


# Create a dropdown menu options
dropdown_options = [{'label':value, 'value':value} for value in spacex_df['Launch Site'].unique()]
dropdown_options.insert(0, {'label':'All Sites', 'value':'ALL'})


# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),

                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                html.Div([
                                    html.Label('Select Launch Site:'),
                                    dcc.Dropdown(
                                        id='site-dropdown',
                                        options=dropdown_options,
                                        value='ALL',
                                        placeholder='Launch Site',
                                        searchable=True
                                    )
                                ]),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                html.Div(
                                    dcc.RangeSlider(id='payload-slider',
                                                    min=min_payload,
                                                    max=max_payload,
                                                    step=1000,
                                                    value=[min_payload, max_payload]
                                                )
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(
        Output(component_id='success-pie-chart', component_property='figure'),
        Input(component_id='site-dropdown', component_property='value')
    )

def get_pie_chart(entered_site):
    filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
    if entered_site == 'ALL':
        fig = px.pie(
            spacex_df[spacex_df['class']==1], 
            values='class', 
            names='Launch Site', 
            title='Success Rate Ratio of All Launch Sites')
        return fig
    else:
        filtered_df['class'] = filtered_df['class'].replace({0:'Failure',1:'Success'})
        color_mapping = {'Failure': 'crimson', 'Success': 'lightgreen'}
        fig = px.pie(
            filtered_df, 
            names='class',
            color='class',
            title=f'{entered_site}\'s Success Rate',
            color_discrete_map=color_mapping
            )
        return fig
        # return the outcomes piechart for a selected site


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
        Output(component_id='success-payload-scatter-chart', component_property='figure'),
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value')
    )

def update_payload_slider(entered_site, entered_payload_range):
    payload_filter_df = spacex_df[spacex_df['Payload Mass (kg)'].between(entered_payload_range[0]-100,entered_payload_range[1]+100)]
    filtered_df = payload_filter_df[payload_filter_df['Launch Site'] == entered_site]
    if entered_site == 'ALL':
        fig = px.scatter(
            payload_filter_df, 
            x='Payload Mass (kg)', 
            y='class', 
            color='Booster Version Category'
        )
        fig.update_layout(yaxis_title='Success Rate')
        return fig
    else:
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)', 
            y='class', 
            color='Booster Version Category'
        )
        fig.update_layout(yaxis_title='Success Rate')
        return fig

    


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
