# VectorChat_Bot: Your Web Knowledge Assistant
A Python application that scrapes web content, processes it into chunks, and stores it in a vector database using OpenAI embeddings for semantic search and AI-powered conversations.

## Features

- Web scraping with intelligent content extraction
- Text chunking for optimal processing
- Vector storage using ChromaDB
- OpenAI embeddings for semantic search
- Interactive chat interface using GPT-4o
- Environment variable configuration for security

## Installation

1. Clone the repository:
```bash
git clone https://github.com/MonkWarrior08/WebVec-AI-Assistant.git
cd WebVec-AI-Assistant
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Run the main script:
```bash
python run.py
```

2. Enter URLs when prompted. Type 'no' when finished adding URLs.

3. The application will:
   - Scrape content from provided URLs
   - Save content to text files in the `info` directory
   - Process text into chunks
   - Store chunks in ChromaDB with OpenAI embeddings
   - Start an interactive chat session

4. Chat with the AI about the processed content. Type 'quit' to exit.

## Project Structure

```
├── run.py          # Main execution script
├── main.py         # ConversationalAI class implementation
├── webscrape.py    # Web scraping functionality
├── .env            # Environment variables
└── info/           # Directory for stored text files
```

## Configuration

The application uses the following default settings:
- Text chunk size: 1000 characters
- Embedding model: text-embedding-3-small
- Chat model: GPT-4o
- Vector store: ChromaDB
- Chat max-token: 300

## Error Handling

The application includes error handling for:
- Missing API keys
- Failed web scraping attempts
- Text processing errors
- Vector store operations

## License

This project is licensed under the MIT License - see the LICENSE file for details.
