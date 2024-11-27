import requests
from bs4 import BeautifulSoup
import html
from datetime import datetime

def clean_text(text):
    return ' '.join(text.strip().split())

def extract_website_content(url, output_file):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for element in soup(['script', 'style']):
            element.decompose()
            
        with open(output_file, 'w', encoding='utf-8') as f:
            # Write metadata
            f.write(f"URL: {url}\n")
            f.write(f"Extraction Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            
            # Extract and write title
            title = soup.title.string if soup.title else "No title"
            f.write(f"Title: {title}\n\n")
            f.write("=" * 80 + "\n\n")
            
            # Process content maintaining the natural flow
            main_content = soup.find(['main', 'article', 'div#content', 'div#main']) or soup.body
            
            def process_element(element):
                if isinstance(element, str):
                    text = clean_text(element)
                    if text:
                        f.write(f"{text}\n\n")
                    return

                if element.name in ['pre', 'code']:
                    code_text = html.unescape(element.get_text())
                    if code_text.strip():
                        f.write("```\n")
                        f.write(code_text.strip())
                        f.write("\n```\n\n")
                    return

                # Process text nodes directly inside this element
                for content in element.contents:
                    if isinstance(content, str):
                        text = clean_text(content)
                        if text:
                            f.write(f"{text}\n\n")
                    elif content.name in ['pre', 'code']:
                        code_text = html.unescape(content.get_text())
                        if code_text.strip():
                            f.write("```\n")
                            f.write(code_text.strip())
                            f.write("\n```\n\n")
                    elif content.name in ['p', 'div', 'section', 'article']:
                        process_element(content)
                    elif content.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                        text = clean_text(content.get_text())
                        if text:
                            f.write(f"\n{text}\n{'=' * len(text)}\n\n")
                    elif content.name in ['ul', 'ol']:
                        for li in content.find_all('li', recursive=False):
                            text = clean_text(li.get_text())
                            if text:
                                f.write(f"• {text}\n")
                        f.write("\n")

            # Start processing from the main content
            process_element(main_content)

        print(f"Content has been extracted and saved to {output_file}")
        
    except Exception as e:
        print(f"Error extracting content: {str(e)}")

