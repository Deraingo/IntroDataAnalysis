import openai

openai.api_key = ""

def analyze_opinions(text, chunk_size=2000):
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    opinions = []
    for chunk in chunks:
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an assistant analyzing weapon data and opinions on the medium class for the game 'The Finals'."},
                    {"role": "user", "content": f"Extract detailed opinions about weapon balancing and overall opions on the pike 556 and how it performs after the 4.2.0 update for the game 'The Finals': {chunk}"}
        
                ],
                temperature=0.7,
                max_tokens=300
            )
            opinions.append(response.choices[0].message.content)
        except Exception as e:
            print(f"Error processing chunk: {e}")
            continue
    
    return " ".join(opinions)
