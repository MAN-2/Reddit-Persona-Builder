# This is the main pipeline which combines and calls all the scripts
import re
import os
import sharedusername

def extract_username(input_str):
    match = re.search(r"reddit\.com/user/([^/]+)/?", input_str)
    if match:
        return match.group(1)
    return input_str.strip()

if __name__ == "__main__":

    raw_input = input("Enter Reddit username or profile URL: ")
    username = extract_username(raw_input)

    if not username:
        print("❌ Username missing.")
        exit()

    sharedusername.set_username(username) #Username set in the sharedusername so that it can be acessed easily along all the scripts
    
    # Sequential pipeline for calling all the scripts
    print(f"\n 1.Scraping posts for user '{username}'...")
    os.system(f"python scrap[1].py {username}")

    print(f"\n 2. Summarizing chunks for user '{username}'...")
    os.system(f"python summarize[2].py {username}")

    print(f"\n 3. Generating final persona for user '{username}'...")
    os.system(f"python finalizepersona[3].py --user {username}")

    print(f"\n 4.Generating avatar image for '{username}'...")
    os.system(f"python genimage[4].py --user {username}")

    print(f"\n 5.Creating final persona card for '{username}'...")
    os.system(f"python combine[5].py --user {username}")

    print(f"\n Final CARD Generated '{username}'. Check the output folder!\n")
