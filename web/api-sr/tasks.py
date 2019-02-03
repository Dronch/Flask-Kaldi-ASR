from rq import get_current_job
import datetime
import librosa
import soundfile as sf
import io
import os
from subprocess import Popen, PIPE
import re


def save_wav(wav_data, outfile, samplerate=8000, subtype='PCM_16'):
    try:
        tmp = io.BytesIO(wav_data)
        data, sr = sf.read(tmp)

        data = librosa.to_mono(data)
        data = librosa.resample(data, sr, samplerate)

        sf.write(outfile, data, samplerate, subtype=subtype)
        return librosa.get_duration(y=data, sr=samplerate)
    except:
        return None


def kaldi_decode(folder, duration):

    scp = os.path.join(folder, 'wav.scp')
    f = open(scp, 'w')
    f.write('decoder-test {}'.format(os.path.join(folder, 'speech.wav')))
    f.close()

    with Popen("cd /opt/model && ./decode.sh {}".format(scp), shell=True, stdout=PIPE, stderr=PIPE) as p:
        output, errors = p.communicate()
        try:
            text = re.search(r'decoder-test (.*)', errors.decode('utf-8')).group(1)
        except:
            text = ''

    tempo = len(text.replace(' ', '')) / duration

    return text, tempo


def wav_to_text(wav_data, tmp_folder):

    try:
        job_started = datetime.datetime.now()

        job = get_current_job()
        guid = job.get_id()
        folder = os.path.join(tmp_folder, guid)
        os.makedirs(folder)
        wav_file = os.path.join(folder, 'speech.wav')

        duration = save_wav(wav_data, wav_file)
        if not duration:
            return None, 400

        result, speech_speed = kaldi_decode(folder, duration)

        job_finished = datetime.datetime.now()

        return {
            'ready': True,
            'text': result,
            'job_started': job_started,
            'job_finished': job_finished,
            'speech_speed': speech_speed
               }, 200
    except:
        return None, 500
