from ppt_extractor import extract_ppt_content
from script_generator import generate_presentation_script_with_context_ollama

if __name__ == "__main__":
    PPT_FILE_PATH = filepath

    extracted_data = extract_ppt_content(PPT_FILE_PATH)

    if extracted_data:
        generate_presentation_script_with_context_ollama(extracted_data)

