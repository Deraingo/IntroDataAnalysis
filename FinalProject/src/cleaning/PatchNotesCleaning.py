import pandas as pd
import re
import os

patch_notes_dir = 'PatchNotes/'
version_pattern = r'(?i)update\s+\d+(\.\d+)*'

def clean_patch_notes(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()
    start_index = None
    for i, line in enumerate(lines):
        if re.search(version_pattern, line):
            start_index = i
            break

    if start_index is not None:
        cleaned_content = lines[start_index:]
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(cleaned_content)
        print(f"Cleaned {file_path}: Content before version removed.")
    else:
        print(f"Skipped {file_path}: No version number found.")
        
for filename in os.listdir(patch_notes_dir):
    if filename.endswith(".txt"):
        patch_file = os.path.join(patch_notes_dir, filename)
        clean_patch_notes(patch_file)



def load_weapon_names(filename):
    df = pd.read_csv(filename)
    return df.iloc[:, 0].dropna().tolist()

heavy_weapons = load_weapon_names('heavy_weapons.csv')
light_weapons = load_weapon_names('light_weapons.csv')
medium_weapons = load_weapon_names('medium_weapons.csv')

all_weapons = set(heavy_weapons + light_weapons + medium_weapons)
change_keywords = ["buff", "nerf", "increase", "reduce", "adjust", "improve", "decrease"]
def extract_weapon_changes(patch_file, weapon_names, change_keywords):
    changes = []
    with open(patch_file, 'r', encoding='utf-8', errors='ignore') as file:
        text = file.read()
        cleaned_text = re.sub(r'\s+', ' ', text)
        
        for weapon in weapon_names:
            pattern = rf"\b{re.escape(weapon)}\b.*?\b({'|'.join(change_keywords)})\b.*?([\d.,%+-]+.*?[\d.,%+-]*)?"
            matches = re.findall(pattern, cleaned_text, re.IGNORECASE)
            
            for match in matches:
                change_type = match[0]
                details = match[1].strip() if match[1] else "No numeric details provided"
                if change_type.lower() in ["buff", "increase", "improve"]:
                    change_direction = "Buff"
                elif change_type.lower() in ["nerf", "reduce", "decrease"]:
                    change_direction = "Nerf"
                else:
                    change_direction = "Adjust"
                changes.append((weapon, change_type, details, change_direction))
    
    return changes

patch_notes_dir = 'PatchNotes/'
all_changes = []
for filename in os.listdir(patch_notes_dir):
    if filename.endswith(".txt"):
        patch_file = os.path.join(patch_notes_dir, filename)
        changes = extract_weapon_changes(patch_file, all_weapons, change_keywords)
        patch_version = filename.split('.')[0]
        all_changes.extend([(patch_version, weapon, change_type, details, direction)
                            for weapon, change_type, details, direction in changes])

changes_df = pd.DataFrame(all_changes, columns=['Patch Version', 'Weapon', 'Change Type', 'Description', 'Direction'])
changes_df.to_csv("detailed_weapon_changes.csv", index=False)

