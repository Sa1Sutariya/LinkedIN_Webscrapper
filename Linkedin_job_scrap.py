# Import libraries and packages for the project 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import csv
import parameters
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
print('- Finish importing packages')
# Task 1: Login to Linkedin

# Task 1.1: Open Chrome and Access Linkedin login site
driver = webdriver.Chrome(parameters.path)
sleep(2)
url = 'https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin'
driver.get(url)
print('- Finish initializing a driver')
sleep(2)

# Task 1.2: Import username and password
username = parameters.linkedin_username
password = parameters.linkedin_password
print('- Finish importing the login credentials')
sleep(2)

# Task 1.2: Key in login credentials
email_field = driver.find_element_by_id('username')
email_field.send_keys(username)
print('- Finish keying in email')
# sleep(3)

password_field = driver.find_element_by_name('session_password')
password_field.send_keys(password)
print('- Finish keying in password')
# sleep(2)

# Task 1.2: Click the Login button
signin_field = driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button')
signin_field.click()
sleep(3)

print('- Finish Task 1: Login to Linkedin')

# For security check You will be uncomment
# sleep(30) 
# Task 2: Search for the profile we want to Job Portal
# Task 2.1: Locate the search bar element
sleep(6)
search_field = driver.find_element_by_xpath('//*[@class="search-global-typeahead__input"]')
# Task 2.2: Input the search query to the search bar
# search_query = input('What profile do you want to scrape? ')
search_query = parameters.search_query
search_field.send_keys(search_query)

# Task 2.3: Search
search_field.send_keys(Keys.RETURN)

print('- Finish Task 2: Search for profiles')

sleep(5)
job = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div[2]/section/div/nav/div/ul/li[1]/button')
job.click()

# First fully loaded
sleep(5)
X_path_1 = f'/html/body/div[5]/div[3]/div[4]/div/div/main/div/section[1]/div/div[7]/ul/li[1]/button'
All_page_1 = driver.find_element_by_xpath(X_path_1)
All_page_1.click()
sleep(2)
driver.find_element_by_tag_name('body').send_keys(Keys.HOME)
down = 0
while down < 75:
    driver.find_element_by_tag_name('body').send_keys(Keys.DOWN)
    # sleep(0.25)
    down = down+1

# Task 3: Scrape the URLs of the profiles
# Task 3.1: Write a function to extract the URLs of one page
def GetURL():

    lnks=driver.find_elements_by_tag_name("a")
    all_profile_URL = []
    for lnk in lnks:
        if "jobs/view" in lnk.get_attribute("href"):
            # print(lnk.get_attribute("href"))
            all_profile_URL.append(lnk.get_attribute("href"))
    return all_profile_URL

# Task 3.2: Navigate through many page, and extract the profile URLs of each page
input_page = parameters.input_page

URLs_all_page = []
for page in range(input_page):
    sleep(3)
    try:
        X_path = f'/html/body/div[5]/div[3]/div[4]/div/div/main/div/section[1]/div/div[7]/ul/li[{page+1}]/button'
        All_page = driver.find_element_by_xpath(X_path)
        All_page.click()
        sleep(5)
    except:
        X_path = f'/html/body/div[5]/div[3]/div[4]/div/div/main/div/section[1]/div/div[6]/ul/li[{page+1}]/button'
        All_page = driver.find_element_by_xpath(X_path)
        All_page.click()
        sleep(5)

    down = 0
    while down < 75:
        driver.find_element_by_tag_name('body').send_keys(Keys.DOWN)
        # sleep(0.25)
        down = down+1
    URLs_one_page = GetURL()
    sleep(2)
    URLs_all_page = URLs_all_page + URLs_one_page
    print(len(URLs_all_page))
    sleep(2)

print('- Finish Task 3: Scrape the URLs')


# Task 4: Scrape the data of 1 Linkedin profile, and write the data to a .CSV file
with open(parameters.file_name, 'w',  newline = '') as file_output:
    headers = ['Job Title', 'Company name', 'Job Detail', 'Location','URL', 'About the job']
    writer = csv.DictWriter(file_output, delimiter=',', lineterminator='\n',fieldnames=headers)
    writer.writeheader()
    for linkedin_URL in URLs_all_page:
        driver.get(linkedin_URL)
        # print('- Accessing profile: ', linkedin_URL)
        sleep(3)
        # page_source = BeautifulSoup(driver.page_source, "html.parser")
        # info_div = page_source.find('div',{'class':'flex-1 mr5'})
        try:
            Job_title = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[1]/div/div/div[1]/h1')
            # print(Job_title.text)

            Company_name = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[1]/div/div/div[1]/div[1]/span[1]/span[1]/a')
            # print(Company_name.text)

            location = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[1]/div/div/div[1]/div[1]/span[1]/span[2]')
            # print(location.text)

            job_disc = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[2]/article/div/div[1]/span')
            # print(job_disc.text)
            
            job_st = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[1]/div/div/div[1]/div[2]/ul/li[1]/span')
            # print(job_st.text)
            writer.writerow({headers[0]:Job_title.text, headers[1]:Company_name.text, headers[2]:job_st.text, headers[3]:location.text, headers[4]:linkedin_URL, headers[5]:job_disc.text})
            # print('\n')
        except:
            pass

print('Mission Completed!')
driver.quit()