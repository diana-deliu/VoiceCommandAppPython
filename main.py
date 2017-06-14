# encoding=utf8
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from os import environ, path
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
import json
import subprocess
import pyaudio

SCRIPTSDIR = 'scripts\\'
MODELDIR = 'model'
DATADIR = 'pocketsphinx/test/data'

mapping = json.load(open('input/mapping.json'))

def run_mapped_script_if_exists(hypothesis):
    for key, value in mapping.iteritems():
        if key in hypothesis:
            bat_file_path = SCRIPTSDIR + value
            print 'Will run:', bat_file_path
            p = subprocess.Popen('start cmd /c ' + bat_file_path, shell=True)
            p.wait()
            break

config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, 'acoustic_model'))
config.set_string('-lm', path.join(MODELDIR, 'acoustic_model.lm'))
config.set_string('-dict', path.join(MODELDIR, 'acoustic_model.dic'))
decoder = Decoder(config)
# config.set_string('-keyphrase', 'forward')
# config.set_float('-kws_threshold', 1e+20)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
stream.start_stream()

in_speech_bf = False
decoder.start_utt()
while True:
    buf = stream.read(1024)
    if buf:
        decoder.process_raw(buf, False, False)
        if decoder.get_in_speech() != in_speech_bf:
            in_speech_bf = decoder.get_in_speech()
            if not in_speech_bf:
                decoder.end_utt()
                hypothesis = decoder.hyp().hypstr
                if hypothesis == 'stop':
                    sys.exit(0)
                elif hypothesis == 'pauză':
                    if hypothesis == 'start':
                        print 'Result:', hypothesis
                        run_mapped_script_if_exists(hypothesis)
                        decoder.start_utt()
                    else:
                        continue
    else:
        break
decoder.end_utt()
