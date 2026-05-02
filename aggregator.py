import json
import os
from google import genai

# Setup the Client
client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

def get_live_briefing():
    prompt = """
    Search for the most recent news (last 3 days) regarding climate change topics 
    relevant to Nationwide Building Society. 
    
    These should be relevant to:
    1. Climate risk management in banking and financial services
    2. PRA SS5/25, or other UK applicable regulation
    3. Climate scenario analysis and stress testing, including incorporating climate elements into IFRS9, and new Scenarios from the likes of NGFS
    4. Climate related disclosures (ISSB S2, TCFD, Transition Plans)
    5. Financed emissions and target setting
    6. Data, modelling and risk management challenges
    7. Changes in government green policy, energy security strategy, or home energy efficiency
    8. Associated peer bank activity (Lloyds, Natwest, Barclays, Santander, HSBC)
    
    COLLATE this into a thematic briefing. Ignore marketing materials.
    Return ONLY a JSON list of objects:
    [{"theme": "...", "briefing": "...", "links": ["..."]}]
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-3.0-flash',
            contents=prompt,
            config={'tools': [{'google_search': {}}]}
        )
        
        # Clean the output to ensure it is valid JSON
        text_content = response.text
        clean_json = text_content.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_json)
    except Exception as e:
        print(f"Error occurred: {e}")
        return []

if __name__ == "__main__":
    briefing = get_live_briefing()
    with open('tailored_news.json', 'w') as f:
        json.dump(briefing, f, indent=4)
