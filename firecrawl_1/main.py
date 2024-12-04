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
  'https://www.theaiaa.com', 
  params={
    'limit': 3, 
    'scrapeOptions': {'formats': ['markdown', 'html']}
  },
  poll_interval=30
)
print(crawl_status)