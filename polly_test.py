import boto3
import contextlib

text = 'こんにちは'
f_out = 's_out.mp3'

p_obj = boto3.client('polly')
p_out = p_obj.synthesize_speech(
	Text=text,
	OutputFormat='mp3',
	VoiceId='Takumi'
)

with contextlib.closing(p_out['AudioStream']) as a_stream:
	with open(f_out, 'wb') as file:
		file.write(a_stream.read())

