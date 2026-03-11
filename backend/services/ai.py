import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_summary(data):

    prompt = f"""
You are a sales analyst.

Analyze the dataset and produce a short executive summary.

Dataset:
{data}

Mention:
- revenue insights
- strongest region
- best product category
"""

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return completion.choices[0].message.content