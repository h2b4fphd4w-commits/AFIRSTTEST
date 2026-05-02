import json
import os
import google.generativeai as genai

# Setup Gemini
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
# Note: Ensure you are using a model version that supports tools/search
model = genai.GenerativeModel('gemini-2.0-flash') 

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
    7. Associated peer bank activity (Lloyds, Natwest, Barclays, Santander, HSBC)
    
    COLLATE this into a thematic briefing. 
    Format the final output as a JSON list of objects:
    [{"theme": "...", "briefing": "...", "links": ["url1", "url2"]}]
    """
    
    # We call the model with 'google_search' enabled
    response = model.generate_content(prompt, tools=[{'google_search': {}}])
    
    try:
        # Extract and clean the JSON
        clean_json = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_json)
    except:
        # Fallback if AI formatting gets messy
        print("Formatting error, retrying...")
        return []

if __name__ == "__main__":
    briefing = get_live_briefing()
    with open('tailored_news.json', 'w') as f:
        json.dump(briefing, f, indent=4)
