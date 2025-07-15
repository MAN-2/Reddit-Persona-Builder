# 🧠 Reddit Persona Builder

This project is a fun and insightful tool that builds a **complete personality profile of any public Reddit user**, based on their posts and comments.

It scrapes their recent Reddit activity, summarizes patterns using an LLM, and generates a **text-based persona profile** — complete with citations, a nickname, key traits, and a final **persona card image** with an auto-generated avatar.

---

## 💡 Features

- 🔍 **Scrapes Reddit comments and posts** using Reddit's public API.
- ✂️ **Chunks and summarizes data** with Mistral-7B via OpenRouter.
- 🧠 **Generates personality profiles** with traits, tone, and citations.
- 🧾 Outputs:
  - `persona.txt` – human-readable profile
  - `persona.json` – structured output
- 🖼️ **Creates an image-based persona card** with:
  - Auto-generated avatar (via Dicebear)
  - Clean background, title, and traits in image
- 🧪 Can be used to analyze influencers, job applicants, or for just fun!

---

## 🛠️ Tech Stack

- **Python** (scripting and orchestration)
- **OpenRouter + Mistral-7B** (for summarization and persona generation)
- **Dicebear API** (for avatar image generation — no cost or API key required )
- **Pillow** (for creating the final persona card image)
- **Reddit API (unauthenticated)** for scraping public content

---

## 🔄 Pipeline Flow

all.py

├── scrap[1].py → Get all comments & posts

├── summarize[2].py → Summarize in chunks with citations

├── finalizepersona[3].py → Generate final persona with traits + tone

├── genimage[4].py → Generate avatar using Dicebear

└── combine[5].py → Combine avatar + text into persona card image



---
## Screenshots:
![11](https://github.com/user-attachments/assets/6a517e06-8ddc-49b0-8647-143b210b909e)
![12](https://github.com/user-attachments/assets/8ab132e7-7ba1-44c8-b20b-1c559ba0e4d3)

<img width="1024" height="640" alt="kojied_persona_card" src="https://github.com/user-attachments/assets/744d2ed5-9b5a-44d0-b756-e19aa817f9a5" />


---

## 🖼️ Why Dicebear?

While testing,  I explored **Replicate’s image generation models**, but it required billing for continued use.

Instead, I switched to [**Dicebear API**](https://www.dicebear.com/) which:
- Is **free**
- Doesn’t need an API key
- Still gives a unique avatar for every user

---

## 🚀 How to Run

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/reddit-persona-builder.git
   cd reddit-persona-builder
Install dependencies:

pip install -r requirements.txt
Run the full pipeline:
python all.py

Enter the Reddit username (or full profile URL) when prompted.

Done! Check the output/<username>/ folder for:

Summary chunks JSON

Final persona (TXT + JSON)

Auto-generated avatar image

Final persona card PNG
---
📝 Example Output
output/kojied/kojied_persona.txt – personality writeup

output/kojied/avatar_kojied.png – avatar image

output/kojied/kojied_persona_card.png – full graphic card

