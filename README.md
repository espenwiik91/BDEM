Read me for "The System".

The python program has been written and tested in and for python 3.7.X. Running tweepy in python
3.7 will cause compatibility issues. The spark version used and tested is
Spark-2.3.2-bin-hadoop2.7.

PS: To solve the compabilities issues with python
3.7, rename all the async parameters in streaming.py
file in python 3.7 to _async. 

BUT we would recommend the user to use python 3.6.X to avoid all compatibility issues.

To run this system you need to import a number of python libraries
into your run-time environment(f.ex. terminal).

This is the complete list:
collections
nltk
pyspark
tweepy
pandas
matplotlib
numpy
os
re
sys
csv
logging

Some are included in the standard python library, others need to be downloaded.
The easiest way is through the "pip install NAMEOFMODULE" command.

After you have all the correct modules you need to run the app.py file.
(ex. in terminal):
>python app.py

Follow the instructions given in the terminal and it should work, given that spark runs correctly. If any modules are 
missing, you will get an error message describing the missing module. Download and run again.
If Spark is unable to load, check the necessary environment variables and use the error codes to search 
for fixes online. 

DEFAULT: When app.py is run, a main function drives the program. This program includes a sample csv file with
tweets that can be used to run the program with all its functions. 

TO TWEAK DATASET: If the user wants to test the code for collecting tweets, follow the instructions
for collecting tweets in the main function, line 109 to 116 in app.py.
When collecting data, the running of app.py must be stopped at some point. Please allow the process
to run for at least 15 minutes to have a sufficient amount of data for analysis.
When collecting is finished, re-comment the lines that were uncommented(add # before line).

For program testing purposes, default is recommended. 