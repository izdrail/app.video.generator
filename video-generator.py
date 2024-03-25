import gtts
import csv
from moviepy.editor import *
import gizeh as gz
from math import pi
import os
import requests
import json

VIDEO_SIZE = (1920, 1080)
BLUE = (59 / 255, 89 / 255, 152 / 255)
GREEN = (176 / 255, 210 / 255, 63 / 255)
WHITE = (255, 255, 255)
WHITE_GIZEH = (1, 1, 1)
SB_LOGO_PATH = './assets/logo.jpg'
DURATION = 10


def draw_stars(t):
    surface = gz.Surface(640, 120, bg_color=WHITE_GIZEH)
    for i in range(5):
        star = gz.star(
            nbranches=5, radius=120 * 0.2, ratio=0.5,
            xy=[100 * (i + 1), 50], fill=GREEN, angle=t * pi)
        star.draw(surface)
    return surface.get_npimage()


#

news_url = 'https://newsapi.org/v2/top-headlines?apiKey=API_KEY&category=entertainment&country=gb'
r = requests.get(news_url)
data = r.json()
json_object = json.dumps(data)
x = json.loads(json_object)
for x in x['articles']:
    filename = x['title']

    audioText = x['title'] + '.' + x['content']

    print(audioText)

    # save a remote image

    # generate and save audio
    tts = gtts.gTTS(audioText, lang='en', tld='co.uk')
    tts.save(filename + '.mp3')

    audioclip = AudioFileClip(filename + '.mp3')
    new_audioclip = CompositeAudioClip([audioclip])

    # Generate the text
    text = TextClip(audioText, fontsize=18, font='Amiri-Bold')

    sb_logo = ImageClip(SB_LOGO_PATH).set_position(('center', 0)).resize(width=200)
    stars = VideoClip(draw_stars, duration=DURATION)

    video = CompositeVideoClip(
        [
            sb_logo,
            text.set_position(
                ('center', text.size[1])),
            stars.set_position(
                ('center', sb_logo.size[1] + text.size[1])
            )
        ],
        size=VIDEO_SIZE). \
        on_color(
        color=WHITE,
        col_opacity=1).set_duration(DURATION)
    video.audio = new_audioclip
    video.write_videofile('generated/' + filename + '.mp4', fps=10)
    os.remove(filename + '.mp3')
