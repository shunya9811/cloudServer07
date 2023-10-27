import boto3
import pprint
import time
import uuid

f_name = 's_out.mp3'
b_name = 'report.aws-s23745140.com'

s3_obj = boto3.resource('s3')
b_obj = s3_obj.Bucket(b_name)
b_obj.upload_file(f_name, f_name)

t_obj = boto3.client('transcribe', 'ap-northeast-1')

jobID = str(uuid.uuid1())
t_out = t_obj.start_transcription_job(
	TranscriptionJobName=jobID,
	Media={'MediaFileUri': 's3://' + b_name + '/' + f_name},
	MediaFormat='mp3',
	LanguageCode='en-US'
)
pprint.pprint(t_out)

while True:
	t_out = t_obj.get_transcription_job(TranscriptionJobName=jobID)
	status = t_out['TranscriptionJob']['TranscriptionJobStatus']
	if status != 'IN_PROGRESS':
		break
	time.sleep(5)
	
print(status)
pprint.pprint(t_out)

