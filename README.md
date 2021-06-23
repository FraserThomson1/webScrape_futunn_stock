# webScrape_futunn_stock
Grabs data from a specific stock's site on the platform at https://www.futunn.com and returns number of posts and comments starting from a certain date.

requirements:
 1. Python and Python libraries
    - beautifulSoup
    - selenium
    - time
    - datetime
  2. ChromeDriver
  3. Good internet connection

How to Run:
  1. Download .py file and appropriate version of chromedriver
  2. Add location of chromedriver to PATH variable
  3. Open command line from folder and type "python project.py"
  4. Input a valid website corresponding to a stock on the site(e.g. https://www.futunn.com/stock/800100-HK)
  5. Input valid Year Month Day for the date you want the program to start counting posts from
  6. Wait for the program to run and return number of posts since 00:00 of that date.
