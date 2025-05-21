import pandas as pd
import re
def preprocessor(data):
    patern = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s"

    messages = re.split(patern, data)[1:]
    dates = re.findall(patern, data)

    df = pd.DataFrame({"User_msg": messages, 'msg_date': dates})
    df['datetime'] = pd.to_datetime(df['msg_date'], format="%d/%m/%Y, %H:%M - ")

    df['User_msg'] = df['User_msg'].apply(lambda x: x.rstrip("\n"))

    users = []
    mess = []
    for message in df['User_msg']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            mess.append(entry[2])
        else:
            users.append("Group Notification")
            mess.append(entry[0])
    df['user'] = users
    df['message'] = mess

    df.drop(columns=['User_msg'], inplace=True)
    df.drop(columns=['msg_date'], inplace=True)
    df['day'] = df['datetime'].dt.day
    df["month"] = df['datetime'].dt.month_name()
    df['year'] = df['datetime'].dt.year
    df['hour'] = df['datetime'].dt.hour
    df["minute"] = df['datetime'].dt.minute
    df["day_name"]=df['datetime'].dt.day_name()
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str("00"))
        elif hour == 00:
            period.append(str(00) + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period

    return df







