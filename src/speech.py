import re
from typing import List

import rake_nltk
import pyaudio
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.oauth2 import service_account
from rake_nltk import Metric
from six.moves import queue
import numpy as np
from src.shutterstock_utils import get_video

credentials = service_account.Credentials. from_service_account_file(r'C:\Users\Evan6\Downloads\My First Project-4397387e7cb5.json')
QQQ=16
# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


def find_deg(l, x):
    t = len(l)
    for i in l:
        t += i.count(" ")
    q = t
    for i, e in enumerate(l):
        if re.search(fr'\b({x})\b', e, re.I):
            return (q - (e.count(" "))/(2*t)) / t
        q -= 1 + e.count(" ")
    return 0.0
def find_freq(l,x):
    if x in l:
        return 1-l.index(x)/len(l)
    return 0.25
def get_important(splitted:List[str]):
    freq_r = rake_nltk.Rake(max_length=3, ranking_metric=Metric.WORD_FREQUENCY)
    freq_r.extract_keywords_from_text(" and ".join(splitted))
    freq_phrases = freq_r.get_ranked_phrases()

    deg_r = rake_nltk.Rake(max_length=3, ranking_metric=Metric.WORD_DEGREE)
    deg_r.extract_keywords_from_text(" ".join(splitted))
    deg_phrases=deg_r.get_ranked_phrases()

    freq_data={i:find_freq(freq_phrases,i.lower()) for i in splitted}
    deg_data={i: find_deg(deg_phrases,i.lower()) for i in splitted}
    data={}
    for k,freq_v in freq_data.items():
        deg_v=deg_data[k]
        data[k]=freq_v+deg_v
    print(deg_phrases)
    print(deg_data)
    print(freq_phrases)
    print(freq_data)
    return [j[0] for j in sorted(data.items(),key=lambda i:-i[1])[:3]]

class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)


def listen_print_loop(responses):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    total=""
    print("AAAAAAAAA")
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript
        # print("t",total+transcript)
        if (total+transcript).count(" ")>=QQQ:
            phrases=(total+" "+transcript).split()[-QQQ:-1]
        else:
            phrases=(total+" "+transcript).split()
        phrase=get_important(phrases)
        # print(total+" "+transcript)
        print("phrase",phrase)
        print("phrases",phrases)
        print(get_video(phrase))
        if result.is_final:
            total+=" "+transcript
            # print(transcript + overwrite_chars)

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r'\b(exit|quit)\b', transcript, re.I):
                print('Exiting..')
                break


def main():
    print("START")
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    language_code = 'en-US'  # a BCP-47 language tag

    client = speech.SpeechClient(credentials=credentials)
    print("CLIENTED")
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True)
    print("WITH")
    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)
        responses = client.streaming_recognize(streaming_config, requests)

        # Now, put the transcription responses to use.
        listen_print_loop(responses)


if __name__ == '__main__':
    main()