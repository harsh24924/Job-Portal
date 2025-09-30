import os
import re
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

def prepare_prompt(instructions, pair):
    job = pair.job
    resume = pair.resume

    job_string = f"""
        Title: {job.title}\n
        Company: {job.company}\n
        Location: {job.location}\n
        Description: {job.description}\n
        Requirements: {job.requirements}\n\n
    """

    resume_string = f"""
        Summary: {resume.summary}\n
        Skills: {resume.skills}\n
        Education: {resume.education}\n
        Experience: {resume.experience}\n
        Projects: {resume.projects}\n\n
    """

    prompt = instructions + "\n\n" + job_string + resume_string
    return prompt

def generate(prompt):
    client = genai.Client(api_key = os.environ.get("GEMINI_KEY"))

    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = prompt
    )

    if response.text == None:
        return "Error: Could not parse analysis from model."
    return response.text

def extract_json(analysis_text: str) -> dict:
  match = re.search(r"\{.*\}", analysis_text, re.DOTALL)
  
  if not match:
      print("Warning: No JSON object found in the LLM response.")
      return {"matches": [], "missing": ["Error: Could not parse analysis from model."]}

  json_string = match.group(0)

  try:
      return json.loads(json_string)
  except json.JSONDecodeError:
      print(f"Warning: Malformed JSON detected: {json_string}")
      return {"matches": [], "missing": ["Error: LLM returned invalid JSON."]}