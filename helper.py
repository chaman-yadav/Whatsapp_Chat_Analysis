from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

# Function to fetch statistics based on selected user
def fetch_stats(selected_user, df):
    # Filter DataFrame if selected_user is not 'Overall'
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Calculate various statistics
    num_messages = df.shape[0]  # Number of messages
    words = [word for message in df['message'] for word in message.split()]  # Total words
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]  # Number of media messages
    extractor = URLExtract()
    links = [link for message in df['message'] for link in extractor.find_urls(message)]  # Extracted links

    return num_messages, len(words), num_media_messages, len(links)

# Function to find the most active users
def most_busy_users(df):
    x = df['user'].value_counts().head()  # Top users by message count
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})  # Percentage of messages per user
    return x, df

# Function to create a word cloud for messages
def create_wordcloud(selected_user, df):
    f = open('stop_hinglish.txt', 'r')  # Open stop words file
    stop_words = f.read()  # Read stop words
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]  # Filter by selected_user

    # Filter out non-user and media messages
    temp = df[df['user'] != 'group_notifications']
    temp = temp[temp['message'] != '<Media omitted>\n']

    # Nested function to remove stop words from messages
    def remove_stop_words(message):
        return " ".join([word for word in message.lower().split() if word not in stop_words])

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))  # Generate word cloud

    return df_wc

# Function to find most common words
def most_common_words(selected_user, df):
    f = open('stop_hinglish.txt', 'r')  # Open stop words file
    stop_words = f.read()  # Read stop words
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]  # Filter by selected_user

    # Filter out non-user and media messages
    temp = df[df['user'] != 'group_notifications']
    temp = temp[temp['message'] != '<Media omitted>\n']

    # Extract and count words, excluding stop words
    words = [word for message in temp['message'] for word in message.lower().split() if word not in stop_words]
    most_common_df = pd.DataFrame(Counter(words).most_common(20))  # Top 20 most common words

    return most_common_df

# Function to extract emojis and their frequencies
def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]  # Filter by selected_user

    # Extract emojis from messages
    emojis = [c for message in df['message'] for c in message if c in emoji.EMOJI_DATA]
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))  # Count emoji occurrences

    return emoji_df

# Function to create a monthly message timeline
def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]  # Filter by selected_user

    # Group messages by year and month, count messages
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    # Format month and year into a readable format
    timeline['time'] = timeline.apply(lambda row: f"{row['month']}-{row['year']}", axis=1)

    return timeline

# Function to create a daily message timeline
def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]  # Filter by selected_user

    # Group messages by date, count messages
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

# Function to map weekly activity
def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]  # Filter by selected_user

    # Count messages by day name
    return df['day_name'].value_counts()

# Function to map monthly activity
def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]  # Filter by selected_user

    # Count messages by month
    return df['month'].value_counts()

# Function to create an activity heatmap
def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]  # Filter by selected_user

    # Pivot table to show message counts by day and period
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap
