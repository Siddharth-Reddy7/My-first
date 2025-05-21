import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import seaborn as sns



st.sidebar.title("Whatsapp Chat Analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocessor(data)

    #fetch unique users
    user_list=df['user'].unique().tolist()
    user_list.remove("Group Notification")
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user=st.sidebar.selectbox("Show analysis wrt ",user_list)

    if st.sidebar.button("show analysis"):
        st.title("Top Statistics")



        num_messages,total_words,num_media,num_links=helper.fetch_stat(selected_user,df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)


        with col2:
            st.header("Total Words")
            st.title(total_words)


        with col3:
            st.header("Media Shared")
            st.title(num_media)

        with col4:
            st.header("Links Shared")
            st.title(num_links)

            # month_year_messages
        new_df = helper.month_year(selected_user, df)
        st.title("Monthly timeline")
        fig, ax = plt.subplots()
        ax.plot(new_df['ym'], new_df['message'],color='green')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # daily_timelinemessages
        new_df = helper.daily_time(selected_user, df)
        st.title("Daily timeline")
        fig, ax = plt.subplots()
        ax.plot(new_df['datetime'], new_df['message'], color='black')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # week_timelinemessages

        st.title("Activity map")
        col1,col2 = st.columns(2)
        with col1:
            busy_day = helper.week_activity_map(selected_user, df)
            st.title("Most Busy day")
            fig, ax = plt.subplots()
            ax.bar(busy_day['day'],busy_day['count'])
            plt.xticks(rotation=90)
            st.pyplot(fig)

        with col2:
            busy_month = helper.monthly_activity_map(selected_user, df)
            st.title("Most Busy month")
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation=90)
            st.pyplot(fig)





        if selected_user=="Overall":
            st.title("Most Busy users ")
            x,n_df=helper.fetch_buzy_users(df)



            col1, col2 = st.columns(2)

            with col1:
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation=90)
                st.pyplot(fig)
            with col2:
                st.dataframe(n_df)

        df_wc=helper.word_cloud(selected_user,df)
        st.title("Word Cloud")
        fig,ax =plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_c_df = helper.most_common_words(selected_user, df)
        st.title("Most Common Words")
        fig, ax = plt.subplots()
        ax.barh(most_c_df[0], most_c_df[1])
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # emoji
        e_df = helper.emoji_count(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(e_df, width=200)

        with col2:
            fig = px.pie(e_df, names='emoji', values='value', title='Pie Chart')

            st.plotly_chart(fig)
        st.bar_chart(e_df.head(7), x='emoji', y='value')

        st.title("Weekly activity map")
        heat = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        sns.heatmap(heat, ax=ax)
        st.pyplot(fig)















