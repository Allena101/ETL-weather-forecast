# ETL-weather-forecast

Here is my pipeline for the ETL assignment
by Magnus Jensen

1) To use , run main.py

Here are some issues and thoughts relevant to the project:

2) i realized that i might not be getting the correct precipitation parameter from the json, so that might is something i would have liked to noticed sooner...
3) I wanted to include data validation, but i am unsure that i actually works, and converting to float prior to pandera checking might be doing things in the wrong order.
4) i realized later that it was a bad idea to format validTime before saving it since i meant i had to format more when loading in the files later. should have just saved either the time zone default value or the dateTime object converted to normal dateTime
5) I tried to include a logger, which works fairly well, but i did not manage to figure out why more than one file is created each run.
6) tried a custom exceptions class but that just did not work...
7) Some things are not done as efficiently as they could, but some of it has to do with simulating a reasonable ETL scenario where you cannot convert files directly since you might want to extract data from several databases before combining and transforming the data into your working data.
8) The imports are redundant in many places. such as datetime.now() being run several times.
9) i made an optional python scheduler, but i know its not airFlow. If you dont run the file manually to start it you have to put the script in the windows start up folder
10) The plotting did not turn out well at all. I wasted a lot of time and it still looks really bad. Only temperature was suitable to be plotted the way that all of the features beside air pressure are plotted now.  Should have included just 24 hours plotting for all features. I also messed nested loops all the time so i decided to run them after each other i.e. more a a hard coded approach (and less skilled). I know that -9 means missing value, but i could not decide if i should plot something else (e.g. just first day) or do some kind of analysis on it. Since there was no ML goal i was unsure what to do. At least in the graphs, when you see that it is minus, you know its missing data.
11) I included an airflow script, but i have not managed to get airflow working with WSL so i cannot confirm that it is working. And, as you know, you cannot run airflow in windows. I might try to test the script later when i got airflow working :)
12) I did not understand if this was a requirement or not, but i save the data to a local psql server. I got my password in the ini file as we have been taught so you have to add your own in that place. I know i should not upload mine, but since it is just a local password i dont think there is any security risk...
13) i got a feeling that i might have missed something that i should done, besides airflow support.
14) overall i am unsatisfied with the project since most advanced things i tried , did not turn out good and i got stuck alot...

