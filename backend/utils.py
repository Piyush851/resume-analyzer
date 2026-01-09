from pdfminer.high_level import extract_text # pyright: ignore[reportMissingImports]
import re
import json
import os

def extract_text_from_pdf(pdf_path):
    # Extract text from a PDF file using pdfminer.six
    try:
        text = extract_text(pdf_path)
        return text
    except Exception as e:
        return str(e)

def clean_text(text):
    # Basic cleaning: removes newlines and extra spaces
    text = text.replace('\n', ' ') # Replace new line with " "
    text = re.sub(' +', ' ', text)
    return text.strip()

def load_skills():
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, 'data', 'skills.json')

    with open(file_path, 'r') as f:
        return json.load(f)

def extract_skills(text):
    skills_db =load_skills()
    found_skills = {}

    for category, skill_list in skills_db.items():
        found_in_category = set()

        for skill_obj in skill_list:
            skill_name = skill_obj['name']
            aliases = skill_obj.get('aliases', [])
            is_case_sensitive = skill_obj.get('case_sensitive',False)
            search_terms = [skill_name] + aliases

            for term in search_terms:
                escaped_term = re.escape(term)
                pattern = r'\b' + escaped_term + r'\b'
                flags = 0 if is_case_sensitive else re.IGNORECASE
                if re.search(pattern, text, flags):
                    found_in_category.add(skill_name)
                    break

        if found_in_category:
            found_skills[category] = list(found_in_category)
    return found_skills
