from gtts import gTTS

def save_tts(script_text, output_path="talking-ppt/audio/tts.mp3", lang='en'):
    try:
        tts = gTTS(text=script_text, lang=lang)
        tts.save(output_path)
        print(f"[✔] 음성 저장 완료: {output_path}")
    except Exception as e:
        print(f"[오류] TTS 저장 실패: {e}")
