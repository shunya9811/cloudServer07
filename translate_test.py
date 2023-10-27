import boto3

t_obj = boto3.client('translate')
txt = 'クラウドサーバ構築特論の授業です。'
txt_en = 'I am studing at AIIT.'

t_out = t_obj.translate_text(
  Text=txt_en,
  #SourceLanguageCode='ja',
  #TargetLanguageCode='en'
  SourceLanguageCode='en',
  TargetLanguageCode='ja'
)

print(t_out)
print(t_out['TranslatedText'])


