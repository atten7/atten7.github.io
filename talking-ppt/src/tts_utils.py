import re

def post_process_for_tts(text):
    # 괄호 안의 내용 제거
    text = re.sub(r'\([^)]*\)', '', text)

    # 쉼표를 사용하여 쉼을 표현하는 방법으로 '...', '..' 등을 변환
    text = text.replace('...', ', ').replace('..', ', ')

    # 별표(**)로 된 강조 표현 제거
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)

    # 불필요한 여러 개의 줄바꿈을 하나로
    text = re.sub(r'\n+', '\n', text).strip()

    # 문장 끝에 쉼표가 여러 개 있는 경우 하나로
    text = re.sub(r',+', ',', text)

    return text