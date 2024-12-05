import os
import re 
import pandas as pd
import matplotlib.pyplot as plt

cleanedCsvsPath = "../../cleanedCsvs/"
outputGraphsPath = "../../graphs/"

os.makedirs(outputGraphsPath, exist_ok=True)

def extractVersionNumber(fileName):
    match = re.search(r'_(\d+\.\d+\.\d+)\.csv', fileName)
    return match.group(1) if match else "unknownVersion"

def sanitizeFilename(name):
    return re.sub(r'[<>:"/\\|?*]', '_', name)

def plotWeaponTrends(weaponClass, groupedDataColumns):
    weaponFiles = sorted([
        file for file in os.listdir(cleanedCsvsPath)
        if file.startswith(f"{weaponClass}_weapons_") and file.endswith(".csv")
    ], key=lambda x: tuple(map(int, extractVersionNumber(x).split('.'))) if extractVersionNumber(x) != "unknownVersion" else (0, 0, 0))

    if not weaponFiles:
        print(f"No data found for {weaponClass} weapons.")
        return

    print(f"Found files for {weaponClass} weapons: {weaponFiles}")
    trends = {column: {} for group in groupedDataColumns for column in group}

    for fileName in weaponFiles:
        version = extractVersionNumber(fileName)
        filePath = os.path.join(cleanedCsvsPath, fileName)
        print(f"Processing file: {filePath}")
        df = pd.read_csv(filePath)
        print(f"Columns in file: {df.columns.tolist()}")
        if "Damage Per Magazine" not in df.columns and "Body Damage" in df.columns and "Magazine Size" in df.columns:
            df["Damage Per Magazine"] = df["Body Damage"] * df["Magazine Size"]

        for group in groupedDataColumns:
            for column in group:
                if column in df.columns:
                    for weapon in df.iloc[:, 0]:
                        if weapon not in trends[column]:
                            trends[column][weapon] = []
                        value = df.loc[df.iloc[:, 0] == weapon, column].values
                        trends[column][weapon].append((version, value[0] if len(value) > 0 else None))

    for weapon in trends[groupedDataColumns[0][0]]:
        for group in groupedDataColumns:
            plt.figure(figsize=(10, 6))

            for column, color in zip(group, ['green', 'blue', 'red', 'purple'][:len(group)]):
                versions = [v for v, val in trends[column][weapon] if val is not None]
                values = [val for v, val in trends[column][weapon] if val is not None]
                plt.plot(versions, values, marker='o', label=column, color=color)

            groupName = " and ".join(group)
            plt.title(f"{groupName} Trends for {weapon} ({weaponClass.capitalize()} Weapons)")
            plt.xlabel("Version")
            plt.ylabel("Value")
            plt.xticks(rotation=45)
            plt.legend()
            plt.grid(True)
            sanitizedWeapon = sanitizeFilename(weapon)
            groupNameSanitized = "_".join(group).replace(" ", "_")
            outputFile = os.path.join(outputGraphsPath, f"{weaponClass}_{sanitizedWeapon}_{groupNameSanitized}_trends.png")
            plt.savefig(outputFile, bbox_inches="tight")
            plt.close()
            print(f"Plot saved at: {outputFile}")

if __name__ == "__main__":
    weaponClasses = ["light", "medium", "heavy"]
    groupedDataColumns = [
        ["Body Damage", "Head Damage"],  # Group 1
        ["Rate of Fire (RPM)"],          # Group 2
        ["Magazine Size"],               # Group 3
        ["Damage Per Magazine"]          # Group 4
    ]

    for weaponClass in weaponClasses:
        print(f"Processing {weaponClass} weapons...")
        plotWeaponTrends(weaponClass, groupedDataColumns)
