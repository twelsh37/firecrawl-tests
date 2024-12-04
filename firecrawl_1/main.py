# Initial file to check Firecrawl functionality
# is working with our local installation
import os
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

from firecrawl import FirecrawlApp
from dotenv import load_dotenv

load_dotenv()

# Initialize the Firecrawl client with the local API URL
app = FirecrawlApp(
    api_key=os.getenv('FIRECRAWL_API_KEY'),
    api_url='http://localhost:3002'
)


# Crawl a website:
crawl_status = app.crawl_url(
  'https://books.toscrape.com/ ', 
  #Set up some parameters
  params={
    # limit the number of pages to crawl
    'limit': 1, 
    # specify the formats to scrape
    'scrapeOptions': {'formats': ['markdown']}
  },
  # Set the polling interval to 3 seconds for a quick run
  poll_interval=3
)

# Output the crawl status
print('Crawl status: ',crawl_status['status'])