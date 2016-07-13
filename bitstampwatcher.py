"""

This is the main script for the bitstamp quote fetcher, it fetches the quote and then send an email with it.
Please, check the bitstampconfig file with the correct keys to configure the functionality below

"""
import ast
import copy
import bitstamp.client
import smtplib

from email.mime.text import MIMEText
from bitstampconfig import DefaultConfig
from sys import exit, argv
from bitstampconfigwriter import config_writer
from apscheduler.schedulers.blocking import BlockingScheduler
from ast import literal_eval as make_tuple


def execute_fetch():
    """
    This function executes the fetch from bitstamp api of the current quote.
    :return: A ticker object from the bitstamp API as seen in https://www.bitstamp.net/api/
    """
    return bitstamp.client.Public().ticker()


def format_email_subject(quote):
    """
    This functions formats the subject field of the email to be send to the user as configured in bitstampconfig.py
    :param quote: The current quote values to be inserted on the subject of the email
    :return: the email subject to be sent with the current quote
    """
    return 'Bitstamp Last Quote: {0} USD'.format(quote['last'])


def format_email_body(quote):
    """
    The Email Body containing all quote information from bitstamp
    :param quote: The current quote values to be inserted on the body of the email
    :return: the email body to be sent with the current quote
    """
    return ("""
            Bitstamp Current: {0} USD
            Bitstamp Open   : {1} USD (Last 24 hours)
            Bitstamp High   : {2} USD (Last 24 hours)
            Bitstamp Low    : {3} USD (Last 24 hours)
            Bitstamp Close  : {4} USD (Last 24 hours)
            Bitstamp Volume : {5} BTC (Last 24 hours)
            """.format(quote['last'], quote['open'], quote['high'], quote['low'], quote['last'], quote['volume']))


def send_email(quote, smtp_server, smtp_port, email_from, email_to, email_user, email_password):
    """
    This function sends a email with the quote from the bitstamp api
    :param quote: The Quote to be sent
    :param smtp_server: The SMTP Server to use
    :param smtp_port: The SMTP Port to use
    :param email_from: The Email from to be used
    :param email_to: The Email To to be used
    :param email_user: The SMTP User on the SMTP Server that will send the email
    :param email_password: The SMTP User's password on the SMTP Server that will send the email
    :return:
    """
    serv = smtplib.SMTP(smtp_server, smtp_port)
    msg = MIMEText('%s' % format_email_body(quote))
    msg['Subject'] = format_email_subject(quote)
    msg['From'] = email_from
    msg['To'] = email_to
    serv.ehlo()
    serv.starttls()
    serv.login(email_user, email_password)
    serv.sendmail(msg['From'], msg['To'], msg.as_string())
    serv.quit()


def send_single_quote(config):
    """
    This function fetches and send a single quote from bitstamp to the configured email specified on the config param
    :param config: A Dictionary with all configuration keys from bitstampconfig.py
    :return: None
    """
    quote = execute_fetch()
    print("Obtained quote:{0} USD".format(quote['last']))
    send_email(quote, config['SMTPServer'],
               config['SMTPPort'],
               config['EmailFrom'],
               config['EmailTo'],
               config['EmailUser'],
               config['EmailPassword'])
    print("Quote sent to {0}".format(config['EmailTo']))


class job_to_execute:
    """
    A simple class to wrap the job parameters and recipients, as the scheduler add_job method requires as
    first parameter a callable (either a function or a class with __class__ method implement.
    This class will encapsulate the information required to run this single job.
    """

    def __init__(self, config_to_use, recipients):
        """ Instance Constructor """
        self.config = copy.deepcopy(config)  # Perform a clone of the dictionary
        self.config['EmailTo'] = recipients  # Make sure that the specific recipients of the job are set.

    def __call__(self):
        """ With the config dictionary encapsulated on the class instance, it sends a single quote to the recipients. """
        send_single_quote(self.config)


def start_schedule_jobs(config, jobs_to_execute):
    """
    This function loops for each tuple on the jobs_to_execute tuple in order to create a job_to_execute class instance and then
    set this instance as the callable function for the apscheduler job, it also parses the scheduling parameters from the tuple from
    string to function arguments to configure the job schedule.

    If the jobs_to_execute is only a single tuple of strings, then just add one job.

    For information regarding the valid schedule parameters, please see:
    For Cron mode: http://apscheduler.readthedocs.io/en/3.0/modules/triggers/cron.html#module-apscheduler.triggers.cron
    For Interval mode: http://apscheduler.readthedocs.io/en/3.0/modules/triggers/cron.html#module-apscheduler.triggers.cron

    :param config: The dictionary containing the configuration keys used to send the email
    :param jobs_to_execute: The Tuple containing the jobs descriptions to run
    :return: None
    """
    sched = BlockingScheduler()
    # Check if our first member is a tuple itself
    if isinstance(jobs_to_execute[0], tuple):
        for current_job in jobs_to_execute:
            start_job(sched, current_job[0], current_job[1], current_job[2])
    else:
        start_job(sched, jobs_to_execute[0], jobs_to_execute[1], jobs_to_execute[2])
    sched.start()


def start_job(sched, recipients, type_schedule, schedule_string):
    current_job_to_use = job_to_execute(config, recipients)
    args = ast.literal_eval("{" + schedule_string + "}")
    print("Created a job to send quotes to:'{0}' using '{1}' scheduler with args:'{2}'".format(recipients,
                                                                                               type_schedule,
                                                                                               schedule_string))
    sched.add_job(current_job_to_use, type_schedule, **args)


def parse_command_line():
    """
    This function parses the command line arguments and execute functions according to the arguments passed.
    If there is no argument, it simply reads the DefaultConfig and returns the dictionary with the configuration keys.
    If the argument is config, it opens a questionnaire to automatically create the bitstampconfig.py file that contains the default configuration.
    If the argument is a python tuple, it assumes that we need to run the script on scheduler mode and use this tuple to configure the script
    If the argument is a simple string, it assumes that it is the recipients string and that the script should be set to once mode.

    :return: A config dictionary containing all the correct keys to the script, or exit the script after writing the bitstampconfig.py file
    """
    if len(argv) == 1:
        return DefaultConfig()
    if argv[1] == 'config':
        config_writer()
        exit(0)
    else:
        config = DefaultConfig()
        try:
            config['ExecutionMode'] = "scheduler"
            config['ScheduleString'] = make_tuple(argv[1])
        except ValueError:
            config['ExecutionMode'] = "once"
            config['EmailTo'] = argv[1]
        return config


if __name__ == "__main__":
    config = parse_command_line()
    if config['ExecutionMode'] == 'once':
        send_single_quote(config)
        exit(0)
    if config['ExecutionMode'] == 'scheduler':
        start_schedule_jobs(config, config['ScheduleString'])
    exit("Invalid ExecutionMode")
