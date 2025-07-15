# build final persona from chunk summaries
import re
import os
import json
import openai
from dotenv import load_dotenv
from pathlib import Path
from sharedusername import get_username
username = get_username()

load_dotenv()
openai.api_key = os.getenv("API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

def load_summaries(username):
    with open(f"summaries/{username}_chunks.json", "r", encoding="utf-8") as f:
        return json.load(f)

def make_persona_prompt(summaries, username):
    blocks = []
    for chunk in summaries:
        summary = chunk["summary"]
        sources = chunk.get("sources", [])
        source_text = "\n".join([
            f'- "{src["text"].strip()}"\n  (https://www.reddit.com{src["permalink"]})'
            for src in sources[:3]
        ])
        block = f"Summary: {summary}\nSources:\n{source_text}"
        blocks.append(block)

    joined = "\n\n".join(blocks)

    messages = [
        {
            "role": "system",
            "content": "You create a Reddit user persona from chunk summaries and Reddit comment citations."
        },
        {
            "role": "user",
            "content": f"""
Using only the chunk summaries and comment sources below, write a user persona for Reddit user '{username}'.

Do the following:
 - **Do not** mention "Chunk" or any placeholder labels. **Cite only actual comment or post URLs**.
1. Add a short, catchy **nickname** based on their traits (max 3 words).
2. Identify **3–5 personality traits**. For **each trait**, cite the relevant **comment or post** that supports it using the format:
   > "Quoted text from user"  
   > (https://reddit.com/actual_permalink)
   e.g.  
   +    Analytical Thinker — “I build cities at borders…”  
   +    (https://reddit.com/r/.../comment/abc123)
3. Include a section titled **Tone and Mindset** describing how the user communicates and what attitude they express.
4. Include a section titled **Additional Details** and infer the following, if possible:
   - **Age**: "Approximate age if known, else 'Not specified'",
   - **Status**: "e.g., casual Redditor, active contributor",
   - **Occupation**: "Inferred from posts, if any",
   - **Location** :"if mentioned or implied",
   - **Archetype** :"e.g., Analytical Thinker, Creative Idealist"
   

5. At the end, add a section titled **Likely Quote** with a short statement they might say that reflects their worldview or values:
 - "Quote": "Likely worldview quote"


Only use the **actual provided comment text and URL** as citations. Do not mention "Chunk 1" or general references. Cite only the actual post/comment text provided above.

Chunk Summaries and Sources:
{joined}
"""
        }
    ]

    return messages

def call_persona_llm(messages):
    res = openai.ChatCompletion.create(
        model = "mistralai/Mistral-7B-Instruct-v0.2",

        messages=messages,
        max_tokens=500,
        temperature=0.7
    )
    return res["choices"][0]["message"]["content"].strip()

def generate_persona(username):
    summaries = load_summaries(username)[:25]
    prompt = make_persona_prompt(summaries, username)
    raw_response = call_persona_llm(prompt)

    print(" Raw LLM response:")
    print(raw_response)

    #  parsing structured JSON
    try:
        data = json.loads(raw_response)
        result = raw_response
    except json.JSONDecodeError:
        print(" LLM response was not valid JSON. Using fallback.")
        data = {}

        def extract_field(field):
            pattern = rf"\*\*{field}:\*\*\s*(.+)"
            match = re.search(pattern, raw_response)
            return match.group(1).strip() if match else "Not specified"

        # Extract structured fields
        data["nickname"]   = extract_field("Nickname")
        data["age"]        = extract_field("Age")
        data["occupation"] = extract_field("Occupation")
        data["status"]     = extract_field("Status")
        data["location"]   = extract_field("Location")
        data["archetype"]  = extract_field("Archetype")
        data["quote"]      = extract_field("Likely Quote")

        # Smart autofills
        if data["status"] == "Not specified":
            data["status"] = "Likely an active Reddit commenter"

        if data["location"] == "Not specified":
            all_sources = [src for chunk in summaries for src in chunk.get("sources", [])]
            for src in all_sources:
                if "lucknow" in src.get("permalink", "").lower():
                    data["location"] = "Possibly India (Lucknow)"
                    break

        if data["archetype"] == "Not specified":
            data["archetype"] = data["nickname"].replace("-", " ").title()

        if data["age"] == "Not specified":
            data["age"] = "No clear age clue"

        if data["occupation"] == "Not specified":
            data["occupation"] = "No clear occupation clue"

        # Extract traits & tone sections
        traits_block = re.search(r"\*\*Personality Traits:\*\*(.+?)(\n\*\*|\Z)", raw_response, re.DOTALL)
        traits_text = traits_block.group(1).strip() if traits_block else "Not available."

        tone_block = re.search(r"\*\*Tone and Mindset:\*\*(.+?)(\n\*\*|\Z)", raw_response, re.DOTALL)
        tone_text = tone_block.group(1).strip() if tone_block else "Not available."

        # Rebuild output with traits first
        result = (
            f"**Personality Traits:**\n{traits_text}\n\n"
            f"**Tone and Mindset:**\n{tone_text}\n\n"
            f"**Nickname:** {data['nickname']}\n"
            f"**Age:** {data['age']}\n"
            f"**Occupation:** {data['occupation']}\n"
            f"**Status:** {data['status']}\n"
            f"**Location:** {data['location']}\n"
            f"**Archetype:** {data['archetype']}\n\n"
            f"**Likely Quote:** {data['quote']}"
        )

    # Save to output
    print("\n Final structured output:\n")
    print(result)

    user_folder = Path(f"output/{username}")
    user_folder.mkdir(parents=True, exist_ok=True)

    with open(user_folder / f"{username}_persona.txt", "w", encoding="utf-8") as f:
        f.write(result)

    with open(user_folder / f"{username}_persona.json", "w", encoding="utf-8") as f:
        json.dump({"username": username, "persona": data}, f, indent=2)

    print(f"Persona saved to: {user_folder}")


if __name__ == "__main__":
    generate_persona(username)


