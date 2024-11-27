import os
from dotenv import load_dotenv
from main import ConversationalAI
from webscrape import extract_website_content  # Import the better scraping function
import glob

def main():
    # Load environment variables
    load_dotenv()
    
    # Get API key from environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Please set OPENAI_API_KEY environment variable")
    
    # Initialize the AI with the API key
    ai = ConversationalAI(api_key)
    
    # Get URLs from user input
    urls = []
    while True:
        url = input("Enter the URL to scrape (or 'no' to finish): ")
        if url.lower() == 'no':
            break
        urls.append(url)
    
    # Step 1: Scrape content and save to files
    for url in urls:
        try:
            print(f"Scraping: {url}")
            output_file = f"info/{url.split('/')[-2]}.txt"  # Create filename from URL
            extract_website_content(url, output_file)
            print(f"Saved to: {output_file}")
        except Exception as e:
            print(f"Error scraping {url}: {e}")
    
    # Step 2: Process all txt files in the info directory
    for file_path in glob.glob("info/*.txt"):
        print(f"\nProcessing: {file_path}")
        chunks = ai.get_text_chunks(file_path)  # Assuming this method exists in your ConversationalAI class
        print(f"File split into {len(chunks)} chunks")
        ai.process_file(file_path)
    
    # Step 3: Verify the number of documents
    print(f"Total documents in collection: {ai.collection.count()}")
    
    # Step 4: Chat with the AI
    print("\nChat with the AI (type 'quit' to exit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        
        response = ai.chat(user_input, max_tokens=300)
        print(f"AI: {response}")

if __name__ == "__main__":
    main() 