from openai import OpenAI
import os
from dotenv import load_dotenv

#openai.api_key = 'your_api_key'
load_dotenv()
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

def generate_description(table_name, columns):
    prompt = f"Describe the purpose and contents of a database table named '{table_name}' with the following columns:\n"
    for column in columns:
        prompt += f"- {column['name']} ({column['type']})\n"
    prompt += "\nProvide a concise description in 2-3 sentences."

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content":prompt,
            }
        ],
        max_tokens=150,
        model="gpt-3.5-turbo",
    )

    return response.choices[0].text.strip()

# Usage
table_name = "customer_orders"
columns = [
    {"name": "order_id", "type": "INTEGER"},
    {"name": "customer_id", "type": "INTEGER"},
    {"name": "order_date", "type": "DATE"},
    {"name": "total_amount", "type": "DECIMAL(10,2)"}
]

description = generate_description(table_name, columns)
print(description)