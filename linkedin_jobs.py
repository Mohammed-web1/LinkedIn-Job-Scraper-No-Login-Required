from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import logging

# Configure logging
logging.basicConfig(
    filename="scraping_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Input job title and location
title = input("Enter job title: ").strip()
location = input("Enter location: ").strip()

# Initial pagination starting point
start = 0  

# Base URL for LinkedIn job search (guest API)
base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={title}&location={location}&start={start}"

# Headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Initialize a list to store job IDs
id_list = []

# Pagination loop (adjust range as needed)
while start < 100:  # Adjust the number of jobs/pages to scrape
    # Format the URL with current parameters
    url = base_url.format(title=title, location=location, start=start)
    
    # Send a GET request
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch data from {url}: {e}")
        break

    # Parse the response HTML
    list_soup = BeautifulSoup(response.text, "html.parser")
    page_jobs = list_soup.find_all("li")

    # Extract job IDs
    for job in page_jobs:
        try:
            base_card_div = job.find("div", {"class": "base-card"})
            job_id = base_card_div.get("data-entity-urn").split(":")[3]
            id_list.append(job_id)
        except AttributeError:
            continue

    # Increment pagination
    start += 25  # Adjust increment as needed

    # Stop if we've gathered 100 job IDs
    if len(id_list) >= 1000:
        break

    # Add a delay to avoid overwhelming the server
    time.sleep(2)

# Initialize a list to store job details
job_list = []

# Extract details for each job ID
for index, job_id in enumerate(id_list[:100], 1):  # Limit to first 100 job IDs
    job_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
    try:
        job_response = requests.get(job_url, headers=headers)
        job_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch job details for ID {job_id}: {e}")
        continue

    job_soup = BeautifulSoup(job_response.text, "html.parser")
    job_post = {}

    # Extract job details
    try:
        job_post["job_title"] = job_soup.find("h2", {"class": "top-card-layout__title"}).text.strip()
    except AttributeError:
        job_post["job_title"] = None

    try:
        job_post["company_name"] = job_soup.find("a", {"class": "topcard__org-name-link"}).text.strip()
    except AttributeError:
        job_post["company_name"] = None

    try:
        job_post["time_posted"] = job_soup.find("span", {"class": "posted-time-ago__text"}).text.strip()
    except AttributeError:
        job_post["time_posted"] = None

    try:
        job_post["num_applicants"] = job_soup.find("span", {"class": "num-applicants__caption"}).text.strip()
    except AttributeError:
        job_post["num_applicants"] = None

    try:
        description_div = job_soup.find("div", {"class":"show-more-less-html__markup relative overflow-hidden"})
        links = description_div.find_all("a")
        for link in links:
            link.replace_with(link.text)
        job_post["description"] = description_div.text.strip()
    except AttributeError:
        job_post["description"] = None

    try:
        job_post["location"] = job_soup.find("span", {"class": "topcard__flavor"}).text.strip()
    except AttributeError:
        job_post["location"] = None

    try:
        rh_span = job_soup.find("span", {"aria-hidden": "true"})
        job_post["rh"] = rh_span.text.strip() if rh_span else None
    except AttributeError:
        job_post["rh"] = None

    job_post["job_url"] = job_url
    job_post["job_id"] = job_id

    job_list.append(job_post)

    # Show progress
    print(f"Processed {index}/{len(id_list[:100])} jobs.")

    # Add a delay to avoid overwhelming the server
    time.sleep(1)

# Convert job list to a DataFrame
jobs_df = pd.DataFrame(job_list)

# Save to CSV with metadata
csv_file_name = "linkedin_jobs.csv"
jobs_df.to_csv(csv_file_name, index=False)

print(f"Job data saved to {csv_file_name}")
