# Covid-Tweets

This project was created using the Crisis-NLP Covid Tweets dataset. The visualization shows the volume of twitter mentions
per country as the pandemic progressed from February to April 2020. 

Because the data was in the form of individual JSON objects, the data from each day had to be treated
as a stream and evaluated per object. Each frame represents one day. The graph was made using
pyplot's Chloropleth class with a logarithmic scale for the color bar.  The final result is below:

![](tweets.gif)
