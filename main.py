import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pycountry
import os
import glob
import moviepy.editor as mpy

for filename in os.listdir("D:/Users/Kate/Data"):
    country_data = {}

    path = os.path.join('D:/Users/Kate/Data/', filename)
    with open(path, 'r', encoding='latin-1') as f:
        print(path)
        for line in f:
            try:
                data = json.loads(line)
                try:
                    for tweet in data["tweet_locations"]:
                        country_data[tweet["country_code"]] = country_data.setdefault(tweet["country_code"], 0) + 1
                except TypeError as e:
                    continue
            except json.JSONDecodeError as e:
                continue

    # Create pandas dataframe to store daily data
    df = pd.DataFrame.from_dict(country_data, orient='index', columns=['Amount of Tweets'])
    df['2 Digit'] = df.index
    li = []

    # Convert all 2-digit country codes to 3-digit codes so they can be plotted
    for item in df['2 Digit']:
        # Kosovo's country code doesn't convert so it must be done manually
        if item == 'xk':
            li.append('XKX')
        else:
            li.append(pycountry.countries.get(alpha_2=item.upper()).alpha_3)

    df['code'] = li
    df.set_index('code', inplace=True, drop=True)
    del df['2 Digit']

    # Create daily choropleth map
    fig = go.Figure(data=go.Choropleth(
        locations=df.index,
        z=np.log10((df['Amount of Tweets'].astype(float))),
        zmin=0,
        zmax=9,
        text=df['Amount of Tweets'],
        colorscale=px.colors.sequential.Reds,
        marker_line_color='white',
        marker_line_width=0.2
    ))

    month = filename.split(sep='-')[2]
    if month == '02': label = 'February'
    elif month == '03': label = 'March'
    else: label = 'April'

    fig.update_layout(
        title_text='Covid Twitter Mentions per Country',
        xaxis_title=label
    )

    fig.write_image(os.path.join('../images', filename.split(sep='.')[0] + '.png'))

# Create gif of all images
fps = 12
os.chdir("../images")
file_list = glob.glob('*.png')
print(file_list)
clip = mpy.ImageSequenceClip(file_list, fps=fps)
clip.write_gif('tweets.gif', fps=fps)
