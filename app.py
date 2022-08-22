import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv('ymh_studios.csv')

app = dash.Dash(__name__,meta_tags=[{"name": "viewport", "content": "width=device-width"}])


plot_background_color = '#000000'
paper_background_color = '#000000'

colors = ['#377eb8']
colors2 = ['#e41a1c','#377eb8']
colors3 = ['#e41a1c','#377eb8','#4daf4a']
colors_line = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#e7298a']

app.layout = html.Div([

    html.Header([
        html.H1('yourmomsanalytics')
    ], id="sticky"),

    # FIRST ROW
    html.Div([

        #TOP 10 BY YEAR
        html.Div([
            #DROPDOWN
            dcc.Dropdown(id='year_option',options=[c for c in df['year_published'].unique()],
                         value='2022',clearable=False,
                         style=dict(width='80%',display='inline-block',verticalAlign="middle"),
                         className="dcc_compon"),
            #GRAPH
            dcc.Graph(id='bar-chart3',config={'displayModeBar': 'hover'},style = {'height': '350px'})

        ], className ='create_container2 four columns', style={'height': '400px'}),

        #TOP 10 BY PODCAST
        html.Div([
            # DROPDOWN
            dcc.Dropdown(id='podcast_option',options=[i for i in df['podcast'].unique()],value='Tom Talks',
                         clearable=False,style=dict(width='80%',display='inline-block',verticalAlign="middle"),
                         className="dcc_compon"),
            # GRAPH
            dcc.Graph(id='bar-chart2',config={'displayModeBar': 'hover'}, style = {'height': '350px'})

        ], className='create_container2 four columns', style={'height': '400px'}),

        #TOP 10 ALL-TIME
        html.Div([
            # GRAPH
            dcc.Graph(id = 'allTime-chart',config = {'displayModeBar': 'hover'}, style = {'height': '350px'})

        ], className='create_container2 four columns', style={'height': '400px'})

    ],className="row flex-display"),

    # SECOND ROW
    html.Div([

        #LINE CHART
        html.Div([
            #DROPDOWN
            dcc.Dropdown(id='statistic_option',options=['Views','Likes','Comments'],
                         value="Views",clearable=False,
                         style=dict(width='40%',display='inline-block',verticalAlign="middle"),
                         className="dcc_compon"),

            #GRAPH
            dcc.Graph(id="line-chart",config = {'displayModeBar': 'hover'}, style = {'height': '350px'})
        ],className ='create_container2 twelve columns')

    ], className="row flex-display"),

    # THIRD ROW
    html.Div([

        #NO. OF EPISODES
        html.Div([
            #GRAPH
            dcc.Graph(id='bar-chart',config={'displayModeBar': 'hover'})

        ], className ='create_container2 four columns', style={'height': '400px'}),

        # TEXT
        html.Div([
            html.Div(id='text1'),
            html.Div(id='text2'),
            html.Div(id='text3'),
            html.Div(id='text4')
        ], className='create_container2 four columns', style={'height': '400px'}),

        #PIE CHART
        html.Div([
            #DROPDOWN
            dcc.Dropdown(id='channel_stats',
                         options=['Subscribers', 'Video Count', 'Views'],
                         value='Subscribers',clearable=False,
                         style=dict(width='60%',display='inline-block',verticalAlign="middle"),
                         className="dcc_compon"),

            #GRAPH
            dcc.Graph(id='pie-chart',config={'displayModeBar': 'hover'})

        ], className ='create_container2 four columns', style={'height': '400px'})

    ], className="row flex-display")

], id= "mainContainer", style={"display": "flex", "flex-direction": "column"})

##### VISUALIZATIONS #####
#TOP 10 ALL TIME - BAR CHART
@app.callback(
    Output('allTime-chart','figure'),
    Input('channel_stats','value')
)
def update_AllTime(value):
    df = pd.read_csv('ymh_studios.csv')
    data = pd.DataFrame(df.groupby(['views', 'podcast', 'year_published'])['video_title'].sum()).reset_index()
    data = data.sort_values(['views'], ascending=False)
    data = data.head(10)
    data = data.iloc[::-1]

    y_axis_labels = [str(i) for i in range(1,11)]
    y_axis_labels.reverse()

    fig = px.bar(data,
                 x=data['views'],
                 y = y_axis_labels,
                 color=data['podcast'],
                 custom_data=['podcast','video_title'],
                 width=430, height=380,
                 color_discrete_sequence=colors2,
                 category_orders={"podcast": ["Your Mom's House", "2 Bears 1 Cave"]},
                 title = 'Top 10 All-Time Most Viewed Episodes',
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
        title_font_color='#FCEFF9')

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
                 width=430, height=330,
                 title = '{} Breakdown'.format(channel_stats))



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
        title_font_color='#FCEFF9')

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
                 width=430, height=380,
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
        title_font_color='#FCEFF9'
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
        width=1400, height=360,
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
                      title_font_color='#FCEFF9')

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
                 width=420, height=335,
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
        title_font_color='#FCEFF9')

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
                 width=420, height=335,
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
        title_font_color='#FCEFF9')

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
                                'color': 'white'}
                       ),

               html.P('{:,}'.format(total_YMH_ep),
                      style={'textAlign': 'center',
                             'color': '#e41a1c',
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
                                'color': 'white'}
                       ),

               html.P('{:,}'.format(result),
                      style={'textAlign': 'center',
                             'color': '#e41a1c',
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
                                'color': 'white'}
                       ),

               html.P('{:,}'.format(result),
                      style={'textAlign': 'center',
                             'color': '#e41a1c',
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
                                'color': 'white'}
                       ),

               html.P('{:,}'.format(result),
                      style={'textAlign': 'center',
                             'color': '#e41a1c',
                             'fontSize': 15,
                             'margin-top': '-10px'
                             }
                      ),
    ]

##### END OF VISUALIZATIONS ######

if __name__ == '__main__':
    app.run_server(debug=True)