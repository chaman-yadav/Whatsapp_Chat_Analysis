import re
import pandas as pd
from datetime import datetime

# Function to convert date and 12-hour time format to 24-hour time format with a 4-digit year
def convert_to_24hr(date_str, time_str):
    """Convert date and 12-hour time format to 24-hour time format with a 4-digit year."""
    datetime_str = f"{date_str} {time_str}"
    datetime_str = re.sub(r'\s+', '', datetime_str)  # Remove any extra spaces
    in_datetime = datetime.strptime(datetime_str, '%d/%m/%Y%I:%M%p')  # Parse input datetime
    out_datetime = datetime.strftime(in_datetime, '%d/%m/%Y %H:%M')  # Format output datetime
    return out_datetime

# Function to preprocess WhatsApp chat data into a structured DataFrame
def preprocess(data):
    dates = []
    usernames = []
    messages = []
    pattern = r'(\d{2}/\d{2}/\d{4}), (\d{1,2}:\d{2}\s*[ap]m) - ([^:]+): (.+?)(?=\d{2}/\d{2}/\d{4}, \d{1,2}:\d{2}\s*[ap]m - |$)'
    matches = re.findall(pattern, data, re.DOTALL)

    # Extracting data from matches
    for match in matches:
        date, time, sender, message = match
        cleaned_datetime = convert_to_24hr(date, time)
        dates.append(cleaned_datetime)

        # Extracting username or number from sender
        if ':' in sender:
            sender_name = sender.split(':', 1)[0].strip()
        else:
            sender_name = sender.strip()

        usernames.append(sender_name)
        messages.append(message)

    # Creating a DataFrame from extracted data
    df = pd.DataFrame({
        'date': dates,
        'user': usernames,
        'message': messages
    })

    # Converting 'date' column to datetime format
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y %H:%M')

    # Extracting additional datetime features
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Determining periods based on hour for analysis
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period  # Assigning periods to DataFrame

    return df  # Returning preprocessed DataFrame
