import gtts
import csv 
from moviepy.editor import *
import gizeh as gz
from math import pi
import os




VIDEO_SIZE = (640, 480)
BLUE = (59/255, 89/255, 152/255)
GREEN = (176/255, 210/255, 63/255)
WHITE = (255, 255, 255)
WHITE_GIZEH = (1, 1, 1)
SB_LOGO_PATH = './assets/logo.png'
DURATION = 10

def render_text(t):
    surface = gz.Surface(640, 60, bg_color=WHITE_GIZEH)
    text = gz.text(
        "Let's build together", fontfamily="Charter",
        fontsize=30, fontweight='bold', fill=BLUE, xy=(320, 40))
    text.draw(surface)
    return surface.get_npimage()


def draw_stars(t):
    surface = gz.Surface(640, 120, bg_color=WHITE_GIZEH)
    for i in range(5):
        star = gz.star(
            nbranches=5, radius=120*0.2, ratio=0.5,
            xy=[100*(i+1), 50], fill=GREEN, angle=t * pi)
        star.draw(surface)
    return surface.get_npimage()





with open('./assets/keywords.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        textToRender = row[0]
        print(textToRender)
        tts=gtts.gTTS(textToRender)
        tts.save(textToRender + '.mp3')

        audioclip = AudioFileClip(textToRender + '.mp3')
        new_audioclip = CompositeAudioClip([audioclip])

        sb_logo = ImageClip(SB_LOGO_PATH). set_position(('center', 0)).resize(width=200)
        text = VideoClip(render_text, duration=DURATION)
        stars = VideoClip(draw_stars, duration=DURATION)

        video = CompositeVideoClip(
            [
                sb_logo,
                text.set_position(
                    ('center', sb_logo.size[1])),
                stars.set_position(
                    ('center', sb_logo.size[1] + text.size[1])
                )
            ],
            size=VIDEO_SIZE). \
            on_color(
            color=WHITE,
            col_opacity=1).set_duration(DURATION)
        video.audio = new_audioclip
        video.write_videofile('generated/' +textToRender + '.mp4', fps=10)
        os.remove(textToRender + '.mp3')
