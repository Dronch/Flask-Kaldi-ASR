from rq import get_current_job
import datetime
import librosa
import soundfile as sf
import io
import os


def save_wav(wav_data, outfile, samplerate=8000, subtype='PCM_16'):
    try:
        tmp = io.BytesIO(wav_data)
        data, sr = sf.read(tmp)

        data = librosa.to_mono(data)
        data = librosa.resample(data, sr, samplerate)

        sf.write(outfile, data, samplerate, subtype=subtype)
        return True
    except:
        return False


def kaldi_decode(wav_file):
    return 'Test', 10


def wav_to_text(wav_data, tmp_folder):

    try:
        job_started = datetime.datetime.now()

        job = get_current_job()
        guid = job.get_id()
        folder = os.path.join(tmp_folder, guid)
        os.makedirs(folder)
        wav_file = os.path.join(folder, 'speech.wav')

        if not save_wav(wav_data, wav_file):
            return None, 400

        result, speech_speed = kaldi_decode(wav_file)

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
