import subprocess
import json
import transcribe_functions as file_handler

file_to_convert = file_handler.get_from_YouTube()
wav_file, mono_file, txt_file = file_handler.convert_to_mono_wav(file_to_convert)
bucket_name = "box_of_rain"
file_to_transcribe = 'gs://' + bucket_name + '/' + mono_file
file_handler.upload_to_bucket(mono_file,file_to_transcribe)
transcript = file_handler.SayWhat(file_to_transcribe)
text_file = "Transcripts/" + txt_file
with open(text_file,"w+") as f:
    f.write(transcript)

file_handler.delete_from_bucket(file_to_transcribe)
file_handler.delete_from_local(file_to_convert, wav_file, mono_file)
