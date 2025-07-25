# Scraper for HousePriceAnalysis

This is part of the project [HousePriceAnalysis](https://github.com/Yaroslav1405/HousePriceAnalysis). The data was scraped from _flatfy.ua_ and was freely accessible to everyone at the time of scraping. 

## Tools used
* Selenium - to open the web page and load all elements.
* Beautiful soup - to load the page source in the lxml format, and extract necessary data.
* Pandas - to create a dataframe file and concatenate results.
* Time - sleep between scraping processes to reduce load on the server. 
