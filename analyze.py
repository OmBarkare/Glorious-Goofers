import json
import os
from google import genai
from datetime import datetime
import re

CHECK_INTERVAL_SECONDS = 0.5
ANALYZE_INTERVAL_SECONDS = 10  # 10s for testing, change to 300s later
SYSTEM_PROMPT = """
You are a productivity analyzer.
I will give you JSON logs of app usage.

Each entry has:
- app_name
- total_time_spent (seconds)
- longest_session (seconds)
- last_active (timestamp)

**Your tasks:**
1. Group entries by application type (e.g., all "YouTube - ..." = "YouTube", all "Visual Studio Code - ..." = "VS Code").
2. For each grouped app:
   - Split into **productive usage** and **unproductive usage** (two separate entries).
   - Decide which individual logs (window titles) are productive vs unproductive.  
     Example: "YouTube - music / memes" → unproductive,  
     "YouTube - tutorial / lecture / course" → productive.
   - Aggregate time separately for productive and unproductive.
   - Take the maximum longest_session for each category.
   - Use the most recent last_active for each category.
3. Summary:
   - total_time (sum of all times)
   - productive_time
   - unproductive_time
   - productivity_score = (productive_time / total_time) * 100
4. Provide 2-3 insights.
5. give a list of single DEFINING keywords that strongly suggest if a window is productive based on your analysis for current dataset. 
   Avoid generic keywords which might imply both productive and unproductive usage or be neutral. Keep the list concise.


**Output format (strict JSON only):**
{
  "summary": {
    "total_time": <float>,
    "productive_time": <float>,
    "unproductive_time": <float>,
    "productivity_score": <float>
  },
  "apps": [
    {
      "app_name": "YouTube",
      "productive": {
        "total_time_spent": <float>,
        "longest_session": <float>,
        "last_active": "<timestamp>"
      },
      "unproductive": {
        "total_time_spent": <float>,
        "longest_session": <float>,
        "last_active": "<timestamp>"
      }
    },
    {
      "app_name": "VS Code",
      "productive": {
        "total_time_spent": <float>,
        "longest_session": <float>,
        "last_active": "<timestamp>"
      },
      "unproductive": {
        "total_time_spent": 0,
        "longest_session": 0,
        "last_active": null
      }
    }
  ],
  "insights": [
    "<string>",
    "<string>"
  ],
  "productive_keywords": ["<string>", "<string>"]
}
"""
USER_DATA_FILE = "./data/user_data.json"
# Global state flags
last_analyze_time = datetime.now()
analyze_in_progress = False

def analyze_worker(log_path):
    global analyze_in_progress
    try:
        print("[ANALYZE] Starting analysis...")
        analyze_data(log_path)  # your existing function
        print("[ANALYZE] Done.")
    except Exception as e:
        print(f"[ANALYZE] Error: {e}")
    finally:
        analyze_in_progress = False  # release the lock

def maybe_trigger_analysis(log_path):
    global last_analyze_time, analyze_in_progress
    now = datetime.now()
    analyze_worker(log_path)

# Load your log JSON from file
def analyze_data(log_path):
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    with open(log_path, "r", encoding="utf-8") as f:
        logs = json.load(f)

    # Convert logs to string and insert into prompt
    user_prompt = SYSTEM_PROMPT + "\n\nNow here is the log JSON:\n" + json.dumps(logs, indent=2)

    # Gemini expects structured request
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=f"{user_prompt}"
    )

    # Extract model’s reply
    raw_output = response.text  # get the text response
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw_output.strip(), flags=re.DOTALL)
    try:
        analyzed_data = json.loads(cleaned)  # 🔥 parse into dict
        os.makedirs(os.path.dirname(USER_DATA_FILE), exist_ok=True)
        with open(USER_DATA_FILE, "w", encoding="utf-8") as f:
          json.dump(analyzed_data, f, indent=2, ensure_ascii=False)      # 🔥 save into user_data.json
        print(f"[ANALYZE] Saved results to {USER_DATA_FILE}")
    except Exception as e:
        print(f"[ANALYZE] Could not parse/save response: {e}")
        print("Raw output:", raw_output)
