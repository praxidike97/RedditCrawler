import configparser

import praw

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
#from email import E

from utils.invert_pdf import invert_color
from utils.NumberedCanvas import NumberedCanvas


def send_email():
    mail = MIMEMultipart()
    mail["SUBJECT"] = "NoSleep!"
    mail["TO"] = "fstern@uni-bremen.de"
    mail["FROM"] = "NoSleep!"

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open("./pdf_output/nosleep.pdf", "rb").read())
    #Encoders.encode_base64(part)

    part.add_header('Content-Disposition', 'attachment; filename="text.txt"')

    mail.attach(part)

    server = smtplib.SMTP("127.0.0.1")
    server.sendmail("NoSleep!", "fstern@uni-bremen.de", mail.as_string())


def get_parser():
    configParser = configparser.RawConfigParser()
    configFilePath = 'config.txt'
    configParser.read(configFilePath)

    credential_path = configParser.get('config', 'credential_path')

    credentialParser = configparser.RawConfigParser()
    credentialParser.read(credential_path)

    return configParser, credentialParser


def setup_reddit(client_id, client_secret):
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent='MyTestScript')
    return reddit


def create_pdf(reddit, subreddit="nosleep", limit=10, top="week", hot=False):
    # Set up new document
    doc = SimpleDocTemplate("./pdf_output/%s.pdf" % subreddit,
                            pagesize=letter,
                            rightMargin=72,
                            leftMargin=72,
                            topMargin=72,
                            bottomMargin=100)

    styles = getSampleStyleSheet()
    flowables = []

    # Define the style for titles
    styleTitle = ParagraphStyle(
        name='Normal',
        fontSize=18,
        leading=20
    )

    # Iterate over submissions
    if hot:
        submissions = reddit.subreddit(subreddit).hot(limit=limit)
    else:
        submissions = reddit.subreddit(subreddit).top(top, limit=limit)
    for submission in submissions:

        # Append title
        flowables.append(Paragraph(submission.title + "<br/><br/>", style=styleTitle))

        # Remove empty lines
        lines = submission.selftext.split("\n")
        lines = list(filter(lambda l: l != "", lines))

        # Add lines as paragraphs
        for line in lines:
            para = Paragraph(line + "<br/><br/>", style=styles["Normal"])
            flowables.append(para)

        # New page for each submission
        flowables.append(PageBreak())

    doc.build(flowables, canvasmaker=NumberedCanvas)


if __name__ == "__main__":
    configParser, credentialParser = get_parser()

    client_id = credentialParser.get('credentials', 'client_id')
    client_secret = credentialParser.get('credentials', 'client_secret')

    limit = int(configParser.get('config', 'limit'))
    dark_mode = bool(int(configParser.get('config', 'dark_mode')))
    top = configParser.get('config', 'top')
    hot = bool(int(configParser.get('config', 'hot')))
    subreddit = configParser.get('config', 'subreddit')

    reddit = setup_reddit(client_id=client_id, client_secret=client_secret)
    create_pdf(reddit, limit=limit, top=top, hot=hot, subreddit=subreddit)

    if dark_mode:
        invert_color("./pdf_output/%s.pdf" % subreddit)

    send_email()
