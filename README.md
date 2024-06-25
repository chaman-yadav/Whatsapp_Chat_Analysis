# WhatsApp Chat Analyzer

## Overview

WhatsApp Chat Analyzer is a Streamlit application that allows users to upload their WhatsApp chat data and gain various insights through statistical analysis and visualizations. The application processes the chat data to provide insights such as the most active users, common words used, activity heatmaps, and more.

Click on the link below to access the deployed app:
<a href="https://whatsappchatanalysis777.streamlit.app/" target="_blank">https://whatsappchatanalysis777.streamlit.app/</a>


If the link does not load properly due to a server error or streamlit cloud error, click on the URL and search it again, or just type the URL:
You have to upload your WhatsApp chat history of either an individual or a group and then click on analysis then you can see various statistics of that group.


## Features

- **Preprocessing of WhatsApp Chat Data**: Converts date and time formats, extracts relevant data, and structures it into a DataFrame.
- **User Statistics**: Provides statistics like the total number of messages, word count, media messages, and links shared.
- **Timeline Analysis**: Displays monthly and daily timelines of message activity.
- **Activity Maps**: Shows the most active days and months.
- **Heatmaps**: Displays user activity heatmaps based on the day and time.
- **User Analysis**: Identifies the most active users in the chat.
- **Word Cloud**: Generates a word cloud of the most common words used.
- **Emoji Analysis**: Displays the most frequently used emojis.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/whatsapp-chat-analyzer.git
    cd whatsapp-chat-analyzer
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Export your WhatsApp chat history (group or individual) in `.txt` format.
2. Run the Streamlit app:
    ```sh
    streamlit run app.py
    ```

3. Upload your WhatsApp chat export file using the sidebar.

4. Select a user to analyze or choose "Overall" for general statistics.

5. Click on "Show Analysis" to generate insights and visualizations.

## Run the Deployed App on Streamlit

You can also run the app directly from the web without setting it up locally. Click the link below to access the deployed app:

<a href="https://whatsappchatanalysis777.streamlit.app/" target="_blank">https://whatsappchatanalysis777.streamlit.app/</a>

If the link does not load properly due to a server error, click on the URL and search it again or just type the URL:





## File Descriptions

### preprocessor.py

Contains functions to preprocess the WhatsApp chat data:

- **convert_to_24hr**: Converts date and 12-hour time format to 24-hour time format.
- **preprocess**: Preprocesses chat data to extract dates, usernames, messages, and additional datetime features, and returns a structured DataFrame.

### app.py

The main application file that uses Streamlit to build the UI and display the analysis:

- Uploads and processes the chat data.
- Displays statistics and visualizations using helper functions.
- Utilizes Matplotlib and Seaborn for plotting graphs.

### helper.py

Contains various helper functions to perform specific analyses and generate visualizations:

- **fetch_stats**: Fetches statistics like the number of messages, words, media messages, and links.
- **most_busy_users**: Identifies the most active users.
- **create_wordcloud**: Generates a word cloud of the most common words.
- **most_common_words**: Finds the most common words used in the chat.
- **emoji_helper**: Analyzes the usage of emojis.
- **monthly_timeline**: Creates a monthly message timeline.
- **daily_timeline**: Creates a daily message timeline.
- **week_activity_map**: Maps weekly activity.
- **month_activity_map**: Maps monthly activity.
- **activity_heatmap**: Creates an activity heatmap.

### requirements.txt

Lists all the required Python packages:

- streamlit
- matplotlib
- seaborn
- urlextract
- wordcloud
- pandas
- emoji
- datetime
- collections

## Example



