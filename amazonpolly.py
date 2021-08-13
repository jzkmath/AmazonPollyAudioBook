import boto3
import os
from contextlib import closing
#from boto3.dynamodb.conditions import Key, Attr

def pollytext(filename,pollyvoice):


    #Added encoding='utf-8' to prevent errors in windows python
    with open(filename, encoding='utf-8') as file: 
        text = file.read()

    polly_client = boto3.Session(
        aws_access_key_id='YOU GET YOUR AWS ACCESS KEY FROM AMAZON',
        aws_secret_access_key='YOU GET YOUR AWS SECRET KEY FROM AMAZON',
        region_name='us-east-1').client('polly')


    sep = '.'
    outputfilename = filename.split(sep, 1)[0]

    voice = pollyvoice

    rest = text

    #Because single invocation of the polly synthesize_speech api can
    # transform text with about 1,500 characters, we are dividing the
    # post into blocks of approximately 1,000 characters.
    textBlocks = []
    while (len(rest) > 1400):
        begin = 0
        end = rest.find(".", 1000)

        if (end == -1):
            end = rest.find(" ", 1000)

        textBlock = rest[begin:end]
        rest = rest[end+1:] #Remove the annoying "Dot" that otherwise starts each new block since you no longer start on that index.
        textBlocks.append(textBlock)
    textBlocks.append(rest)


    #For each block, invoke Polly API, which will transform text into audio

    for textBlock in textBlocks:
        response = polly_client.synthesize_speech(
            OutputFormat='mp3',
            Text = textBlock,
            VoiceId = voice,
            Engine = 'neural'
        )

        #Save the audio stream returned by Amazon Polly on Lambda's temp
        # directory. If there are multiple text blocks, the audio stream
        # will be combined into a single file.



        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                output = os.path.join('tmp', outputfilename + '.mp3')
                with open(output, "ab") as file:
                   file.write(stream.read())




pollytext('audiobookname.txt','Amy')
