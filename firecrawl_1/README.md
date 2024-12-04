# Second test - A Simple Confidence Check of crawl_url
In the previous example in firecrawl_0, we used scrape_url. This is a simple utility to pull a single URL.
Form now on we will be using the much more configurable crawl_url
lets carry out a quick confidence check to ensure firecrawl, and specificaly 'crawl_url', are functioning as expected.

We will query books.toscrape.com website and displays the crawl status.

We set up paramaters so that we only crawl 1 page and we return the results in markdown only.
We dont display the contents on this simple confidence check.

We set the 'poll_interval' to 3 to speed up the test.

```
(firecrawl-tests-py3.12) E:\data\vscodeproject\firecrawl-tests\firecrawl_1>python main.py
Crawl status:  completed
```