import os.path

from flask import Flask, request
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import Resource
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']
app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    return "index"


def get_google_cloud_service() -> Resource:
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            """
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=5000)
            """
            pass    # handle exception

    with open('token.json', 'w') as token:
        token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
    except HttpError as error:
        print('An error occurred: %s' % error)

    return service


@app.route("/timesheet", methods=['POST'])
def timesheet() -> None:
    if hasattr(request, 'json'):
        print(request.json)

        if 'event' in request.json:
            # delete event
            if len(request.json) == 1:
                pass
            # create/update event
            else:
                service = get_google_cloud_service()
                # https://developers.google.com/calendar/api/v3/reference/events
                event = {
                    'summary': request.json['item']['project']['title'],
                    'start': {
                        'dateTime': request.json['item']['startDateTime'],
                        'timeZone': 'Asia/Seoul',
                    },
                    'end': {
                        'dateTime': request.json['item']['endDateTime'],
                        'timeZone': 'Asia/Seoul',
                    },
                    # TODO: URL join method
                    'source': (
                        'https://my.timesheet.io/tasks/show/'
                        + request.json['item']['id']
                    ),
                    'transparency': "transparent",
                    # 'description':
                }
                event = service.events().insert(
                    # TODO: to config
                    calendarId=(
                        'ivaaltu751ft6rlqkkb1viqqgs'
                        '@group.calendar.google.com'
                    ),
                    body=event,
                ).execute()
                print('Event created: %s' % (event.get('htmlLink')))

                return 'success'
    # return 'failure'
