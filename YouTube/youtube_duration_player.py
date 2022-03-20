#!/usr/bin/python3

import re
import json
from pytube.innertube import InnerTube
from oauth2client.tools import argparser

def youtube_search_video(options):
  id=options.id
  innertube = InnerTube()
  video_info = innertube.player(id)

  duration = video_info["streamingData"]["formats"][0]["approxDurationMs"]
  # This video is embeddable?
  embeddable = video_info["playabilityStatus"]["playableInEmbed"]
  if not embeddable:
    print(-1)
    exit()
  else:
    print(int(duration)/1000)
    # print(embeddable)

if __name__ == "__main__":
  argparser.add_argument("--id", help="VideoIDs", default="Sq5QW3YqipM")
  args = argparser.parse_args()

  try:
    youtube_search_video(args)
  except HttpError as e:
    print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
