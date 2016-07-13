import sys


def ask_execution_mode(config):
    print("What is the execution mode (once/scheduler):", end="", flush=True)
    config['ExecutionMode'] = sys.stdin.readline().strip('\n')
    if not (config['ExecutionMode'] == 'once' or config['ExecutionMode'] == 'scheduler'):
        print("Sorry, only once or scheduler values are allowed.")
        ask_execution_mode(config)


def ask_schedule_string(config):
    print("What is the schedule string for each recipient (please see example file for format):", end="", flush=True)
    config['ScheduleString'] = sys.stdin.readline().strip('\n')
    if len(config['ScheduleString']) == 0:
        print("Sorry, you need to provide a schedule string.")
        ask_schedule_string(config)


def ask_smtp_server(config):
    print("What is the SMTP server:", end="", flush=True)
    config['SMTPServer'] = sys.stdin.readline().strip('\n')
    if len(config['SMTPServer']) == 0:
        print("Sorry, you need to provide a valid smtp server.")
        ask_smtp_server(config)


def ask_smtp_port(config):
    print("What is the SMTP port:", end="", flush=True)
    config['SMTPPort'] = sys.stdin.readline().strip('\n')
    if len(config['SMTPPort']) == 0:
        print("Sorry, you need to provide a valid smtp port.")
        ask_smtp_port(config)


def ask_email_from(config):
    print("What is the EmailFrom:", end="", flush=True)
    config['EmailFrom'] = sys.stdin.readline().strip('\n')
    if len(config['EmailFrom']) == 0:
        print("Sorry, you need to provide a valid EmailFrom string.")
        ask_email_from(config)


def ask_email_to(config):
    print("What is the EmailTo:", end="", flush=True)
    config['EmailTo'] = sys.stdin.readline().strip('\n')
    if len(config['EmailTo']) == 0:
        print("Sorry, you need to provide a valid EmailTo string.")
        ask_email_from(config)


def ask_email_password(config):
    print("What is the EmailPassword:", end="", flush=True)
    config['EmailPassword'] = sys.stdin.readline().strip('\n')
    if len(config['EmailPassword']) == 0:
        print("Sorry, you need to provide a valid EmailPassword string.")
        ask_email_password(config)


def ask_email_user(config):
    print("What is the EmailUser:", end="", flush=True)
    config['EmailUser'] = sys.stdin.readline().strip('\n')
    if len(config['EmailUser']) == 0:
        print("Sorry, you need to provide a valid EmailUser string.")
        ask_email_user(config)


def write_config_file(config):
    f = open('bitstampconfig.py', 'w')
    f.write("def DefaultConfig():\n")
    f.write("    return {\n")
    f.write("        'ExecutionMode': '{0}',\n".format(config["ExecutionMode"]))
    if config['ExecutionMode'] == 'scheduler':
        f.write("        'ScheduleString': '{0}',\n".format(config["ScheduleString"]))
    f.write("        'SMTPServer': '{0}',\n".format(config["SMTPServer"]))
    f.write("        'SMTPPort': '{0}',\n".format(config["SMTPPort"]))
    f.write("        'EmailFrom': '{0}',\n".format(config["EmailFrom"]))
    if config['ExecutionMode'] == 'once':
        f.write("        'EmailTo': '{0}',\n".format(config["EmailTo"]))
    f.write("        'EmailPassword': '{0}',\n".format(config["EmailPassword"]))
    f.write("        'EmailUser': '{0}'\n".format(config["EmailUser"]))
    f.write("    }\n")
    f.close()
    print("bitstampconfig.py configuration file written...")


def config_writer():
    print("Welcome to the configuration generator for the bitstamp watcher script configuration writer")
    print("-------------------------------------------------------------------------------------------")
    config = {}
    ask_execution_mode(config)
    if config['ExecutionMode'] == 'scheduler':
        ask_schedule_string(config)
    ask_smtp_server(config)
    ask_smtp_port(config)
    ask_email_from(config)
    if config['ExecutionMode'] == 'once':
        ask_email_to(config)
    ask_email_password(config)
    ask_email_user(config)
    write_config_file(config)
