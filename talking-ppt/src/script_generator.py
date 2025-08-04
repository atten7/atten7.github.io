# script_generator.py

from openai import OpenAI
from tts_utils import post_process_for_tts  # TTS 전처리 함수가 있으면 임포트
from tts import save_tts

# Ollama API 클라이언트 생성 (localhost:11434가 Ollama 서버 주소)
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # 아무 문자열이나 가능
)

def generate_presentation_script_with_context_ollama(slides_data, model_name="llama3:instruct"):
    if not slides_data:
        print("[오류] 슬라이드 데이터 없음")
        return

    full_script_raw = []
    full_script_tts = []

    print("--- 전체 발표 맥락 파악 시작 ---")

    combined_content = ""
    for slide in slides_data:
        combined_content += f"슬라이드 {slide['slide_number']}:\n"
        if slide['text']:
            combined_content += f"텍스트: {' '.join(slide['text'])}\n"
        if slide['notes']:
            combined_content += f"메모: {slide['notes']}\n"
        if slide['images']:
            combined_content += f"이미지: {', '.join(slide['images'])}\n"
        combined_content += "\n"

    context_prompt = f"""
Below is the content of all slides in the PPT presentation.
Please analyze this content and summarize the overall presentation's theme, key message, and key keywords.
This summary will serve as an important context for creating the script for each slide.
Please reply with only the content, excluding all comments.
---
{combined_content}
---
"""

    try:
        context_response = client.completions.create(
            model=model_name,
            prompt="You are an AI that writes PPT presentation scripts.\n\n" + context_prompt,
            max_tokens=1000,
            temperature=0.7,
        )
        presentation_context = context_response.choices[0].text.strip()
        print(presentation_context)
    except Exception as e:
        print(f"[오류] 맥락 파악 실패: {e}")
        presentation_context = "맥락 파악 불가"

    print("--- 각 슬라이드별 대본 생성 시작 ---")

    for slide_info in slides_data:
        slide_number = slide_info["slide_number"]
        slide_text = "\n".join(slide_info["text"])
        slide_notes = slide_info["notes"]
        image_captions = ", ".join(slide_info["images"])

        script_prompt = f"""
[발표 전체 개요]
{presentation_context}
Below are the key points from the PPT slide {slide_number} corresponding to the outline above.
Based on the summary on the slide, please create a presentation script that explains this content in a way that fits the overall presentation flow.
If necessary, enrich the content by adding background information or examples.
Please ensure the script connects seamlessly with the previous slides.
Please write a script of 1-2 minutes per slide.
Please reply with only the content, excluding all comments.
Except for things like 'script for Slide'
---
Slide text: {slide_text if slide_text else "없음"}
Presentation Notes: {slide_notes if slide_notes else "없음"}
Image Description: {image_captions if image_captions else "없음"}
---
"""

        print(f"\n[슬라이드 {slide_number} 대본 생성 중...]")
        try:
            response = client.completions.create(
                model=model_name,
                prompt="You are an AI that writes PPT presentation scripts.\n\n" + script_prompt,
                max_tokens=1500,
                temperature=0.7,
            )
            script_text = response.choices[0].text.strip()

            full_script_raw.append(f"--- 슬라이드 {slide_number} ---\n{script_text}\n")
            tts_text = post_process_for_tts(script_text) if 'post_process_for_tts' in globals() else script_text
            full_script_tts.append(f"{tts_text}\n")

            print(f"--- 슬라이드 {slide_number} 대본 ---")
            print(script_text)

        except Exception as e:
            print(f"[오류] 슬라이드 {slide_number} 대본 생성 실패: {e}")
            full_script_raw.append(f"--- 슬라이드 {slide_number} ---\n[오류로 인해 실패]\n")
            full_script_tts.append(f"--- 슬라이드 {slide_number} ---\n[오류로 인해 실패]\n")

    print("\n--- 전체 대본 생성 완료 ---")

    raw_output_filename = "talking-ppt/data/presentation_script_raw.txt"
    with open(raw_output_filename, "w", encoding="utf-8") as f:
        f.write("\n\n".join(full_script_raw))

    tts_output_filename = "talking-ppt/data/presentation_script_tts.txt"
    with open(tts_output_filename, "w", encoding="utf-8") as f:
        f.write("\n\n".join(full_script_tts))

    print(f"원본 대본 저장 완료: {raw_output_filename}")
    print(f"TTS용 대본 저장 완료: {tts_output_filename}")
    print("\n--- 오디오 생성 시작 ---")
    tts_script_text = "\n\n".join(full_script_tts)
    save_tts(tts_script_text, output_path="talking-ppt/audio/tts.mp3", lang='en')
    return "\n\n".join(full_script_tts)