import boto3
import sys
import contextlib
import pprint
import time
import uuid

def translate():
    t_obj = boto3.client('translate')
    txt = sys.argv[1]

    t_out = t_obj.translate_text(
        Text=txt,
        SourceLanguageCode='ja',
        TargetLanguageCode='en'
    )

    return t_out['TranslatedText']

def polly(text):
    f_out = 's_out.mp3'
    
    p_obj = boto3.client('polly')
    p_out = p_obj.synthesize_speech(
	    Text=text,
	    OutputFormat='mp3',
	    VoiceId='Salli'
    )
    
    with contextlib.closing(p_out['AudioStream']) as a_stream:
	    with open(f_out, 'wb') as file:
    		file.write(a_stream.read())
    		
def transcribe():
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


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {} [sentence]".format(sys.argv[0]))
        sys.exit()
    
    translated_text = translate()
    polly(translated_text)
    transcribe()