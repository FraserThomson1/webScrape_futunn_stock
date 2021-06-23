from bs4 import BeautifulSoup
from selenium import webdriver
import selenium
import time
from datetime import date
from selenium.webdriver.chrome.options import Options

url = input("Enter url for stock: ")
target_year = int(input("Enter search year: "))
target_month = int(input("Enter search month: "))
target_day = int(input("Enter search day: "))
target_date = date(target_year, target_month, target_day)
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--log-level=3')
driver = webdriver.Chrome(options = chrome_options)

def get_comments_link(url):
	#try to load page
	try:
		driver.get(url)
	except selenium.common.exceptions.InvalidArgumentException:
		return None
	#get the page to display comments
	e = driver.find_elements_by_xpath("//*[text()='评论']");
	if len(e) == 0: return None
	e[0].click()
	#get html and extract link to comments
	pg_src = driver.page_source
	src = BeautifulSoup(pg_src,"html.parser")
	feed = src.find(title="feed")
	if feed == None: return None
	comments_link = feed.attrs['src']
	return comments_link

def check_time(time, current_date,target_date):
	days = (current_date - target_date).days
	if days == 0:
		if (time[1] == "minutes" and time[2] == "ago") or (time[0] == "Today"): 
			return True
	elif days == 1:
		if (time[1] == "minutes" and time[2] == "ago") or (time[0] == "Today") or (time[0]=="1" and time[1]=="day" and time[2]=="ago"):return True
	elif current_date.year == target_date.year:
		if len(time[0].split("-")) == 2:
			if date(current_date.year, int(time[0].split("-")[0]), int(time[0].split("-")[1])) >= target_date:return True 
		elif len(time[0].split("-")) != 3: return True 
	else:
		if len(time[0].split("-")) == 3:
			if date(int(time[0].split("-")[0]), int(time[0].split("-")[1]), int(time[0].split("-")[2])) >= target_date: return True
		else: return True
	return False

def find_target_comments(comments,current_date,target_date):
	for i in range(len(comments)):
		time = comments[i].find(class_="time").find("a").contents[0].split(" ")
		if not check_time(time, current_date, target_date):
			return comments[:i]
	return None 

def get_num_discussions(comment):
	discussions = comment.find_all(class_ = "js-commentItem")
	return len(discussions)

print("-------------------------------------------------------------------------------")
if(target_date>date.today()):
	print("Search date can not be later than current date.")
	driver.quit()
else:
	comments_link = get_comments_link(url)
	if comments_link == None:
		print("Please check if website is valid or quality of your internet connection.")
		driver.quit()
	else:
		current_date = date.today()
		#go to comments link
		driver.get(comments_link)
		time.sleep(5)
		#extract comments
		comments_html = BeautifulSoup(driver.page_source,"html.parser")
		comments = comments_html.find_all(class_="feedBox01 js-feedItem")
		#extract comments to be analysed
		target_comments = find_target_comments(comments,current_date,target_date)
		while target_comments == None:
			#try load more comments
			try:
				e = (driver.find_elements_by_xpath("//*[text()='More']")+driver.find_elements_by_xpath("//*[text()='Loading…']")+driver.find_elements_by_xpath("//*[text()='Reload']"))[0]; 
				e.click()
			except selenium.common.exceptions.ElementNotInteractableException: 
				print("Check your internet connection quality.")
				driver.quit()
				exit()
			#extract comments
			comments_html = BeautifulSoup(driver.page_source,"html.parser")
			comments = comments_html.find_all(class_="feedBox01 js-feedItem")
			#extract comments to be analysed
			target_comments = find_target_comments(comments,current_date,target_date)

		driver.quit()

		print("Total number of posts since %s/%s/%s/00:00 : %s posts\n"%(target_year,target_month,target_day,str(len(target_comments))))
		#get count of discussions under each comment
		for i in range(len(target_comments)):
			print("POST %i"%(i+1))
			print("time:%s"%(target_comments[i].find(class_="time").find("a").contents[0]))
			print("number of comments:%s\n"%(get_num_discussions(target_comments[i])))
input("\n\nPress Any Key to Exit.")