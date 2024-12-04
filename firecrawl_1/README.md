# First test - A Simple Confidence Check
Initial file to check Firecrawl is working with our local installation. 
A simple confidence check
It queries books.toscrape.com  website and displays the crawl status.

We set up paramaters so that we only crawl 1 page and we return the results in markdown only.
We dont display the contents on this simple confidence check.

We set the 'poll_interval' to 3 seconds for a quick test. You might have to incrase this if you have a slow internet connection.

```
(firecrawl-tests-py3.12) E:\data\vscodeproject\firecrawl-tests\firecrawl_1>python main.py
Crawl status:  completed
```