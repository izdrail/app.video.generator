import gtts
import csv 
import moviepy.editor as mpy
import gizeh as gz
from math import pi




VIDEO_SIZE = (640, 480)
BLUE = (59/255, 89/255, 152/255)
GREEN = (176/255, 210/255, 63/255)
WHITE = (255, 255, 255)
WHITE_GIZEH = (1, 1, 1)
SB_LOGO_PATH = './assets/logo.png'
DURATION = 10


with open('./assets/keywords.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	for row in csv_reader:
		textToRender = row[0]
		print(textToRender)
		tts=gtts.gTTS(textToRender)
		tts.save(textToRender + '.mp3')
		surface = gz.Surface(640, 60, bg_color=WHITE_GIZEH)
		text = gz.text(textToRender, fontfamily="Charter",fontsize=30, fontweight='bold', fill=BLUE, xy=(320, 40))
		text.draw(surface)
		renderedTextAsImage =  surface.get_npimage()

		sb_logo = mpy.ImageClip(SB_LOGO_PATH). set_position(('center', 0)).resize(width=200)

		textVideo = mpy.VideoClip(renderedTextAsImage, duration=DURATION)
        
		video = mpy.CompositeVideoClip([sb_logo,textVideo.set_position(('center', sb_logo.size[1]))],size=VIDEO_SIZE).on_color(color=BLACK,col_opacity=1).set_duration(DURATION)
		video.write_videofile( textToRender + '.mp4', fps=10)
