
#Installation

1. Please install Python 3.5 (It should work with 2.7 as well)
2. Open a command prompt and type:
~~~~
pip install BitStampClient
~~~~
3. Configure the information on the config dictionary on:
~~~~
bitstampconfig.py
~~~~
4. Open a terminal and execute:
~~~~
python  bitstampwatcher.py
~~~~

#Remarks
* The script work both on 'loop' or 'once' mode.
* In loop mode, it will send a email at a each certain amount of minutes
* You can also configure to only send email at certain days of the week