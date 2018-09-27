import ffmpy
from myrecorder import file_sender

def scheduled_recording(duration, instream, file_name):
	ff = ffmpy.FFmpeg(inputs={instream:None},outputs={f'./files/{file_name}.mp3':'-t '+ duration})
	ff.run()

	# optional function to email mp3 file to user after completion
	#file_sender.sendit()

