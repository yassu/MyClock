# -*- coding: utf-8 -*-
import wave
import pyaudio

# メイン
def main():
    wf = wave.open("default_bell.wav", "r")
    # ストリーム開始
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(1024)
    while(data != b''):
        stream.write(data)
        data = wf.readframes(1024)
    stream.close()      # ストリーム終了
    p.terminate()


if __name__ == '__main__':
    main()
    main()

