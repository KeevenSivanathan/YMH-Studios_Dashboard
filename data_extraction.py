from googleapiclient.discovery import build
import pandas as pd
import numpy as np
import re

# Function to scrape channel stats
def get_channel_data(service, channel_ids):
    data = []
    request = youtube.channels().list(
        part='snippet,contentDetails,statistics',
        id=','.join(channel_ids))

    response = request.execute()
    for i in range(len(response['items'])):
        channel_data = dict(channel_name=response['items'][i]['snippet']['title'],
                            subscribers=response['items'][i]['statistics']['subscriberCount'],
                            views=response['items'][i]['statistics']['viewCount'],
                            video_count=response['items'][i]['statistics']['videoCount']
                            )
        data.append(channel_data)
    return data


# Function to get playlist data from channel
def get_playlist_data(service, channel_id):
    all_playlists = []
    request = youtube.playlists().list(
        part="snippet,contentDetails",
        channelId=channel_id,
        maxResults=25
    )
    response = request.execute()
    for i in range(len(response['items'])):
        playlist = dict(playlist_title=response['items'][i]['snippet']['title'],
                        item_count=response['items'][i]['contentDetails']['itemCount'],
                        playlist_id=response['items'][i]['id'])

        all_playlists.append(playlist)

    return all_playlists


# Function to get video_ids from playlist
def get_video_id(service, playlist_id):
    request = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=playlist_id,
        maxResults=50
    )
    response = request.execute()

    video_ids = []

    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])

    next_page_token = response.get('nextPageToken')
    more_pages = True

    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request = youtube.playlistItems().list(
                part="contentDetails",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()

            for i in range(len(response['items'])):
                video_ids.append(response['items'][i]['contentDetails']['videoId'])

                next_page_token = response.get('nextPageToken')

    return video_ids


# Function to get video statistics
def get_video_stats(service, video_ids):
    all_stats = []

    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part='snippet,statistics',
            id=",".join(video_ids[i:i + 50]))

        response = request.execute()

        for video in response['items']:
            video_stats = dict(video_title=video['snippet']['title'],
                               date_published=video['snippet']['publishedAt'],
                               views=video['statistics'].get('viewCount'),
                               likes=video['statistics']['likeCount'],
                               comments=video['statistics']['commentCount'])

            all_stats.append(video_stats)

    return all_stats


# Function to extract episode number of podcast from video title
def extract_episode(df):
    # Extracting all integers from video title
    df['episode_num'] = df['video_title'].astype('str').str.extractall('(\d+)').unstack().fillna('').sum(axis=1).astype(
        int)

    return df


# Function to clean string
def clean_string(df):
    # 2 Bears, 1 Cave Edits
    df['video_title'] = df['video_title'].map(lambda x: x.replace('2 Bears 1 Cave w/', ''))
    df['video_title'] = df['video_title'].map(lambda x: x.replace('2 Bears, 1 Cave w/', ''))
    # Where My Moms At Edits
    df['video_title'] = df['video_title'].map(lambda x: x.replace('Having 2 Sets Of Twins', 'Having Two Sets of Twins'))
    df['video_title'] = df['video_title'].map(
        lambda x: x.replace('2 Fingers w/ Dion Bardeau', 'Two Fingers w/ Dion Bardeau'))
    df['video_title'] = df['video_title'].map(lambda x: x.replace('Part 1', 'Part One'))
    df['video_title'] = df['video_title'].map(lambda x: x.replace('Part 2', 'Part Two'))
    df['video_title'] = df['video_title'].map(lambda x: x.replace('6,000', 'Six Thousand'))
    # YMH Edits
    df['video_title'] = df['video_title'].map(lambda x: x.replace('2/12/17', ''))
    df['video_title'] = df['video_title'].map(lambda x: x.replace('10/8/17', ''))
    df['video_title'] = df['video_title'].map(lambda x: x.replace('H3H3', 'Ethan Klein'))
    df['video_title'] = df['video_title'].map(lambda x: x.replace('Best Mom-ents of 2019', 'End of Year Best Moments'))
    df['video_title'] = df['video_title'].map(lambda x: x.replace('Best Moments of 2019', 'End of Year Best Moments'))
    df['video_title'] = df['video_title'].map(lambda x: x.replace('Shaggy 2 Dope', 'Shaggy Two Dope'))
    # Dr.Drew Edits
    df['video_title'] = df['video_title'].map(
        lambda x: x.replace('Ep. 47 Best Moments Of 2019 ', 'Ep. 47 End of Year Best Moments'))
    df['video_title'] = df['video_title'].map(lambda x: x.replace('Queen Above 18', 'Queen Above Eighteen'))
    df['video_title'] = df['video_title'].map(lambda x: x.replace('Option No. 2', 'Option Two'))

    return df


# Function to preprocess dataframe
def preprocess(df_1, df_2, df_3, df_4, df_5, df_6, df_7, df_8):
    # Edits to string in video title
    df_1 = clean_string(df_1)
    df_2 = clean_string(df_2)
    df_3 = clean_string(df_3)
    df_4 = clean_string(df_4)
    df_5 = clean_string(df_5)
    df_6 = clean_string(df_6)
    df_7 = clean_string(df_7)
    df_8 = clean_string(df_8)

    # Extract Episode Number from video title
    pod_1 = extract_episode(df_1)
    pod_2 = extract_episode(df_2)
    pod_3 = extract_episode(df_3)
    pod_4 = extract_episode(df_4)
    pod_5 = extract_episode(df_5)
    pod_6 = extract_episode(df_6)
    pod_7 = extract_episode(df_7)
    pod_8 = extract_episode(df_8)

    # Join into a single dataframe of all podcasts
    df_allPodcasts = pd.concat([pod_1, pod_2, pod_3, pod_4, pod_5, pod_6, pod_7, pod_8])

    # Converting date_published to datetime
    df_allPodcasts['date_published'] = df_allPodcasts['date_published'].map(lambda x: x.split('T')[0])
    df_allPodcasts['date_published'] = pd.to_datetime(df_allPodcasts['date_published'])

    # Extract Year from date
    df_allPodcasts['year_published'] = df_allPodcasts['date_published'].dt.to_period('Y')
    df_allPodcasts['year_published'] = df_allPodcasts['year_published'].astype(str)

    # Drop Rows with Missing Values --> 2 rows dropped which were live broadcast episodes
    df_allPodcasts = df_allPodcasts.dropna()

    # Converting Views, Likes, Comments to ints
    df_allPodcasts["views"] = df_allPodcasts["views"].astype(str).astype(int)
    df_allPodcasts["likes"] = df_allPodcasts["likes"].astype(str).astype(int)
    df_allPodcasts["comments"] = df_allPodcasts["comments"].astype(str).astype(int)

    df_allPodcasts = df_allPodcasts[["podcast", "episode_num", "date_published", "year_published",
                                     "views", "likes", "comments", "video_title"]]

    df_allPodcasts = df_allPodcasts.sort_values('date_published', ascending=True)

    return df_allPodcasts

api_key = 'AIzaSyA_jfPRBDK9G19VT8RluNrqhx5ibDyDo-Y'
youtube = build('youtube', 'v3', developerKey = api_key)
channel_ids = ['UCYIgiXwJck_Pb5Nj-wIrsqg','UCuT0B27AxYqCPWMJixOOnMQ','UCi6roWLrNBmXCCF8URGQE3A']
channel_data = pd.DataFrame(get_channel_data(youtube, channel_ids))

#Dataframe of playlist data
#YMH playlist data
ymh_playlist_data = pd.DataFrame(get_playlist_data(youtube, channel_ids[0]))

#Tom Segura playlist data
segura_playlist_data = pd.DataFrame(get_playlist_data(youtube, channel_ids[1]))

#Christina P. playlist data
christina_playlist_data = pd.DataFrame(get_playlist_data(youtube, channel_ids[2]))


podcast_list = ['The Danny Brown Show - Full Episodes', 'Tom Talks - Full Episodes',
               '2 Bears 1 Cave - Full Episodes',
                'Dr. Drew After Dark - Full Episodes',
                'YMH Podcast - Full Episodes','Where My Moms At Podcast - Full Episodes',
               'The Josh Potter Show - Full Episodes','YMH Podcast - Classic Jeans']

#Get podcasts from YMH playlist
podcasts_YMH = ymh_playlist_data.copy()
podcasts_YMH = podcasts_YMH.loc[ymh_playlist_data['playlist_title'].isin(podcast_list)]
podcasts_YMH = podcasts_YMH[podcasts_YMH.playlist_title != 'Tom Talks - Full Episodes']

#Get podcasts from Tom Segura playlist
podcasts_segura = segura_playlist_data.copy()
podcasts_segura = podcasts_segura.loc[segura_playlist_data['playlist_title'].isin(podcast_list)]

#Get podcasts from Christina P. playlist
podcasts_christina = christina_playlist_data.copy()
podcasts_christina = podcasts_christina.loc[christina_playlist_data['playlist_title'].isin(podcast_list)]

podcasts_produced = pd.concat([podcasts_YMH,podcasts_segura,podcasts_christina])

#Preprocessing
#Remove '- Full Episodes'
podcasts_produced['playlist_title'] = podcasts_produced['playlist_title'].map(
    lambda x: x.replace('- Full Episodes',''))

#Trim Whitespace
podcasts_produced['playlist_title'] = podcasts_produced['playlist_title'].map(
    lambda x: x.strip())

# #Remove newline character
podcasts_produced['playlist_title'] = podcasts_produced['playlist_title'].map(
    lambda x: x.replace("\n",''))

podcasts_produced = podcasts_produced.sort_values('item_count',ascending = True)

#Getting id's of playlist of full podcast episodes
danny_brown = podcasts_produced[podcasts_produced['playlist_title'] == 'The Danny Brown Show']['playlist_id'].iloc[0]
tom_talks = podcasts_produced[podcasts_produced['playlist_title'] == 'Tom Talks']['playlist_id'].iloc[0]
twoBears_oneCave = podcasts_produced[podcasts_produced['playlist_title'] == '2 Bears 1 Cave']['playlist_id'].iloc[0]
where_myMoms = podcasts_produced[podcasts_produced['playlist_title'] == 'Where My Moms At Podcast']['playlist_id'].iloc[0]
dr_drew = podcasts_produced[podcasts_produced['playlist_title'] == 'Dr. Drew After Dark']['playlist_id'].iloc[0]
ymh_podcast = podcasts_produced[podcasts_produced['playlist_title'] == 'YMH Podcast']['playlist_id'].iloc[0]
josh_potter = podcasts_produced[podcasts_produced['playlist_title'] == 'The Josh Potter Show']['playlist_id'].iloc[0]
classic_jeans = podcasts_produced[podcasts_produced['playlist_title'] == 'YMH Podcast - Classic Jeans']['playlist_id'].iloc[0]

#Adding classic jeans episodes to YMH Episodes
classicJeans_count = podcasts_produced[podcasts_produced['playlist_title'] == 'YMH Podcast - Classic Jeans']['item_count'].iloc[0]
YMH_count = podcasts_produced[podcasts_produced['playlist_title'] == 'YMH Podcast']['item_count'].iloc[0]
YMH_totalCount = classicJeans_count + YMH_count
podcasts_produced = podcasts_produced.loc[podcasts_produced['item_count'] != 23]
podcasts_produced = podcasts_produced.replace(YMH_count,YMH_totalCount)

#Retrieving video id's of all videos in podcast playlist
videoID_dannyBrown = get_video_id(youtube, danny_brown)
videoID_tomTalks = get_video_id(youtube, tom_talks)
videoID_2B1C = get_video_id(youtube, twoBears_oneCave)
videoID_myMoms = get_video_id(youtube, where_myMoms)
videoID_drDrew = get_video_id(youtube, dr_drew)
videoID_YMH = get_video_id(youtube, ymh_podcast)
videoID_joshPotter = get_video_id(youtube, josh_potter)
videoID_classicJeans = get_video_id(youtube, classic_jeans)

#Placing video stats into dataframes & adding column titled 'podcast'
df_dannyBrown = pd.DataFrame(get_video_stats(youtube, videoID_dannyBrown))
df_dannyBrown['podcast'] = 'The Danny Brown Show'

df_tomTalks = pd.DataFrame(get_video_stats(youtube, videoID_tomTalks))
df_tomTalks['podcast'] = 'Tom Talks'

df_2B1C = pd.DataFrame(get_video_stats(youtube, videoID_2B1C))
df_2B1C['podcast'] = '2 Bears 1 Cave'

df_myMoms = pd.DataFrame(get_video_stats(youtube, videoID_myMoms))
df_myMoms['podcast'] = 'Where My Moms At Podcast'

df_drDrew = pd.DataFrame(get_video_stats(youtube, videoID_drDrew))
df_drDrew['podcast'] = 'Dr.Drew After Dark'

df_YMH = pd.DataFrame(get_video_stats(youtube, videoID_YMH))
df_YMH['podcast'] = "Your Mom's House"

df_joshPotter = pd.DataFrame(get_video_stats(youtube, videoID_joshPotter))
df_joshPotter['podcast'] = "The Josh Potter Show"

df_classicJeans = pd.DataFrame(get_video_stats(youtube, videoID_classicJeans))
df_classicJeans['podcast'] = "Your Mom's House"

df = preprocess(df_dannyBrown, df_tomTalks, df_2B1C, df_drDrew, df_YMH, df_myMoms,df_joshPotter,df_classicJeans)

#Export as csv file
df.to_csv('ymh_studios.csv')
channel_data.to_csv('channel_stats.csv')
podcasts_produced.to_csv('episode_count.csv')

print("Data has been extracted to csv files.")