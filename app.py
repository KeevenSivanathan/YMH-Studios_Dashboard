import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv('ymh_studios.csv')

app = dash.Dash(__name__,external_stylesheets =[dbc.themes.BOOTSTRAP,dbc.icons.FONT_AWESOME])

plot_background_color = '#FFFFFF'
paper_background_color = '#FFFFFF'
colors = ['#0091D5']
colors2 = ['#EA6A47','#0091D5']
colors3 = ['#7E909A','#EA6A47','#0091D5']
colors_line = ['#EA6A47','#0091D5','#00CC66','#6B2737','#F1DB4B','#090C08','#DB5ABA']

app.layout = html.Div([
    #HEADER
    html.Header([
        html.H1('yourmomsanalytics')
    ], id="sticky"),

    #BODY
    #ROW 1
    dbc.Row([
        #ITEM 1
        dbc.Col(
            html.Div([
            #DROPDOWN
            dcc.Dropdown(id='year_option',options=[c for c in df['year_published'].unique()],
                         value='2022',clearable=False,
                         style=dict(width='80%',display='inline-block',verticalAlign="middle"),
                         className="dcc_compon"),
            #GRAPH
            dcc.Graph(id='bar-chart3',config={'displayModeBar': 'hover'})
            ],className ='create_container twelve columns'),width = 4
        ),
        #ITEM 2
        dbc.Col(
            html.Div([
            #DROPDOWN
            dcc.Dropdown(id='podcast_option',options=[i for i in df['podcast'].unique()],value='Tom Talks',
                         clearable=False,style=dict(width='80%',display='inline-block',verticalAlign="middle"),
                         className="dcc_compon"),
            # GRAPH
            dcc.Graph(id='bar-chart2',config={'displayModeBar': 'hover'})
            ],className ='create_container twelve columns'), width = 4
        ),
        #ITEM 3
        dbc.Col(
            html.Div([
            #DROPDOWN
            dcc.Dropdown(id='allTime_option',options=['Views','Likes','Comments'],value='Likes',
                         clearable=False,style=dict(width='80%',display='inline-block',verticalAlign="middle"),
                         className="dcc_compon"),
            # GRAPH
            dcc.Graph(id = 'allTime-chart',config = {'displayModeBar': 'hover'})
            ],className ='create_container twelve columns'),width = 4
        )
    ],align="start"),
    #ROW 2
    dbc.Row([
        #ITEM 1
        dbc.Col(
            html.Div([
            #DROPDOWN
            dcc.Dropdown(id='statistic_option',options=['Views','Likes','Comments'],
                         value="Views",clearable=False,
                         style=dict(width='40%',display='inline-block',verticalAlign="middle"),
                         className="dcc_compon"),
            #GRAPH
            dcc.Graph(id="line-chart",config = {'displayModeBar': 'hover'})
            ],className ='create_container twelve columns')
        )
    ],align="center"),
    #ROW 3
    dbc.Row([
        #ITEM 1
        dbc.Col(
            html.Div([
            #GRAPH
            dcc.Graph(id='bar-chart',config={'displayModeBar': 'hover'})
            ],className ='create_container twelve columns'),width = 4
        ),
        #ITEM 2
        dbc.Col(
            html.Div([
                html.Div(id='text1'),
                html.Div(id='text2'),
                html.Div(id='text3'),
                html.Div(id='text4')
            ],className ='create_container twelve columns'),width = 4
        ),
        #ITEM 3
        dbc.Col(
            html.Div([
            #DROPDOWN
            dcc.Dropdown(id='channel_stats',
                         options=['Subscribers', 'Video Count', 'Views'],
                         value='Subscribers',clearable=False,
                         style=dict(width='60%',display='inline-block',verticalAlign="middle"),
                         className="dcc_compon"),

            #GRAPH
            dcc.Graph(id='pie-chart',config={'displayModeBar': 'hover'})
            ],className ='create_container twelve columns'),width = 4
        )
    ],align="start"),

    #FOOTER
    html.Footer([

        html.Div([
            html.A(html.I(className="fa-brands fa-github"), href='https://github.com/KeevenSivanathan'),
            html.A(html.I(className="fa-solid fa-user-astronaut"), href='https://keevensivanathan.webflow.io/'),
            html.A(html.I(className="fa-brands fa-linkedin"), href='https://www.linkedin.com/in/ksivanathan/')
        ], className="footer-right"),

        html.Div([
            html.P([
                dcc.Link('Back to Top',href = '#',className='link-1'),
                html.A("YMH",href='https://www.youtube.com/c/YourMomsHousePodcast'),
                html.A('Tom Segura',href = 'https://www.youtube.com/user/tomsegura'),
                html.A('Christina P.',href = 'https://www.youtube.com/c/ChristinaP'),
            ],className="footer-links")
        ],className="footer-left")
    ],className="footer-distributed")
])

##### VISUALIZATIONS #####
#TOP 10 ALL TIME - BAR CHART
@app.callback(
    Output('allTime-chart','figure'),
    Input('allTime_option','value')
)
def update_AllTime(value):
    df = pd.read_csv('ymh_studios.csv')
    option = value.lower()
    data = pd.DataFrame(df.groupby([option, 'podcast', 'year_published'])['video_title'].sum()).reset_index()
    data = data.sort_values([option], ascending=False)
    data = data.head(10)
    data = data.iloc[::-1]

    y_axis_labels = [str(i) for i in range(1,11)]
    y_axis_labels.reverse()

    fig = px.bar(data,
                 x=data[option],
                 y = y_axis_labels,
                 color=data['podcast'],
                 custom_data=['podcast','video_title'],
                 color_discrete_sequence=colors2,
                 category_orders={"podcast": ["Your Mom's House", "2 Bears 1 Cave"]},
                 title = 'Top 10 Episodes of All-Time by {}'.format(value),
                 labels={"views": 'Views',"y": '',"podcast": "Podcast"})

    fig.update_traces(hovertemplate="<br>".join([
        "%{customdata[0]}",
        "Views: %{x}",
        "Episode Title: %{customdata[1]}",
        "<extra></extra>"
    ]))

    fig.update_yaxes(showticklabels=True, visible=True, showgrid = False,categoryorder='array',
                     categoryarray=['10','9','8','7','6','5','4','3','2','1'])
    fig.update_yaxes(tickfont=dict(size=14),ticksuffix = "  ")
    fig.update_xaxes(tickfont=dict(size=14))
    fig.update_xaxes(showgrid = True)

    fig.update_layout(
        plot_bgcolor=plot_background_color,
        paper_bgcolor=paper_background_color,
        title={'x': 0.5,'xanchor': 'center'},
        title_font_color='#202020')

    return fig



#YOUTUBE DATA BREAKDOWN
@app.callback(
    Output('pie-chart','figure'),
    Input('channel_stats','value'))
def update_pieChart(channel_stats):
    # Channel Data
    df_stats = pd.read_csv("channel_stats.csv")
    channel_names = [i for i in df_stats['channel_name'].unique()]

    if channel_stats == 'Subscribers':
        data = [i for i in df_stats['subscribers']]

    if channel_stats == 'Video Count':
        data = [i for i in df_stats['video_count']]

    if channel_stats == 'Views':
        data = [i for i in df_stats['views']]


    fig = px.bar(df_stats,
                 y=channel_names,
                 x=data,
                 color_discrete_sequence=colors,
                 title = 'YouTube Channel: {}'.format(channel_stats))



    fig.update_traces(hovertemplate='%{value}')
    fig.update_yaxes(tickfont=dict(size=14), ticksuffix=" ")
    fig.update_xaxes(tickfont=dict(size=14))
    fig.update_layout(
        plot_bgcolor=plot_background_color,
        paper_bgcolor=paper_background_color,
        legend=dict(title = 'Youtube Channel',yanchor="top",y=0.8,xanchor="right",x=1.5),
        title={'x': 0.5,'xanchor': 'center'},
        xaxis=dict(title='{}'.format(channel_stats)),
        yaxis=dict(title=''),
        title_font_color='#202020')

    return fig


#EPISODE COUNT - BAR CHART
@app.callback(
    Output('bar-chart','figure'),
    Input('channel_stats','value'))
def update_barChart1(value):
    df_epCount = pd.read_csv('episode_count.csv')

    fig = px.bar(df_epCount,
                 y=df_epCount['playlist_title'],
                 x=df_epCount['item_count'],
                 color_discrete_sequence=colors,
                 title = 'Number of Episodes in each Podcast')

    fig.update_traces(hovertemplate='Count: %{x}')
    fig.update_yaxes(tickfont=dict(size=13), ticksuffix=" ")
    fig.update_xaxes(tickfont=dict(size=14))

    fig.update_layout(
        plot_bgcolor=plot_background_color,
        paper_bgcolor=paper_background_color,
        xaxis=dict(title='Episode Count'),
        yaxis=dict(title=''),
        title={'x': 0.5,'xanchor': 'center'},
        title_font_color='#202020'
    )

    return fig


#LINE CHART
@app.callback(
    Output('line-chart','figure'),
    Input('statistic_option','value')
)
def update_lineChart(statistic_option):
    df_lineChart = pd.read_csv('ymh_studios.csv')
    option = statistic_option.lower()

    fig = px.line(df_lineChart,
        x= df_lineChart['date_published'],
        y= df_lineChart[option],
        color = df_lineChart['podcast'],
        color_discrete_sequence=colors_line,
        title = "Number of {} from 2016 to 2022".format(statistic_option),
        custom_data=['podcast','episode_num'],
        labels = {
            "date_published":'Date Published',
            "podcast":'Podcast'
        }
    )

    fig.update_traces(hovertemplate="<br>".join([
        "%{customdata[0]}",
        "Episode: %{customdata[1]}",
        "Date Published: %{x}",
        "Count: %{y}",
        "<extra></extra>"
    ]))

    fig.update_yaxes(tickfont=dict(size=14), ticksuffix=" ")
    fig.update_xaxes(tickfont=dict(size=14))

    fig.update_layout(legend=dict(yanchor="top",y=0.75,xanchor="left",x=1.02),
                      plot_bgcolor=plot_background_color,
                      paper_bgcolor=paper_background_color,
                      title={'x': 0.5,'xanchor': 'center'},
                      xaxis=dict(showgrid=False),
                      yaxis=dict(showgrid=False),
                      title_font_color='#202020')

    return fig

#TOP 10 BY PODCAST - BAR CHART
@app.callback(
    Output('bar-chart2','figure'),
    Input('podcast_option','value'))
def update_barChart2(podcast_option):

    df = pd.read_csv('ymh_studios.csv')

    #CODE TO GET PODCAST
    selection = df[df['podcast'] == podcast_option]
    result = pd.DataFrame(selection.groupby(['views','video_title'])['episode_num'].sum()).reset_index()
    result = result.sort_values(['views'], ascending=False)
    result = result.head(10)

    x_vals = [int(i) for i in result['episode_num']]
    x_vals = [str(i) for i in x_vals]

    fig = px.bar(result,
                 y=result['views'],
                 x=x_vals,
                 color_discrete_sequence=colors,
                 custom_data=['video_title'],
                 title = '{}: Top 10 Most Viewed Episodes'.format(podcast_option))

    fig.update_traces(hovertemplate="<br>".join([
        "Title: %{customdata[0]}",
        "Episode: %{x}",
        "Views: %{y}",
        "<extra></extra>"
    ]))

    fig.update_yaxes(tickfont=dict(size=13), ticksuffix=" ")
    fig.update_xaxes(tickfont=dict(size=14), ticksuffix=" ")

    fig.update_layout(
        plot_bgcolor=plot_background_color,
        paper_bgcolor=paper_background_color,
        xaxis=dict(title='Episode Number'),
        yaxis=dict(title='Number of Views'),
        title={'x': 0.5,'xanchor': 'center'},
        title_font_color='#202020')

    return fig


#TOP 10 BY YEAR - BAR CHART
@app.callback(
    Output('bar-chart3','figure'),
    Input('year_option', 'value'))
def update_barChart3(value):

    df = pd.read_csv('ymh_studios.csv')
    data = df.copy()
    data = data.loc[data['year_published'] == int(value)]
    data = pd.DataFrame(data.groupby(['views', 'podcast', 'year_published'])['video_title'].sum()).reset_index()
    data = data.sort_values(['views'], ascending=False)
    data = data.head(10)
    data = data.iloc[::-1]

    y_axis_labels = [str(i) for i in range(1,11)]
    y_axis_labels.reverse()

    fig = px.bar(data,
                 x=data['views'],
                 y = y_axis_labels,
                 color=data['podcast'],
                 color_discrete_sequence=colors2,
                 category_orders={"podcast": ["Your Mom's House", "2 Bears 1 Cave"]},
                 custom_data=['podcast','video_title'],
                 title = 'Top 10 Most Viewed Episodes in {}'.format(value),
                 labels={"views": 'Views',"y": '',"podcast": "Podcast"})

    fig.update_traces(hovertemplate="<br>".join([
        "%{customdata[0]}",
        "Views: %{x}",
        "Episode Title: %{customdata[1]}",
        "<extra></extra>"
    ]))

    fig.update_yaxes(showticklabels=True, visible=True, showgrid = False,categoryorder='array',
                     categoryarray=['10','9','8','7','6','5','4','3','2','1'])
    fig.update_yaxes(tickfont=dict(size=13), ticksuffix="  ")
    fig.update_xaxes(tickfont=dict(size=14))
    fig.update_xaxes(showgrid=True)

    fig.update_layout(
        plot_bgcolor=plot_background_color,
        paper_bgcolor=paper_background_color,
        title={'x': 0.5,'xanchor': 'center'},
        title_font_color='#202020')

    return fig

#TEXT
#TEXT 1
@app.callback(
    Output('text1', 'children'),
    [Input('channel_stats', 'value')])

def update_text(value):

    total_YMH_ep = df.shape[0]

    return [

               html.H6(children = 'Total Episodes',
                       style = {'textAlign': 'center',
                                'color': '#202020'}
                       ),

               html.P('{:,}'.format(total_YMH_ep),
                      style={'textAlign': 'center',
                             'color': '#EA6A47',
                             'fontSize': 15,
                             'margin-top': '-10px'
                             }
                      ),
    ]

#TEXT 2
@app.callback(
    Output('text2', 'children'),
    [Input('channel_stats', 'value')])

def update_text(value):

    result = df['views'].sum()

    return [

               html.H6(children = 'Total Views',
                       style = {'textAlign': 'center',
                                'color': '#202020'}
                       ),

               html.P('{:,}'.format(result),
                      style={'textAlign': 'center',
                             'color': '#EA6A47',
                             'fontSize': 15,
                             'margin-top': '-10px'
                             }
                      ),
    ]

#TEXT 3
@app.callback(
    Output('text3', 'children'),
    [Input('channel_stats', 'value')])

def update_text(value):

    result = df['likes'].sum()

    return [

               html.H6(children = 'Total Likes',
                       style = {'textAlign': 'center',
                                'color': '#202020'}
                       ),

               html.P('{:,}'.format(result),
                      style={'textAlign': 'center',
                             'color': '#EA6A47',
                             'fontSize': 15,
                             'margin-top': '-10px'
                             }
                      ),
    ]

#TEXT 4
@app.callback(
    Output('text4', 'children'),
    [Input('channel_stats', 'value')])

def update_text(value):

    result = df['comments'].sum()

    return [

               html.H6(children = 'Total Comments',
                       style = {'textAlign': 'center',
                                'color': '#202020'}
                       ),

               html.P('{:,}'.format(result),
                      style={'textAlign': 'center',
                             'color': '#EA6A47',
                             'fontSize': 15,
                             'margin-top': '-10px'
                             }
                      ),
    ]

##### END OF VISUALIZATIONS ######

if __name__ == '__main__':
    app.run_server(debug=True)