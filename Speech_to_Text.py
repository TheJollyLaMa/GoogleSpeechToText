#dedications:
#to my parents, who taught me to listen for what others really wanted and to bring them what they really needed
#to the sages who have recognized the goodness they saw before them since time immemorial
#to google who knows more than any of us
#and to Raghunath and Kaustubah for sharing their thoughts, knowledge, and wisdom for the glorification of Krsna's pastimes - the effect of which shall be our edification
#Hare Krsna Hare Krsna Krsan Krsna Hare Hare Hare Rama Hare Rama Rama Rama Hare Hare
# Thank You - this is just so cool to play with such powerful tools
import subprocess
import json
import transcribe_functions as file_handler

file_to_convert = file_handler.get_from_YouTube()
wav_file, mono_file, txt_file = file_handler.convert_to_mono_wav(file_to_convert)
bucket_name = "wisdom_bucket"
file_to_transcribe = 'gs://' + bucket_name + '/' + mono_file
file_handler.upload_to_bucket(mono_file,file_to_transcribe)
transcript = file_handler.SayWhat(file_to_transcribe)
text_file = "Transcripts/" + txt_file
with open(text_file,"w+") as f:
    f.write(transcript)

file_handler.delete_from_bucket(file_to_transcribe)
file_handler.delete_from_local(file_to_convert, wav_file, mono_file)
