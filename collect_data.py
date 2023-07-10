import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
    
# Configure Selenium webdriver
driver = webdriver.Chrome()

# Load the Glassdoor HTML page
driver.get("https://www.glassdoor.com/Job/data-scientist-jobs-SRCH_KO0,14.htm?clickSource=searchBox")

# Initialize a list to store job data
job_data = []

# Iterate over each page
for j in range(0,30):
    print("Page "+ str(j))

    # Wait for the job listings to load
    job_listings = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//li[@class='react-job-listing css-108gl9c eigr9kq3']")))

    # Iterate over each job listing
    for i, listing in enumerate(job_listings, start=1):
        print(j*30+i)
        try:
            listing.click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@data-test="jobTitle"]')))
            if(i==1 and j==0):
                try:
                    time.sleep(2)
                    driver.find_element(By.XPATH,"//button[@class='e1jbctw80 ei0fd8p1 css-1n14mz9 e1q8sty40']").click()
                    time.sleep(2)
                except NoSuchElementException:
                    pass
            job_name = listing.find_element(By.XPATH, '//div[@data-test="jobTitle"]').text
            company_element = listing.find_element(By.XPATH, '//div[@data-test="employerName"]').text
            x = company_element.split()
            company_rating = -1
            company_name = ""
            if(is_float(x[len(x)-1])):
                company_rating = x[len(x)-1]
                company_name = company_element[:-4]
            else:
                company_name = company_element
            job_location = listing.find_element(By.XPATH, '//div[@data-test="location"]').text
            job_salary = None
            try:
                job_salary = listing.find_element(By.XPATH, '//span[@data-test="detailSalary"]').text
            except NoSuchElementException:
                pass
                
            job_description = listing.find_element(By.XPATH, '//div[contains(@class, "jobDescriptionContent desc")]').text

            #Gather company details

            try:
                headquarters = driver.find_element(By.XPATH, '//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Headquarters"]//following-sibling::*').text
            except NoSuchElementException:
                headquarters = -1

            try:
                size = driver.find_element(By.XPATH, '//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Size"]//following-sibling::*').text
            except NoSuchElementException:
                size = -1

            try:
                founded = driver.find_element(By.XPATH, '//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Founded"]//following-sibling::*').text
            except NoSuchElementException:
                founded = -1

            try:
                type_of_ownership = driver.find_element(By.XPATH, '//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Type"]//following-sibling::*').text
            except NoSuchElementException:
                type_of_ownership = -1

            try:
                industry = driver.find_element(By.XPATH, '//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Industry"]//following-sibling::*').text
            except NoSuchElementException:
                industry = -1

            try:
                sector = driver.find_element(By.XPATH, '//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Sector"]//following-sibling::*').text
            except NoSuchElementException:
                sector = -1

            try:
                revenue = driver.find_element(By.XPATH, '//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Revenue"]//following-sibling::*').text
            except NoSuchElementException:
                revenue = -1

            try:
                competitors = driver.find_element(By.XPATH, '//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Competitors"]//following-sibling::*').text
            except NoSuchElementException:
                competitors = -1

            # Append job data to the list
            job_data.append([j*30+i, job_name, company_name, company_rating, job_location, job_salary, job_description, headquarters, size, founded, type_of_ownership, industry, sector, revenue, competitors])
        except Exception as e: 
            print(e)
            continue
    driver.find_element(By.XPATH,'//button[@data-test="pagination-next"]').click()
    time.sleep(3)

# Close the browser
driver.quit()

# Save job data to a CSV file
csv_filename = 'job_data.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Number', 'Job Name', 'Company', 'Rating', 'Location', 'Salary', 'Description','Headquarters','Size','Founded','Type of ownership','Industry','Sector','Revenue','Competitors'])
    writer.writerows(job_data)

print(f"Job data saved to '{csv_filename}'.")