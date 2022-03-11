#!/usr/bin/env python3
import os
import time
import random
import subprocess

path=os.path.dirname(__file__)

movie_list=[]

video_file="video_list.txt"
with open(path+"/"+video_file) as vf:
  for l in vf:
    l=l.strip()
    # Skip line start from '#' as a comment.
    if l.find("#") != 0:
      movie_list.append(l)

# Set video randomly.
v=random.randint(0,len(movie_list)-1)
url="https://www.youtube.com/embed/"+movie_list[v]

tmpl_file=path+"/iframe.html.tmpl"
output_file=path+"/iframe.html"

### Get movie duration from script ../YouTube/youtube_duration.py.
# Please see a code at RasPiCon2018 at ~/pychromecast/examples/my_youtube.py.
duration=int(subprocess.check_output(path+"/../YouTube/youtube_duration.py --id "+movie_list[v], shell=True))
# The constant 5 seconds means the video playback start time.
duration=int((duration+5)*1.1)

print("Movie ID:"+movie_list[v])
print("Duration:"+str(duration))

with open(tmpl_file) as f_tmpl:
  tmpl=f_tmpl.read()
  tmp=tmpl.replace('%%%URL%%%',url)
  out=tmp.replace('%%%TIME%%%',str(duration))
  with open(output_file, mode='w') as f_out:
    f_out.write(out)

time.sleep(5)

# Open browser on new window.
subprocess.run(path+"/../bin/create_new_browser.sh "+path+"/iframe.html", shell=True)
time.sleep(duration)
