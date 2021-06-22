# webScrape_futunn_stock
Grabs data from a specific stock's site on the platform at https://www.futunn.com and returns number of posts and comments starting from a certain date.

requiremetns:
  1.Python
    1.1 beautifulSoup
    1.2 selenium
    1.3 time
    1.4 datetime
  2.ChromeDriver
  3.Good internet connection

How to Run:
  1.Download .py file and put in same folder as chromedriver.exe file
  2.open command line from folder and type "python project.py"
  3.input a valid website corresponding to a stock on the site(e.g. https://www.futunn.com/stock/800100-HK)
  4.input valid Year Month Day for the date you want the program to start counting posts from
  5.wait for the program to run and return number of posts since 00:00 of that date.
