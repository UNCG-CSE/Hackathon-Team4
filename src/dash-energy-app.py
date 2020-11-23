#!/usr/bin/env python
# coding: utf-8

# # 1. Install follwing libraries in order to run the notebook
# >dash bootstrap components:- 'pip install dash-bootstrap-components'
# <br>
# >pandas library:- 'pip install pandas'
# 

# ## 2. Import follwing modules to run the dashboard

# In[1]:


import pandas as pd
import glob
import plotly.io as pio
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime, date
from dateutil import tz, parser
import warnings
warnings.filterwarnings('ignore')
import os


# # 3. Data file handling

# In[2]:


########## Important to change path for the data files ##########

path = '../Data/Analysis' 

########## End ##########

all_files = glob.glob(path + "/*.csv")
all_files_dict={}# to store paths of data files

for csv in all_files:
    meter_name=os.path.basename(csv).replace('_results.csv','')
    all_files_dict[meter_name]=os.path.abspath(csv)


# # 4.  Handling labels and typos in meter names

# In[3]:


########## Important to change path for the data files ##########
labels = pd.read_csv('../Data/Meter Names and Labels.csv')

########## End ##########

labels = labels.rename(columns={"Name": "Building_Name"})
labels['Building_Name'] = labels['Building_Name'].str.replace("'" , " ")
labels['Building_Name'] = labels['Building_Name'].str.replace('-' , "")
labels['Building_Name'] = labels['Building_Name'].str.replace('"Spencer Hall"' , '')
labels['Building_Name'] = labels['Building_Name'].str.replace('_kWh' , "")
labels['Building_Name'] = labels['Building_Name'].str.strip()
# labels
# print(labels.Building_Name.unique())


# # 5. Preparing data for input elements and dropdowns

# In[4]:


# find building names and storing them for dropdowns
building_options=[]
build_name = {}
for index, row in labels.iterrows():
#     print(row['c1'], row['c2'])
    building_options.append({'label':row['Label'],'value':row['Building_Name']})

   
# year options
year_options = []
temp_csv = open(all_files_dict[list(all_files_dict.keys())[0]])
cols = ['Actual','Predicted','obs_ci_lower','obs_ci_upper','Datetime']
temp_df = pd.read_csv(temp_csv ,encoding = "ISO-8859-1",engine = 'python', sep=',', header=0,names=cols,error_bad_lines=False)
temp_df['Datetime'] = pd.to_datetime(temp_df['Datetime'],utc=True,infer_datetime_format=False)
years = list(set(temp_df.Datetime.dt.year))
years.sort()  
temp_csv.close()
for year in years:
    year_options.append({'label':year,'value':year})


# # 6. Initiating dash app and implementation of User interface elements

# In[5]:


# initialise dash app
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
# App layout
app.layout = html.Div([
# dashboard header    
dbc.Navbar(
    [
    html.Img(src="https://news.uncg.edu/wp-content/uploads/2018/08/NewSpartan-36009-F1.jpg", height="90px"),
        html.Pre("   UNCG ENERGY CONSUMPTION DASHBOARD \n (funded by the UNCG Green Fund)", style={'align': 'center','text-align': 'center','color':'#FFB71B','font-size': '30px','margin':'0','margin-left': '130px'}),
    ],
    color="#072955",
    dark=True,
),
html.Br(),
html.Div([
dbc.Row([    
    dbc.Col([
        dbc.Card(dbc.CardBody([
            dbc.Row(html.H4(dbc.Badge("Total/Average Consumption ",style={"background-color": "#072955"},className="ml-1"))),

            dbc.Row(

                dbc.FormGroup(
                    [
                    dbc.RadioItems(
                    options=[
                        {'label': 'Total', 'value': 'Total'},
                        {'label': 'Average', 'value': 'Average'}
                    ],
                        value='Total',
                        id="consumption",
                        inline=True,
                    ),
                    ]
                )
            ),


            dbc.Row(html.H4(dbc.Badge("Select Time Units",className="ml-1",style={"background-color": "#072955"}))),

            dbc.Row(

                dbc.FormGroup(
                    [
                    dbc.RadioItems(
                    options=[
                        {'label': 'Hourly', 'value': 'hourly'},
                        {'label': 'Daily',  'value': 'daily'},
                        {'label': 'Weekly', 'value': 'weekly'},
                        {'label': 'Monthly','value': 'monthly'}
                    ],
                        value='monthly',
                        id="freq",
                        inline=True,
                    ),
                    ]
                )
            ),
            

            dbc.Row(
                dbc.FormGroup(
                    [
                    dbc.Checklist(
                    options=[
                        {'label': 'Actual (A)', 'value': 'Actual'},
                        {'label': 'Predicted (P)', 'value': 'Predicted'}
                    ],
                        value=['Actual'],
                        id="check",
                        inline=True,
                        switch=True,
                    ),
                    ]
                )
            ),
            dbc.Row(html.H4(dbc.Badge("Select a meter ",style={"background-color": "#072955"},className="ml-1"))),

            dbc.Row(dbc.Col(
                dcc.Dropdown(
                id='meters',
                options=building_options,
                value=['Baseball'],
                multi=True),

                width=11,
            )),
        
            dbc.Row(html.H4(dbc.Badge("Select a Year/Years",style={"background-color": "#072955"},className="ml-1"))),
            dbc.Row(

                dbc.FormGroup(
                    [
                    dbc.Checklist(
                        options=year_options,
                        value=[2020],
                        id="years",
                        inline=True,
                    ),
                    ]
                )
            ), 
    ]),style={"background-color": "#FFB71B"},className="shadow-lg "),
    ], width=3),
    
    dbc.Col(
        dbc.Card(dbc.CardBody([
            dcc.Graph(id='predicted_graph', figure={}),
        ],style={"background-color": "#072955",'padding':'8px'}),className="shadow-lg "),
    width=9),    
    
    
]),    
    
html.Br(),
########################## for task 2 ##############################    
dbc.Row([     
    
    dbc.Col([
        dbc.Card(dbc.CardBody([        
            dbc.Row(html.H4(dbc.Badge("Select a meter  ",style={"background-color": "#072955"},className="ml-1"))),

            dbc.Row(dbc.Col(
                dbc.Select(
                    id="meter_group",
                    options=building_options,
                    value='Baseball'
                        ),
                width=11,
            )),

            dbc.Row(html.H4(dbc.Badge("Select Time Units",style={"background-color": "#072955"},className="ml-1"))),

            dbc.Row(
                    dbc.FormGroup(
                        [
                        dbc.RadioItems(
                        options=[
                            {'label': 'Hourly', 'value': 'hourly'},
                            {'label': 'Daily',  'value': 'daily'},
                            {'label': 'Weekly', 'value': 'weekly'},
                            {'label': 'Monthly','value': 'monthly'}
                        ],
                            value='monthly',
                            id="freq_group",
                            inline=True,
                        ),
                        ]
                    )
            ),
            dbc.Row(html.H4(dbc.Badge("Pick a date range",style={"background-color": "#072955"},className="ml-1"))),

            dbc.Row(dcc.DatePickerRange(
                id='date-picker-range',
                min_date_allowed=date(2020, 1, 1),
                max_date_allowed=date(2100, 12, 31),
                initial_visible_month=date(2020, 1, 1),
                start_date=date(2020, 1, 1),
                end_date=date(2020, 12, 31),
            )),
        ]), style={"background-color": "#FFB71B"},className="shadow-lg "),

    ],width=3),
    
    dbc.Col(  
        dbc.Card(dbc.CardBody([ 
            dcc.Graph(id='group_plot', figure={}),
        ],style={"background-color": "#072955",'padding':'8px'}),className="shadow-lg "),
    width=9),
]),


]),

],className='container-fluid')
    


# # 7. Implementing call-back function for dynamic user interaction.

# In[6]:


# Connect the Plotly graphs with Dash Components
@app.callback(
    [ Output(component_id='predicted_graph', component_property='figure'),
    Output(component_id='group_plot', component_property='figure')],
    [Input(component_id='consumption', component_property='value'),
    Input(component_id='freq', component_property='value'),
    Input(component_id='check', component_property='value'),
    Input(component_id='meters', component_property='value'),
    Input(component_id='years', component_property='value'),
    Input(component_id='meter_group', component_property='value'),
    Input(component_id='freq_group', component_property='value'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),]
)
def update_graph(cons_agg,freq,act_pred,meters,years,meter_group,freq_group,start_date,end_date):
#     print('Chosen values are:',cons_agg,freq,act_pred,meters,years)


##### fucntion to get data for real-time interactive plot of energy consumption and prediction for task 1. #####

    def get_data(cons_agg,freq,act_pred,meter,years):
        
        cols = ['Actual','Predicted','obs_ci_lower','obs_ci_upper','Datetime']
        file_path=all_files_dict[meter]
        csv_file = open(file_path)
        dff = pd.read_csv(csv_file ,encoding = "ISO-8859-1",engine = 'python', sep=',', header=0,names=cols,error_bad_lines=False)
        dff['Datetime'] = pd.to_datetime(dff['Datetime'],utc=True,infer_datetime_format=False)
        dff_sel_year = dff[dff.Datetime.dt.year.isin(years) ]
        
        if freq=='daily':
            if cons_agg == 'Total':
                dff1 = dff_sel_year.groupby(pd.Grouper(key='Datetime', freq='D'))['Actual','Predicted','obs_ci_upper','obs_ci_lower'].sum().reset_index()
            else:
                dff1 = dff_sel_year.groupby(pd.Grouper(key='Datetime', freq='D'))['Actual','Predicted','obs_ci_upper','obs_ci_lower'].mean().reset_index()

        elif freq=='weekly':
            if cons_agg == 'Total':
                dff1 = dff_sel_year.groupby(pd.Grouper(key='Datetime', freq='W'))['Actual','Predicted','obs_ci_upper','obs_ci_lower'].sum().reset_index()
            else:
                dff1 = dff_sel_year.groupby(pd.Grouper(key='Datetime', freq='W'))['Actual','Predicted','obs_ci_upper','obs_ci_lower'].mean().reset_index()
        elif freq=='monthly':
            if cons_agg == 'Total':
                dff1=dff_sel_year.groupby(pd.Grouper(key='Datetime',freq='M'))['Actual','Predicted','obs_ci_upper','obs_ci_lower'].sum().reset_index()
            else:
                dff1 = dff_sel_year.groupby(pd.Grouper(key='Datetime', freq='M'))['Actual','Predicted','obs_ci_upper','obs_ci_lower'].mean().reset_index()
        else:
            # Hourly
            if cons_agg == 'Total':
                dff1 = dff_sel_year
            else:
                dff1 = dff_sel_year
        csv_file.close()
        return(dff1)

    
    if type(meters)==str:
        meters=[meters]
    fig = go.Figure()   
    for meter in meters:
        
        data=get_data(cons_agg,freq,act_pred,meter,years)
        if 'Actual' in act_pred:     
#             fig = px.scatter(x=data['Datetime'], y=data['Actual'],)
            fig.add_trace(
                go.Scatter(x=data['Datetime'],
                            y=data['Actual'], 
                            mode='lines+markers', line={'dash': 'solid'},
                            name='A-'+meter)
            )
        if 'Predicted' in act_pred:
            fig.add_trace(go.Scatter(x=data['Datetime'], y=data['Predicted'],
                                mode='lines+markers',
                                line={'dash': 'dash'},
                                name='P-'+meter))
            fig.add_trace(go.Scatter(
                                name='Upper Bound',
                                x=data['Datetime'],
                                y=data['obs_ci_upper'],
                                mode='lines',
                                marker=dict(color="#444"),
                                line=dict(width=0),
                                showlegend=False))
            fig.add_trace(go.Scatter(
                                name='Lower Bound',
                                x=data['Datetime'],
                                y=data['obs_ci_lower'],
                                marker=dict(color="#444"),
                                line=dict(width=0),
                                mode='lines',
                                fillcolor='rgba(68, 68, 68, 0.3)',
                                fill='tonexty',
                                showlegend=False))
# marker=dict(size=7, color="red") 
    a = ''
    
    if freq=='hourly':
        a = 'Hour'
        xax = 'Time of day'
    elif freq=='daily':
        a = 'Day'
        xax = 'Date'
    elif freq=='weekly':
        a = 'Week'
        xax = 'Week'
    elif freq=='monthly':
        a = 'Month'
        xax = 'Month, Year'
    if cons_agg == 'Average':
        title = "Average Hourly Consumption at UNCG per "+ a
    elif cons_agg == 'Total':
        title = "Total Consumption at UNCG per "+ a
    fig.update_layout(
        title_text=title,
        title_xanchor="center",
        title_font=dict(size=24),
        title_x=0.5,
        showlegend=True
    )
    

    fig.update_xaxes(title_text=xax)
    fig.update_yaxes(title_text=cons_agg+' Energy consumption (KWH)')
    fig.update_layout(hovermode="x unified")
    
    
    
##### fucntion to get data for Predictive plot for task 2. #####
    def get_data_group(freq,act_pred,meter,start_date,end_date):
        
        cols = ['Actual','Predicted','obs_ci_lower','obs_ci_upper','Datetime']
        file_path=all_files_dict[meter]
        csv_file = open(file_path)
        dff = pd.read_csv(csv_file ,encoding = "ISO-8859-1",engine = 'python', sep=',', header=0,names=cols,error_bad_lines=False)
        dff['Datetime'] = pd.to_datetime(dff['Datetime'],utc=True,infer_datetime_format=False)
#         dff_sel_year = dff[dff.Datetime.dt.year.isin(years) ]
        dff_sel_year=dff.loc[(dff['Datetime'] > start_date) & (dff['Datetime'] <= end_date)]

#         print(dff_sel_year.head())
        if freq=='daily':
            dff1 = dff_sel_year.groupby(pd.Grouper(key='Datetime', freq='D'))['Actual','Predicted'].mean().reset_index()
        elif freq=='weekly':
            dff1 = dff_sel_year.groupby(pd.Grouper(key='Datetime', freq='W'))['Actual','Predicted'].mean().reset_index()
        elif freq=='monthly':
            dff1 = dff_sel_year.groupby(pd.Grouper(key='Datetime', freq='M'))['Actual','Predicted'].mean().reset_index()
        else:# Hourly
            dff1 = dff_sel_year
        csv_file.close()
        return(dff1)
#     meter_group
    from_date='a'
    to_date='a'
    group_data=get_data_group(freq_group,act_pred,meter_group,start_date,end_date)
    day_name=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
#     cc = pd.to_datetime('2015-12-23 04:40:40-04:00').weekday()
#     yr = pd.to_datetime('2015-12-23 04:40:40-04:00').year
    group_data['Datetime_week'] = group_data['Datetime'].apply(lambda x: day_name[x.weekday()]+', '+str(x.day))
#      + ' ' + str(x.year)
    fig_group = go.Figure() 
    time_delta = pd.to_datetime(end_date) - pd.to_datetime(start_date)
    if freq_group=='daily' and time_delta.days <=30:
        fig_group.add_trace(
            go.Scatter(x=group_data['Datetime_week'],
                    y=group_data['Actual'], 
                    mode='markers', 
                   line={'dash': 'solid'},
                    name='A-'+meter_group)
        )
        fig_group.add_trace(go.Scatter(x=group_data['Datetime_week'], y=group_data['Predicted'],
                    mode='lines',
                    line={'dash': 'dash'},
                    name='P-'+meter_group))
    else :
        fig_group.add_trace(
            go.Scatter(x=group_data['Datetime'],
                    y=group_data['Actual'], 
                    mode='markers', 
                   line={'dash': 'solid'},
                    name='A-'+meter_group)
        )
        fig_group.add_trace(go.Scatter(x=group_data['Datetime'], y=group_data['Predicted'],
                    mode='lines',
                    line={'dash': 'dash'},
                    name='P-'+meter_group))
    
    
    
    b = ''
    
    if freq_group=='hourly':
        b = 'Hour'
        xbx = 'Time of day'
    elif freq_group=='daily':
        b = 'Day'
        xbx = 'Date'
    elif freq_group=='weekly':
        b = 'Week'
        xbx = 'Week'
    elif freq_group=='monthly':
        b = 'Month'
        xbx = 'Month, Year'
    title_2 = "Average Hourly Consumption at UNCG per "+ b

    fig_group.update_layout(
        title_text=title_2,
        title_xanchor="center",
        title_font=dict(size=24),
        title_x=0.5,
        showlegend=True,

    )
    

    fig_group.update_xaxes(title_text=xbx)
    fig_group.update_yaxes(title_text='Average Hourly Energy consumption (KWH)')
    fig_group.update_layout(hovermode="x unified")
                      
    return fig, fig_group


# # 8. To run dash application server

# In[ ]:


##### host should be verified #####

if __name__ == '__main__':
    #app.run_server(debug=True)
    app.run_server(debug=False,host = '127.0.0.1')
    
    
    


# In[ ]:





# In[ ]:




