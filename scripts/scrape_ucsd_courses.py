#!/usr/bin/env python
# scrape_ucsd_courses.py
"""
此脚本用于自动抓取UCSD课程目录中研究生课程（200-299）的数据，
并将整合后的数据存为CSV文件以供后续数据分析和处理。
"""

import requests
from bs4 import BeautifulSoup
import csv
import re

# 目标URL（请根据实际情况调整）
url = "https://catalog.ucsd.edu/front/courses.html"

def fetch_course_data(url):
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, "html.parser")
    
    courses = []
    
    # 假设每门课程信息都位于<div class="course">中，
    # 课程编号、标题、描述分别在<span class="course-number">、<span class="course-title">、<div class="course-description">
    for course_div in soup.find_all("div", class_="course"):
        course_number_tag = course_div.find("span", class_="course-number")
        course_title_tag  = course_div.find("span", class_="course-title")
        course_desc_tag   = course_div.find("div", class_="course-description")
        
        if course_number_tag and course_title_tag:
            num_text = course_number_tag.get_text(strip=True)
            # 筛选200-299的研究生课程
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
    print(f"数据已保存至 {filename}")

if __name__ == "__main__":
    courses = fetch_course_data(url)
    if courses:
        save_to_csv(courses)
    else:
        print("未抓取到任何课程数据，请检查目标页面或选择器设置。")
