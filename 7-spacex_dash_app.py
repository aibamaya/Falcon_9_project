# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launch_sites = spacex_df['Launch Site'].unique()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                 {'label': 'All Sites', 'value': 'ALL'},
                                                 {'label': launch_sites[0], 'value': launch_sites[0]},
                                                 {'label': launch_sites[1], 'value': launch_sites[1]},
                                                 {'label': launch_sites[2], 'value': launch_sites[2]},
                                                 {'label': launch_sites[3], 'value': launch_sites[3]},
                                             ],
                                             value='ALL',
                                             placeholder="place holder here",
                                             searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={
                                                    0: '0',
                                                    2500: '2500',
                                                    5000: '5000',
                                                    7500: '7500',
                                                    10000: '10000'},
                                                value=[min_payload, max_payload]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'),

)
def get_pie_chart(entered_site):
    filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
    
    if entered_site == 'ALL':
        figure = px.pie(spacex_df, values='class', 
                        names = 'Launch Site',
                        title = 'Total Success Launches By Site')
        return figure
    else:
        new_df = filtered_df['class'].value_counts().to_frame()
        new_df['category'] = ['Failure', 'Success']
        figure = px.pie(new_df, values='class', 
                        names = 'category',
                        title = 'Total Success Launches for site ' + entered_site)
        return figure
        


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value'),]

)
def get_scatter_chart(entered_site, payload_slider):
    range_mass= (spacex_df["Payload Mass (kg)"] >= payload_slider[0]) & (spacex_df["Payload Mass (kg)"] <= payload_slider[1])
    range_df = spacex_df[range_mass]
    filtered_df = range_df[spacex_df['Launch Site'] == entered_site]
    
    if entered_site == 'ALL':
        figure = px.scatter(range_df, x="Payload Mass (kg)", y="class", 
                            color="Booster Version Category",  hover_data=['Payload Mass (kg)'],
                            title='Success Launch for All Sites with Respect to Payload Mass (kg)')
        return figure
    else:
        figure = px.scatter(filtered_df, x="Payload Mass (kg)", y="class", 
                            color="Booster Version Category",  hover_data=['Payload Mass (kg)'],
                            title='Success Launch for' + entered_site + 'Site With Respect to Payload Mass (kg)')
        return figure
        


# Run the app
if __name__ == '__main__':
    app.run_server()
