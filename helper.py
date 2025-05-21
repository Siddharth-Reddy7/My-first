from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
ex = URLExtract()
def fetch_stat(selected_user,df):
    if selected_user != "Overall":
        df=df[df['user']==selected_user]
    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())
    num_words = len(words)
    num_media=df[df['message']=='<Media omitted>'].shape[0]
    links = []
    for message in df['message']:
        links.extend(ex.find_urls(message))

    return num_messages, num_words,num_media,len(links)

def fetch_buzy_users(df):
    x=df['user'].value_counts().head()
    n_df=round(df["user"].value_counts()/df.shape[0]*100,2).reset_index().rename(columns={'count':'percent'})
    return x,n_df

def word_cloud(selected_user,df):
    if selected_user != "Overall":
        df=df[df['user']==selected_user]
    f = open("stop_hinglish.txt", "r")
    stop_words = f.readlines()
    temp_df = df[df['user'] != "Group Notification"]
    temp_df = temp_df[temp_df['message'] != "<Media omitted>"]

    words = []
    for meassage in temp_df['message']:
        for word in meassage.lower().split():
            if word not in stop_words:
                words.append(word)
    all_text = ' '.join(words)
    wc=WordCloud(width=500, height=500, background_color='white',min_font_size=10).generate(all_text)
    return wc
def most_common_words(selected_user,df):
    f =open("stop_hinglish.txt","r")
    stop_words = f.readlines()
    if selected_user != "Overall":
        df=df[df['user']==selected_user]
    temp_df = df[df['user'] != "Group Notification"]
    temp_df = temp_df[temp_df['message'] != "<Media omitted>"]

    words = []
    for meassage in temp_df['message']:
        for word in meassage.lower().split():
            if word not in stop_words:
                words.append(word)

    c_df=pd.DataFrame(Counter(words).most_common(20))
    return c_df

def emoji_count(selected_user,df):
    if selected_user != "Overall":
        df=df[df['user']==selected_user]

    emo = []
    for message in df['message']:
        emo.extend([c for c in message if emoji.is_emoji(c)])
    e_df = pd.DataFrame(Counter(emo).most_common(len(Counter(emo))), columns=['emoji', 'value'])

    return e_df
def month_year(selected_user,df):
    if selected_user != "Overall":
        df=df[df['user']==selected_user]
    new_df = df.groupby(['year',  'month']).count()['message'].reset_index()
    new_df['ym'] = new_df['year'].astype(str) + "-" + new_df['month'].astype(str)

    return new_df

def daily_time(selected_user,df):
    if selected_user != "Overall":
        df=df[df['user']==selected_user]
    dt_df = df.groupby(df['datetime'].dt.date).count()['message'].reset_index()
    return dt_df

def week_activity_map(selected_user,df):
    if selected_user != "Overall":
        df=df[df['user']==selected_user]
    busy_day=df['day_name'].value_counts().reset_index()
    busy_day.rename(columns={'day_name':'day'},inplace=True)
    return busy_day

def monthly_activity_map(selected_user,df):
    if selected_user != "Overall":
        df=df[df['user']==selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != "Overall":
        df=df[df['user']==selected_user]

    heat=df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return heat