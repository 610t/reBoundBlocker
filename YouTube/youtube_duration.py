#!/usr/bin/python3

import re
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "MY_DEVELOPER_KEY"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_search_video(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    videos_response = youtube.videos().list(
        part="contentDetails,status",
        id=options.id
    ).execute()

#  videos = []

    for result in videos_response.get("items", []):
        duration = result["contentDetails"]["duration"]
        # This video is embeddable?
        embeddable = result["status"]["embeddable"]
        if not embeddable:
            print(-1)
            exit()
        pattern = r'PT(?:(?P<hours>\d+)H)?((?P<minutes>\d+)M)?(?P<seconds>\d+)S'
        match = re.match(pattern, duration)

        hours = int(match.group('hours') or 0)
        minutes = int(match.group('minutes') or 0)
        seconds = int(match.group('seconds') or 0)
#    print(duration, hours, minutes, seconds)
        print(60*60*hours+60*minutes+seconds)
#    videos.append("%s" % (duration))
#  print("\n".join(videos), "\n")


if __name__ == "__main__":
    argparser.add_argument("--id", help="VideoIDs", default="Sq5QW3YqipM")
    args = argparser.parse_args()

    try:
        youtube_search_video(args)
    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
