import tkinter as tk
from tkinter import filedialog, messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from bs4 import BeautifulSoup
import pandas as pd
import time
import os


def init_driver():
    service = FirefoxService(executable_path='C:\\Users\\Perfect\\MLT\\geckodriver.exe')
    driver = webdriver.Firefox(service=service)
    return driver


def scrape_amazon_product(url):
    driver = init_driver()
    driver.get(url)

    
    time.sleep(5)

    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

  
    try:
        title = soup.find('span', {'id': 'productTitle'}).get_text(strip=True)
    except AttributeError:
        title = 'N/A'

   
    try:
        price = soup.find('span', {'class': 'a-price-whole'}).get_text(strip=True)
    except AttributeError:
        price = 'N/A'

    try:
        description = soup.find('div', {'id': 'feature-bullets'}).get_text(strip=True)
    except AttributeError:
        description = 'N/A'

  
    try:
        reviews = soup.find('span', {'id': 'acrCustomerReviewText'}).get_text(strip=True)
    except AttributeError:
        reviews = 'N/A'

    return {
        'Title': title,
        'Price': price,
        'Description': description,
        'Reviews': reviews
    }


def scrape_multiple_urls(urls):
    data = []
    for url in urls:
        product_data = scrape_amazon_product(url)
        data.append(product_data)
    return data


def browse_file():
    filename = filedialog.askopenfilename(
        title="Select file",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )
    if filename:
        file_path.set(filename)


def load_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file.readlines()]
    return urls


def start_scraping():
    urls = []
    if url_entry.get():
        urls.append(url_entry.get().strip())
    elif file_path.get():
        urls = load_urls_from_file(file_path.get())
    else:
        messagebox.showerror("Error", "Please enter a URL or select a file.")
        return

    if not urls:
        messagebox.showerror("Error", "No URLs provided.")
        return

    try:
        scraped_data = scrape_multiple_urls(urls)
        df = pd.DataFrame(scraped_data)
        output_file = 'amazon_product_data.csv'
        df.to_csv(output_file, index=False)
        messagebox.showinfo("Success", f"Data saved to {output_file}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

app = tk.Tk()
app.title("Amazon Product Scraper")
tk.Label(app, text="Enter Amazon Product URL:").pack(pady=5)
url_entry = tk.Entry(app, width=50)
url_entry.pack(pady=5)


file_path = tk.StringVar()
tk.Button(app, text="Select File with URLs", command=browse_file).pack(pady=5)
tk.Entry(app, textvariable=file_path, width=50).pack(pady=5)
tk.Button(app, text="Start Scraping", command=start_scraping).pack(pady=20)
app.mainloop()
