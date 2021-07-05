#developed by fraser thomson
from bs4 import BeautifulSoup
from selenium import webdriver
import selenium
import time
from datetime import date
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--log-level=3')
terminate = "n"

def get_comments_link(url):
	#try to load page
	try:
		#display page with comments
		driver.get(url+"/comments")
	except selenium.common.exceptions.InvalidArgumentException:
		return None
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
	for i in range(len(comments)-1,-1,-1):
		time = comments[i].find(class_="time").find("a").contents[0].split(" ")
		if check_time(time, current_date, target_date):
			if i == len(comments)-1:
				return None
			else:
				return comments[:i+1] 

def get_num_discussions(comment):
	discussions = comment.find_all(class_ = "js-commentItem")
	return len(discussions)


while terminate == "n":
	print("-------------------------------------------------------------------------------")
	url = input("Enter url for stock: ")
	try:
		target_year = int(input("Enter search year: "))
		target_month = int(input("Enter search month: "))
		target_day = int(input("Enter search day: "))
		target_date = date(target_year, target_month, target_day)
	except ValueError:
		print("\ndate entered has invalid value.")
	else:
		start_time = time.time()
		if(target_date>date.today()):
			print("\nSearch date cannot be later than current date.")
		else:
			driver = webdriver.Chrome(options = chrome_options)
			print("\n")
			comments_link = get_comments_link(url)
			if comments_link == None:
				print("\nPlease check if website is valid or quality of your internet connection.")
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
				stop = False
				while target_comments == None and not stop:
					#try load more comments
					try:
						e = (driver.find_elements_by_xpath("//*[text()='More']")+driver.find_elements_by_xpath("//*[text()='Loading…']")+driver.find_elements_by_xpath("//*[text()='Reload']"))[0]; 
						e.click()
					except selenium.common.exceptions.ElementNotInteractableException: 
						print("\nCheck your internet connection quality.")
						stop = True
					else:
						#extract comments
						comments_html = BeautifulSoup(driver.page_source,"html.parser")
						comments = comments_html.find_all(class_="feedBox01 js-feedItem")
						#extract comments to be analysed
						target_comments = find_target_comments(comments,current_date,target_date)

				driver.quit()
				end_time = time.time()
				if not stop:
					print("\nTotal number of posts since %s/%s/%s/00:00 : %s posts\n"%(target_year,target_month,target_day,str(len(target_comments))))
					#get count of discussions under each comment
					for i in range(len(target_comments)):
						print("POST %i"%(i+1))
						print("time:%s"%(target_comments[i].find(class_="time").find("a").contents[0]))
						print("number of comments:%s\n"%(get_num_discussions(target_comments[i])))
	print("time taken: %s seconds"%(end_time-start_time))
	terminate = input("\n\nTerminate program?(y/n):")