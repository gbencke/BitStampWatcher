
#Installation

1. Please install Python 3.5 (It will not work with Python 2)
2. Open a command prompt and type:
~~~~
pip install BitStampClient apscheduler
~~~~
3. Use the auto-configuration to configure and create the bitstampconfig.py file, please see the example below for clarification 
~~~~
python bitstampwatcher.py config
~~~~
4. Open a terminal and execute:
~~~~
python bitstampwatcher.py
~~~~

#Configuration File Example:
The configuration file is a regular python file that has a single function that returns a dictionary with the configuration keys:
~~~~
def DefaultConfig():
    """
    This is the default configuration for the script. Each key on the dictionay returned sets a different functionality.

    It contains the following keys:

    ExecutionMode: 'once' for a single execution, 'scheduler' for execution with a scheduler

    ScheduleString: When using the scheduler, it contains the string containing the tuples for recipients and schedules for exemplo:

    (("gbencke@gmail.com,teste@gmail.com","interval","1 hour"),("mail@gbencke.com","cron","day_of_week='mon-fri', hour=17"))

    As seen in the example above we have a job to send every 1 hour the quotes and another to send every mon-fri @ 5 PM

    The parameters that can be used on the cron mode are described in:
    http://apscheduler.readthedocs.io/en/3.0/modules/triggers/cron.html#module-apscheduler.triggers.cron

    The parameters that can be used on the interval mode are described in:
    http://apscheduler.readthedocs.io/en/3.0/modules/triggers/interval.html#module-apscheduler.triggers.interval

    STMPServer: The SMTP server to use

    SMTPPort: The port of the SMTP server to use

    EmailFrom: The From email address to appear on the email message

    EmailTo: The recipients of the email message in case of a "once" mode, this is ignored in "scheduler" mode

    EmailPassword: The password of the user on the SMTP Server

    EmailUser: The user on the SMTP Server

    :return: A Dictionary with all configuration keys above.

    """
    return {
        'ExecutionMode': 'scheduler',
        'ScheduleMode': 'MoTuWeThFrSaSu',
        'ScheduleString': 1,
        'SMTPServer': 'smtp.somewhere.com.br',
        'SMTPPort': '587',
        'EmailFrom': 'ignite@somewhere.com.br',
        'EmailTo': 'gbencke@gmail.com',
        'EmailPassword': 'somepassword',
        'EmailUser': 'someone@somewhere.com'
    }
~~~~

#Remarks
* The script work both on 'scheduler' or 'once' mode.
* In once mode, it will send a quote to a certain address and then end execution
* In scheduler mode, it can either send a email at a certain interval or at a certain cron schedule.