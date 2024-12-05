import os
import pandas as pd

csv_data_path = "../../csvData/" 
cleaned_csvs_path = "../../cleanedCSVs/" 
os.makedirs(cleaned_csvs_path, exist_ok=True)

def clean_weapon_data(file_path):
    df = pd.read_csv(file_path)
    df.iloc[:, 0] = df.iloc[:, 0].str.strip()
    
    try:
        light_idx = df[df.iloc[:, 0].str.contains('Light', case=False, na=False)].index[0]
        medium_idx = df[df.iloc[:, 0].str.contains('Medium', case=False, na=False)].index[0]
        heavy_idx = df[df.iloc[:, 0].str.contains('Heavy', case=False, na=False)].index[0]
        light_weapons = df.iloc[light_idx + 1:medium_idx]
        medium_weapons = df.iloc[medium_idx + 1:heavy_idx]
        heavy_weapons = df.iloc[heavy_idx + 1:]

        return light_weapons, medium_weapons, heavy_weapons
    except IndexError:
        print(f"Error: Could not find all weapon categories in {file_path}.")
        return None, None, None

def extract_version_number(file_name):
    import re
    match = re.search(r'\(([\d\.]+)\)', file_name)
    return match.group(1) if match else "unknown_version"
for file_name in os.listdir(csv_data_path):
    if file_name.startswith("[THE FINALS]Zafferman'sWeaponMasterSheet") and file_name.endswith(".csv"):
        file_path = os.path.join(csv_data_path, file_name)
        print(f"Processing {file_name}...")
        version_number = extract_version_number(file_name)
        light_weapons, medium_weapons, heavy_weapons = clean_weapon_data(file_path)
        
        if light_weapons is not None:
            light_weapons.to_csv(os.path.join(cleaned_csvs_path, f"light_weapons_{version_number}.csv"), index=False)
            medium_weapons.to_csv(os.path.join(cleaned_csvs_path, f"medium_weapons_{version_number}.csv"), index=False)
            heavy_weapons.to_csv(os.path.join(cleaned_csvs_path, f"heavy_weapons_{version_number}.csv"), index=False)
            print(f"Saved cleaned data for version {version_number}.")
        else:
            print(f"Skipping {file_name} due to missing data.")
