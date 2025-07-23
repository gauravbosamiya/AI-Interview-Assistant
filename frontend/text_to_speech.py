# import os 
# import elevenlabs
# from elevenlabs.client import ElevenLabs
# import subprocess
# import platform
# from dotenv import load_dotenv
# from gtts import gTTS
# import io
# from pydub import AudioSegment

# load_dotenv()

# ELEVENLABS_API_KEY=os.environ.get("ELEVENLABS_API_KEY")


# def text_to_speech(questios, outputfile_path="test.mp3"):
#     client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
#     audio=client.text_to_speech.convert(
#         text=questios,
#         voice_id="s3TPKV1kjDlVtZbl4Ksh",
#         model_id="eleven_monolingual_v1",
#         output_format="mp3_22050_32"
#     )
#     elevenlabs.save(audio, outputfile_path)
#     os_name = platform.system()
#     try:
#         if os_name=="Darwin":
#             subprocess.run(['afplay',outputfile_path])
#         elif os_name=="Windows":
#             # subprocess.run(['powershell','-c',f'(New-Object Media.SoundPlayer "{outputfile_path}").PlaySync();'])
#             playsound(outputfile_path)
#         elif os_name=="Linux":
#             subprocess.run(['aplay',outputfile_path])
#         else:
#             raise OSError("Unsupported operating system")
#     except Exception as e:
#         print(f'An error occured while trying to play the audio: {e}')



# def text_to_speech_with_gtts(text, output_file="test.mp3"):
#     print("Falling back to gTTS...")
#     try:
#         tts = gTTS(text=text, lang="en")
#         tts.save(output_file)
#         print("gTTS audio saved:", output_file)

#         os_name = platform.system()
#         if os_name == "Windows":
#             playsound(output_file)
#         elif os_name == "Darwin":
#             subprocess.run(["afplay", output_file])
#         elif os_name == "Linux":
#             subprocess.run(["aplay", output_file])
#         else:
#             raise OSError("Unsupported OS")
#     except Exception as e:
#         print("gTTS fallback failed:", e)
#     os.remove(output_file)

# questions = "Can you briefly introduce yourself and tell me about your background in Data Science?"


import io
import os
import tempfile
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import subprocess
import platform


def text_to_speech_with_speed(text, speed=1.3):
    print("Generating and playing audio faster...")

    try:
        mp3_fp = io.BytesIO()
        tts = gTTS(text=text, lang="en")
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)

        audio = AudioSegment.from_file(mp3_fp, format="mp3")
        faster_audio = audio.speedup(playback_speed=speed)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_path = temp_file.name
            faster_audio.export(temp_path, format="wav")

        os_name = platform.system()
        if os_name == "Windows":
            subprocess.run(["powershell", "-c", f'(New-Object Media.SoundPlayer "{temp_path}").PlaySync();'])
        elif os_name == "Darwin":
            subprocess.run(["afplay", temp_path])
        elif os_name == "Linux":
            subprocess.run(["aplay", temp_path])

        print("Playback completed.")

    except Exception as e:
        print("Error during playback:", e)

    finally:
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except:
            pass



