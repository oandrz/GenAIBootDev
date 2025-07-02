import os
from openai import OpenAI


def main():
    # Ensure the OPENAI_API_KEY environment variable is set
    # Set your API key (alternatively, set OPENAI_API_KEY env var)

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "sk-5678ijklmnopabcd5678ijklmnopabcd5678ijkl"))

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"}
        ]
    )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
