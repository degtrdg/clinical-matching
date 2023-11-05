import os
import openai
import dotenv
from module.prompts import *

dotenv.load_dotenv(".env")
openai.api_key = os.environ.get("OPENAI_API_KEY")


def get_patient_match_result(patient_report, clinical_trial):
    try:
        sys_prompt = oncologist_sys_prompt
        prompt = patient_matching.format(patient_report=patient_report, clinical_trial=clinical_trial)
        response = openai.ChatCompletion.create(
          model="gpt-4",
          messages=[{
              "role": "system",
              "content": sys_prompt 
          },
          {
              "role": "user",
              "content": prompt
          }],
          temperature=0,
          max_tokens=1500
        )
        text = response["choices"][0]["message"]["content"]
        answer_header = "# Answer"
        last_index_of_answer_header = text.rindex(answer_header)
        reasoning = text[:last_index_of_answer_header]
        answer = text[last_index_of_answer_header + len(answer_header):]
        # String \n if it exists
        if answer[0] == '\n':
            answer = answer[1:]
        return {
            'reasoning': reasoning,
            'answer': answer
        }
    except Exception as e:
        print(f"An error occurred while generating the prompt: {e}")
        return None
