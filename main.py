import os
from dotenv import load_dotenv
from google import genai

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API key from environment variables
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment variables")
        return
    
    try:
        # Initialize the Gemini client
        client = genai.Client(api_key=api_key)
        
        # Define the prompt
        prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
        
        # Generate content using the Gemini model
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=prompt
        )
        
        # Print the response text
        print("\nResponse:")
        print(response.text)
        
        # Print token usage
        if hasattr(response, 'usage_metadata'):
            print("\nToken Usage:")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
