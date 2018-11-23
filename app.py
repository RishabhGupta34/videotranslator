from flask import Flask,render_template,request
import pafy
import speech_recognition as sr
#import urllib.request
#import goslate
#from translation import google, ConnectError
import shutil
from translate import Translator
import os 
from pydub import AudioSegment
import youtube_dl
from pydub import AudioSegment
from pydub.silence import split_on_silence

to_lang = 'hi'
#secret = '<your secret from Microsoft>'
translator = Translator(to_lang=to_lang)
#proxy_handler = urllib.request.ProxyHandler({"http" : "http://67.63.33.7:80"})
#proxy_opener = urllib.request.build_opener(urllib.request.HTTPHandler(proxy_handler),
                      #              urllib.request.HTTPSHandler(proxy_handler))
#from googletrans import Translator
#translator = Translator()

# audio_chunks = split_on_silence(sound_file, 
#     # must be silent for at least half a second
#     min_silence_len=500,

#     # consider it silent if quieter than -16 dBFS
#     silence_thresh=-16
# )

# for i, chunk in enumerate(audio_chunks):

app=Flask(__name__)

#def audio_convert(link):
	


@app.route("/home",methods=['GET','POST'])
def home():
	if request.method=='GET':
		return render_template('home.html')
	elif request.method=='POST':
		link=request.form.get("vidlink")
		url=link
		# video = pafy.new(url)
		# bestaudio = video.getbestaudio()	
		# bestaudio.download("audioc.ogg")
		# song = AudioSegment.from_file("audioc.ogg", format="ogg")
		# song.export("audioc1.ogg", format="ogg")
		
		options = {
			    'format':'bestaudio/best',
			    'extractaudio':True,
			    'audioformat':'wav',
			    'outtmpl':'%(id)s',     #name the file the ID of the video
			    'noplaylist':True,
			    'postprocessors': [{
			        'key': 'FFmpegExtractAudio',
			        'preferredcodec': 'wav',
			        'preferredquality': '192',
			    }]
			}
			    # 'nocheckcertificate':True,
			
		with youtube_dl.YoutubeDL(options) as ydl:
		    ydl.download([link])
		#with sr.AudioFile(AUDIO_FILE) as source:
		#	audio = r.record(source)
		sound_file = AudioSegment.from_wav("wav")

		for i, chunk in enumerate(sound_file[::3500]):
		    out_file = "./split/chunk%03d.wav"%i
		    chunk.export(out_file, format="wav")

		path="D:/split/"
		os.mkdir(path)
		files=sorted(os.listdir(path))
		cid="R_02XikG3l1iC05AUw1wfg=="
		ck="ulxB9AJylsOpX-neGUlArSv1iquw3ZrG8oIZZ5BhIyfyL_T8ZwYuYWtoQUk3aexLL2ZrJoPlPAXIO8PypfYSWQ=="
		all_text=""
		for i in range(len(files)):
		    AUDIO_FILE = path+files[i]
		    r = sr.Recognizer()
		    r.energy_threshold = 70

		    with sr.AudioFile(AUDIO_FILE) as source:
		        audio = r.record(source)
		    try:
		    	a=r.recognize_sphinx(audio) #,client_id=cid,client_key=ck
		    	all_text=" ".join([all_text,a])
		    except sr.UnknownValueError:
		        print("Google Speech Recognition could not understand audio")

		# AUDIO_FILE = "wav"
		# r = sr.Recognizer()

		# with sr.AudioFile(AUDIO_FILE) as source:
		# 	audio = r.record(source)
		# cid="R_02XikG3l1iC05AUw1wfg=="
		# ck="ulxB9AJylsOpX-neGUlArSv1iquw3ZrG8oIZZ5BhIyfyL_T8ZwYuYWtoQUk3aexLL2ZrJoPlPAXIO8PypfYSWQ=="
		# try:
		# 	# all_text=r.recognize_houndify(audio,client_id=cid,client_key=ck)
		# 	all_text=r.recognize_google(audio,language="hi-IN")
		# 	#with open("audiotext.txt","w") as file:
		# 	#	file.write(r.recognize_houndify(audio,client_id=cid,client_key=ck))
		# except sr.UnknownValueError:
		# 	print("Google Speech Recognition could not understand audio")
		#with open("audiotext.txt","r") as file1:
		#	all_text=file1.read()
		#gs = goslate.Goslate()
		#gs.translate(all_text)
		#print(google(all_text, dst = 'hi', proxies = {'http': '69.127.29.51:19948'}))
		print(all_text)
		translation=translator.translate(all_text[:len(all_text)//2])
		translation=translation+translator.translate(all_text[len(all_text)//2:])
		# with open('tr.docx','w') as f:
		# 	f.write(translation)
		shutil.rmtree(path)
		return render_template("trans.html",translation=translation)


if __name__=="__main__":
	app.run(port=8000,debug=True)