import pandas as pd
import os

def save_transcripts_opinions(data, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    df = pd.DataFrame(data)
    output_file = os.path.join(output_dir, "post_update_opinions_pike.csv")
    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")
