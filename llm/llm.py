import os
import json
from gc_agent.dir import BASE_DIR
from playwright.async_api import Playwright, async_playwright
from google import genai
from dotenv import load_dotenv
pdfo =  """Sample Document: Lab 04 - Titration of Acetic Acid1. Safety Guidelines (Read Carefully)Always wear ANSI-approved safety goggles while handling NaOH.In case of a spill, neutralize with the provided citric acid kit before wiping.Do not dispose of chemical waste in the common sink; use the labeled "Organic Waste" carboy.2. Required Materials50mL BurettePhenolphthalein indicator0.1M Sodium Hydroxide (NaOH)250mL Erlenmeyer flask3. Experimental ProcedureStep A: Rinse the burette twice with 5mL of distilled water.Step B: Fill the burette with 0.1M NaOH and record the initial volume to the nearest 0.01mL.Note: Ensure there are no air bubbles in the tip of the burette before starting the titration.Step C: Pipette 10.00mL of the vinegar sample into a clean Erlenmeyer flask.Step D: Add exactly 3 drops of phenolphthalein to the flask.Step E: Slowly add the titrant while swirling the flask until a persistent light pink color appears for at least 30 seconds.Step F: Calculate the molarity of the acetic acid using the formula: $M_1V_1 = M_2V_2$.4. Data SubmissionAll results must be entered into the LabPortal by 5:00 PM on Friday.Attach a photo of your neutralized solution to the digital report."""

load_dotenv() 
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
def load_prompt_format():
    PATH = BASE_DIR/"llm/system_prompt.txt"
    with open(PATH,"r") as file:
            return file.read()
def run_llm(pdfo):
    prompt = load_prompt_format() + pdfo
    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-3-flash-preview", contents=prompt
    )
    return response.text


if __name__ == "__main__":
    print(run_llm(pdfo))