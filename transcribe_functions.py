import subprocess
import pathlib
import os
import json

def get_from_YouTube():
    """Gets mp4 video file with Youtube-DL"""
    link = input("Give the youtube link: ")
    cmd= ['youtube-dl', '-o', '%(title)s.%(ext)s', '-f', '18', link]
    res = subprocess.call(cmd)
    for path in pathlib.Path('/Users/J/Desktop/GoogleTranscribe').iterdir():
        if path.is_file():
            if path.suffix == '.mp4':
                old_name = path.stem #original filename
                show_num = old_name.split(' -')[0] # number at front
                suf = path.suffix #original file extension
                directory = path.parent #current file location
                num_name = show_num + suf
                path.rename(pathlib.Path(directory, num_name))
                file_to_convert = num_name
    return file_to_convert

def convert_to_mono_wav(file_to_convert):
    """Converts mp4 stereo to mono wav"""
    vid_file = file_to_convert
    filename = vid_file.split(".mp4")[0]
    txt_file = filename + ".txt"
    wav_file = filename + ".wav"
    cmd1 = ['avconv', '-i', vid_file, '-vn', '-f', 'wav', wav_file]
    subprocess.call(cmd1)
    mono_file = filename + "_mono.wav"
    cmd2 = ['sox', wav_file, '-c', '1', mono_file]
    subprocess.Popen(cmd2)
    return wav_file, mono_file, txt_file

def upload_to_bucket(mono_file, file_to_transcribe):
    """Uploads a file to the bucket."""
    cmd = ['gsutil', 'cp', mono_file, file_to_transcribe]
    subprocess.call(cmd)

def SayWhat(file_to_transcribe):
    """Google Cloud Speech to Text with glcoud command line interface"""
    #long running recognize with speaker diarization and punctuation
    cmd1 = ['gcloud', 'alpha', 'ml', 'speech', 'recognize-long-running', file_to_transcribe, '--language-code=en-US', '--async', '--format=json', '--enable-speaker-diarization', '--audio-channel-count=1', '--separate-channel-recognition', '--enable-automatic-punctuation']
    res1 = subprocess.check_output(cmd1)
    res1 = json.loads(res1.decode('utf8'))
    opid = res1['name']
    cmd2 = ['gcloud','ml','speech','operations','wait', opid, '--format=json']
    res2 = json.loads(subprocess.check_output(cmd2))
    result = res2['results'][-1]
    words_info = result['alternatives'][0]['words']
    transcript = ""
    lastSpeaker = -1
    for word_info in words_info:
        if word_info['speakerTag'] == lastSpeaker:
            transcript+= word_info['word']
            transcript+=" "
        else:
            transcript+= "\n"
            transcript+= str(word_info['speakerTag'])
            transcript+= ": "
        lastSpeaker = word_info['speakerTag']
    return transcript

def delete_from_bucket(file_to_delete):
    """Deletes a file from the bucket."""
    cmd = ['gsutil', 'rm', file_to_delete]
    subprocess.call(cmd)

def delete_from_local(file_to_convert, wav_file, mono_file):
    """Deletes the original video from local."""
    cmd = ['rm', file_to_convert, wav_file, mono_file]
    subprocess.call(cmd)
