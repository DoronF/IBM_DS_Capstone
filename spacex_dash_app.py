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

# Launch site dropdown options
options=[{'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
             {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
             {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
             {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'}]
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', 
                                            options=options, 
                                            value='ALL', 
                                            placeholder="Select a Launch Site here",
                                            searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,
                                                value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback([
                Output(component_id='success-pie-chart', component_property='figure'),
                Output(component_id='success-payload-scatter-chart', component_property='figure')
            ],
            [
                Input(component_id='site-dropdown', component_property='value'),
                Input(component_id='payload-slider', component_property='value')
             ])

def get_pie_chart(entered_site, payload_range):
    filtered_df = spacex_df
     
    #filtered_df = filtered_df.columns.str.replace(' ', '')
    if entered_site == 'ALL':
        filtered_df = filtered_df[((filtered_df['Payload Mass (kg)']  >= payload_range[0]) & (filtered_df['Payload Mass (kg)']  <= payload_range[1]))]
        filtered_counts = filtered_df.groupby('Launch Site', as_index=False)['class'].count()
        fig_1 = px.pie(filtered_counts, values='class', 
        names='Launch Site',
        title='Success rate for all launch sites')
        fig_2 = px.scatter(filtered_df, 
                            x='Payload Mass (kg)', 
                            y='class', 
                            color='Booster Version Category',
                            title='Correlation between Payload and Success for All Sites')
        fig_2.update_yaxes(tickvals=[0, 1], nticks=2)
        fig_2.update_layout(yaxis_title='Success')
        return [fig_1, fig_2]
    else:
        #condition = "'Launch Site' == '"+ entered_site +"'"
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        filtered_df = filtered_df[((filtered_df['Payload Mass (kg)']  >= payload_range[0]) & (filtered_df['Payload Mass (kg)']  <= payload_range[1]))]
        filtered_counts = filtered_df.groupby('class' , as_index=False)['class'].count()
        fig_1 = px.pie(filtered_counts, values='class', 
        names=['Success', 'Otherwise'],
        title='Success rate for ' + entered_site)
        fig_2 = px.scatter(filtered_df, 
                            x='Payload Mass (kg)', 
                            y='class', 
                            color='Booster Version Category',
                            title='Correlation between Payload and Success for ' + entered_site
                            )
        fig_2.update_yaxes(tickvals=[0, 1], nticks=2)
        fig_2.update_layout(yaxis_title='Success')
        return [fig_1, fig_2]
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run_server()
