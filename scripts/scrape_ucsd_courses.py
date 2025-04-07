#!/usr/bin/env python
# scrape_ucsd_courses.py
"""
This script automatically scrapes UCSD course catalog data for graduate courses (200-299),
and saves the consolidated data into a CSV file for further analysis and processing.
"""

import requests
from bs4 import BeautifulSoup
import csv
import re

# Target URL (please adjust based on the actual URL)
url = "https://catalog.ucsd.edu/front/courses.html"

def fetch_course_data(url):
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, "html.parser")
    
    courses = []
    
    # Assuming each course's information is contained in a <div class="course"> element,
    # with the course number, title, and description in <span class="course-number">,
    # <span class="course-title">, and <div class="course-description"> respectively.
    for course_div in soup.find_all("div", class_="course"):
        course_number_tag = course_div.find("span", class_="course-number")
        course_title_tag = course_div.find("span", class_="course-title")
        course_desc_tag = course_div.find("div", class_="course-description")
        
        if course_number_tag and course_title_tag:
            num_text = course_number_tag.get_text(strip=True)
            # Filter for graduate courses with numbers in the 200-299 range
            if re.match(r"^2\d\d", num_text):
                courses.append({
                    "number": num_text,
                    "title": course_title_tag.get_text(strip=True),
                    "description": course_desc_tag.get_text(strip=True) if course_desc_tag else ""
                })
    return courses

def save_to_csv(courses, filename="ucsd_graduate_courses.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["number", "title", "description"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for course in courses:
            writer.writerow(course)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    courses = fetch_course_data(url)
    if courses:
        save_to_csv(courses)
    else:
        print("No course data was retrieved. Please check the target page or selector settings.")
