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

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
stream.start_stream()

in_speech_bf = False
paused = False
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
                print 'Hypothesis:', hypothesis
                if 'stop' == hypothesis:
                    print 'Will stop execution of program'
                    sys.exit(0)
                elif 'pauză' == hypothesis:
                    paused = True
                    print 'Paused: say \'START\' to resume running commands'
                else:
                    if paused:
                        if 'start' in hypothesis:
                            paused = False
                            print 'Resumed running commands'
                    else:
                        run_mapped_script_if_exists(hypothesis)
                decoder.start_utt()
    else:
        break
decoder.end_utt()
