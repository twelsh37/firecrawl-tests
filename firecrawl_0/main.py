# Initial file to check Firecrawl functionality
# is working with our local installation

# We will be using scrape_url as we will pe pulling a single UTL not a complete site
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

import os
from firecrawl import FirecrawlApp
from dotenv import load_dotenv

load_dotenv()

# Initialize the Firecrawl client with the local API URL
app = FirecrawlApp(
    api_key=os.getenv('FIRECRAWL_API_KEY'),
    api_url='http://localhost:3002'
)


# Scrape a URL:
crawl_status = app.scrape_url('books.toscrape.com', params={'formats': ['markdown']})

# Output the crawl status
print(f'\nHere are the scrape results: \n\n{crawl_status}')