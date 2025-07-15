# generating the image for avatar
import requests
from pathlib import Path
import argparse
from sharedusername import set_username, get_username


parser = argparse.ArgumentParser() #cli input 
parser.add_argument("--user", help="Reddit username")
args = parser.parse_args()


if args.user:
    set_username(args.user)
username = get_username()


def generate_avatar_image(username):
    style = "adventurer"  # style provided by dicebear
    url = f"https://api.dicebear.com/8.x/{style}/png?seed={username}" # using Api of Dicebear to create image avatar 

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to download avatar: {response.status_code}")

    out_dir = Path(f"output/{username}")
    out_dir.mkdir(parents=True, exist_ok=True)

    img_path = out_dir / f"avatar_{username}.png"
    with open(img_path, "wb") as f:
        f.write(response.content)

    print(f"Avatar saved to: {img_path}")
    return str(img_path)



if __name__ == "__main__":
    generate_avatar_image(username)
