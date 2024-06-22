import streamlit as st
import preprocessor, helper  # Importing necessary modules
import matplotlib.pyplot as plt
import seaborn as sns

# Setting up the sidebar title
st.sidebar.title("Whatsapp Analysis")

# File upload functionality
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)  # Preprocessing the uploaded data

    # Fetch unique users from preprocessed data
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0, "Overall")  # Adding 'Overall' option to user list

    # Selectbox for choosing user for analysis
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    # Button to trigger analysis
    if st.sidebar.button("Show Analysis"):
        # Fetching statistics using helper functions
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

        # Displaying top statistics
        st.markdown("""
            <style>
            .stat-box {
                display: flex;
                justify-content: space-around;
                margin: 20px 0;
            }
            .stat-item {
                text-align: center;
                border: 1px solid #ddd;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                width: 20%;
            }
            .stat-item h1 {
                font-size: 24px;
                margin-bottom: 10px;
            }
            </style>
            """, unsafe_allow_html=True)

        st.markdown("<h1 style='text-align: center;'>Top Statistics</h1>", unsafe_allow_html=True)

        st.markdown("""
            <div class="stat-box">
                <div class="stat-item">
                    <h1>Total Messages</h1>
                    <h2>{}</h2>
                </div>
                <div class="stat-item">
                    <h1>Words Count</h1>
                    <h2>{}</h2>
                </div>
                <div class="stat-item">
                    <h1>Media Shared</h1>
                    <h2>{}</h2>
                </div>
                <div class="stat-item">
                    <h1>Links Shared</h1>
                    <h2>{}</h2>
                </div>
            </div>
            """.format(num_messages, words, num_media_messages, num_links), unsafe_allow_html=True)


        # # Displaying top statistics
        # st.markdown("<h1 style='text-align: center;'>Top Statistics</h1>", unsafe_allow_html=True)
        # col1, col2, col3, col4 = st.columns(4)
        #
        # with col1:
        #     st.header("Total Messages")
        #     st.title(num_messages)
        # with col2:
        #     st.header("Words Count")
        #     st.title(words)
        # with col3:
        #     st.header("Media Shared")
        #     st.title(num_media_messages)
        # with col4:
        #     st.header("Links Shared")
        #     st.title(num_links)

        # Monthly timeline analysis
        st.markdown("<h1 style='text-align: center;'>Monthly Timeline</h1>", unsafe_allow_html=True)
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily timeline analysis
        st.markdown("<h1 style='text-align: center;'>Daily Timeline</h1>", unsafe_allow_html=True)
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity map section
        st.markdown("<h1 style='text-align: center;'>Activity Map</h1>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<h1 style='text-align: center;'>Most Busy Day</h1>", unsafe_allow_html=True)
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.markdown("<h1 style='text-align: center;'>Most Busy Month</h1>", unsafe_allow_html=True)
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Weekly activity heatmap
        st.markdown("<h1 style='text-align: center;'>Weekly Activity Map</h1>", unsafe_allow_html=True)
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # Busiest users analysis (if 'Overall' is selected)
        if selected_user == "Overall":
            st.markdown("<h1 style='text-align: center;'>Most Busy Users</h1>", unsafe_allow_html=True)
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation=90)
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df, use_container_width=True)  # Displaying percentage use in a DataFrame

        # Wordcloud visualization
        st.markdown("<h1 style='text-align: center;'>Wordcloud</h1>", unsafe_allow_html=True)
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Most common words analysis
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1], color='blue')
        plt.xticks(rotation=90)
        st.markdown("<h1 style='text-align: center;'>Most Common Words</h1>", unsafe_allow_html=True)
        st.pyplot(fig)

        # Emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.markdown("<h1 style='text-align: center;'>Emoji Analysis</h1>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)  # Displaying emoji DataFrame

        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)  # Displaying emoji pie chart
