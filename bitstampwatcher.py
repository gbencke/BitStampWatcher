"""

This is the main script for the bitstamp quote fetcher, it fetches the quote and then send an email with it.
Please, check the bitstampconfig file with the correct keys to configure the functionality below

"""


import bitstamp.client
import smtplib
import time
import datetime
from email.mime.text import MIMEText
from bitstampconfig import DefaultConfig
from sys import exit


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


def should_we_send_today(config):
    """

    This function checks in the configuration Dictionary if we should or not send the quote today

    :param config: Dictionary that contains the configuration keys for the application, including the DaysOfWeek that configure
     the days of the week that we should send the quotes
    :return: Return True if it is ok to send, or False if it is not.
    """
    weekday = datetime.datetime.today().weekday()
    if weekday == 0 and 'Mo' in config['DaysOfWeek']:
        return True
    if weekday == 1 and 'Tu' in config['DaysOfWeek']:
        return True
    if weekday == 2 and 'We' in config['DaysOfWeek']:
        return True
    if weekday == 3 and 'Th' in config['DaysOfWeek']:
        return True
    if weekday == 4 and 'Fr' in config['DaysOfWeek']:
        return True
    if weekday == 5 and 'Sa' in config['DaysOfWeek']:
        return True
    if weekday == 6 and 'Su' in config['DaysOfWeek']:
        return True
    return False


def loop_quote_fetch(config):
    """
    This function loops every N Minutes and then fetch and send a single quote
    from bitstamp to the configured email specified on the config param
    :param config: A Dictionary with all configuration keys from bitstampconfig.py
    :return: None
    """
    while True:
        if should_we_send_today(config):
            send_single_quote(config)
            print("Will Sleep {0} Minutes".format(config['LoopIntervalMinutes']))
        time.sleep(config['LoopIntervalMinutes'] * 60)


if __name__ == "__main__":
    config = DefaultConfig()
    if config['ExecutionMode'] == 'once':
        send_single_quote(config)
        exit(0)
    if config['ExecutionMode'] == 'loop':
        loop_quote_fetch(config)
        exit(0)
    exit("Error, invalid Execution Mode, only 'once' or 'loop' is supported")
