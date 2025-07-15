# summarize reddit data in chunks using openrouter llm 

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

CHUNK_SIZE = 5

def load_posts(username):
    with open(f"data/{username}.json", "r", encoding="utf-8") as f:
        return json.load(f)

def chunk_posts(posts, size=CHUNK_SIZE):
    return [posts[i:i+size] for i in range(0, len(posts), size)]

def summarize_chunk(chunk, username):
    texts = [p['body'] for p in chunk if 'body' in p and len(p['body'].strip()) > 20]
    combined_text = "\n\n".join(texts)
    if not combined_text:
        return "(chunk skipped: no useful content)"

    messages = [
        {"role": "system", "content": "Summarize Reddit user's behavior."}, #prompt for summarization
        {"role": "user", "content": f"Summarize this Reddit activity by user '{username}':\n{combined_text}"}
    ]

    res = openai.ChatCompletion.create(
        model = "mistralai/Mistral-7B-Instruct-v0.2",

        messages=messages,
        max_tokens=300,
        temperature=0.7
    )

    return res["choices"][0]["message"]["content"].strip()

def summarize_all(username):
    posts = load_posts(username)
    chunks = chunk_posts(posts)
    
    Path("summaries").mkdir(exist_ok=True)
    out_path = f"summaries/{username}_chunks.json"
    summaries = []

    for i, chunk in enumerate(chunks[:20]):  # Limit to first 20 chunks
        print(f". Summarizing chunk {i+1}...")
        try:
            summary = summarize_chunk(chunk, username)
        except Exception as e:
            print(f" Failed to summarize chunk {i+1}: {e}")
            continue  # Skip failed chunk
        
        sources = [
            {
                "text": p["body"][:100],
                "permalink": f"https://www.reddit.com{p.get('permalink', '')}"
            }
            for p in chunk if "body" in p and "permalink" in p and len(p["body"].strip()) > 20
        ]

        summaries.append({
            "chunk_id": f"Chunk {i+1}",
            "summary": summary,
            "sources": sources
        })

        # 🔁 Save after every chunk 
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(summaries, f, indent=2)

    print(f" Saved {len(summaries)} summaries to {out_path}")

if __name__ == "__main__":
    
    if not username:
        print(" Please enter a valid Reddit username.")
    else:
        summarize_all(username)
