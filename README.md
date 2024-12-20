# LinkedIn-Job-Scraper-No-Login-Required
This project is a Python-based web scraper that fetches job postings from LinkedIn without requiring user authentication. It extracts job details such as title, company name, location, posting time, and description using public APIs and web scraping techniques. The scraped data is saved in a CSV file for easy analysis.
Features
Scrapes LinkedIn jobs without needing to log in.
Extracts key job details:
Job title
Company name
Location
Time posted
Number of applicants
Full job description
Saves the results in a CSV file for further analysis.
Includes error handling and logging for failed requests.
Mimics browser behavior with custom headers to avoid detection.
Technologies Used
Python: Core programming language.
BeautifulSoup: For HTML parsing and data extraction.
Requests: For making HTTP requests.
Pandas: To handle and save the scraped data.
Logging: For error tracking and debugging.
How to Use
Clone the repository:
bash
Copier le code
git clone https://github.com/yourusername/linkedin-job-scraper.git
Navigate to the project directory:
bash
Copier le code
cd linkedin-job-scraper
Install the required dependencies:
bash
Copier le code
pip install -r requirements.txt
Run the script:
bash
Copier le code
python scraper.py
Enter the desired job title and location when prompted.
View the saved CSV file (linkedin_jobs.csv) in the project directory.
Prerequisites
Python 3.x installed.
Libraries: beautifulsoup4, requests, pandas.
Important Notes
The scraper is designed for educational purposes only. Ensure compliance with LinkedIn's terms of service.
Avoid excessive scraping to prevent getting blocked.
Output Example
The generated CSV file will contain columns such as:

job_title
company_name
location
time_posted
num_applicants
description
job_url
job_id
