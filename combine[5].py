# Persona Card Generator 

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import argparse
from sharedusername import set_username, get_username
import textwrap

# CLI args
parser = argparse.ArgumentParser()
parser.add_argument("--user", help="Reddit username")
args = parser.parse_args()

if args.user:
    set_username(args.user)
username = get_username()

def extract_field(text, label):
    lines = text.splitlines()
    for line in lines:
        line = line.strip()
        if line.startswith(f"**{label}:**") or line.startswith(f"- **{label}:**"):
            parts = line.split("**")
            if len(parts) >= 3:
                return parts[2].strip(": ").strip()
    return "Not specified"

def extract_quote(text):
    lines = text.splitlines()
    quote_lines = []
    capture = False
    for line in lines:
        if "**Likely Quote**" in line:
            capture = True
            continue
        if capture:
            if line.strip() == "":
                break
            quote_lines.append(line.strip())
    return " ".join(quote_lines).strip().strip('"')


def generate_persona_card(username):
    out_dir = Path(f"output/{username}")
    avatar_path = out_dir / f"avatar_{username}.png"
    persona_path = out_dir / f"{username}_persona.txt"

    if not avatar_path.exists() or not persona_path.exists():
        raise FileNotFoundError("Required files not found.")

    with open(persona_path, "r", encoding="utf-8") as f:
        text = f.read()

    name = username
    nickname = extract_field(text, "Nickname")
    age = extract_field(text, "Age")
    occupation = extract_field(text, "Occupation")
    status = extract_field(text, "Status")
    location = extract_field(text, "Location")
    archetype = extract_field(text, "Archetype")
    quote = extract_quote(text)

   
    avatar = Image.open(avatar_path).resize((256, 256))
    card = Image.new("RGB", (1024, 640), color=(245, 250, 255))
    draw = ImageDraw.Draw(card)
    font_path = r"E:\project\reddit\ttf\DejaVuSans.ttf"

    if not Path(font_path).exists():
        raise FileNotFoundError("Font not found.")

    title_font = ImageFont.truetype(font_path, 26)
    text_font = ImageFont.truetype(font_path, 18)
    quote_font = ImageFont.truetype(font_path, 16)

    #  avatar
    card.paste(avatar, (40, 40))

    #  info
    x = 320
    y = 40
    draw.text((x, y), f"Reddit Persona: {name}", font=title_font, fill="black")
    y += 40
    draw.text((x, y), f"Nickname: {nickname}", font=text_font, fill="black"); y += 30
    draw.text((x, y), f"Age: {age}", font=text_font, fill="black"); y += 30
    draw.text((x, y), f"Occupation: {occupation}", font=text_font, fill="black"); y += 30
    draw.text((x, y), f"Status: {status}", font=text_font, fill="black"); y += 30
    draw.text((x, y), f"Location: {location}", font=text_font, fill="black"); y += 30
    draw.text((x, y), f"Archetype: {archetype}", font=text_font, fill="black"); y += 40

   
    quote_wrapped = textwrap.wrap(f'"{quote}"', width=50)
    draw.text((x, y), "Likely Quote:", font=title_font, fill="black")
    y += 30
    for q in quote_wrapped:
        draw.text((x, y), q, font=quote_font, fill="black")
        y += 24

    out_path = out_dir / f"{username}_persona_card.png"
    card.save(out_path)
    print(f"Persona card saved to: {out_path}")

if __name__ == "__main__":
    generate_persona_card(username)
