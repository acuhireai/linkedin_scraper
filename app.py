from linkedin_scraper import Person, Company, Job, actions
from selenium import webdriver
import os
from dotenv import load_dotenv
load_dotenv()


driver = webdriver.Chrome()


email = os.getenv("LINKEDIN_USER")
password = os.getenv("LINKEDIN_PASSWORD")
actions.login(driver, email, password)
# person = Person(
#     "https://www.linkedin.com/in/andre-iguodala-65b48ab5", driver=driver, close_on_complete=False)
# print(person)
# company = Company("https://ca.linkedin.com/company/google", driver=driver)
# print(company)

job = Job("https://www.linkedin.com/jobs/collections/recommended/?currentJobId=3456898261",
          driver=driver, close_on_complete=False)
