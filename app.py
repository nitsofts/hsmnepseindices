from flask import Flask, request, jsonify
from selenium import webdriver
from bs4 import BeautifulSoup
import time


app = Flask(__name__)

# Function to scrape and extract the data using Selenium
def scrape_data(url):
    chrome_driver_path = './chromedriver.exe'
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)
    driver.get(url)
    
    # You may need to add some delay here to ensure the page loads completely.
    time.sleep(5)
    
    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')
    data = []

    # Your code for scraping the data from the soup goes here
    # Extract the Indices data
    indices_table = soup.find('table', {'class': 'table-index', 'data-live': 'index-summary-only'})
    if indices_table:
        time_element = indices_table.find_previous('span', {'class': 'label label-default pull-right'})
        if time_element:
            time = time_element.get_text().replace("As of ", "")
            rows = indices_table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) == 4:
                    index_name = cols[0].get_text()
                    index_value = cols[1].get_text()
                    percent_change = cols[3].get_text()
                    # Filter out elements with empty text
                    if index_name and index_value and percent_change:
                        data.append({
                            "indexName": index_name,
                            "indexValue": index_value,
                            "percentChange": percent_change,
                            "asOfTime": time,
                            "indexType": "Indices"
                        })

    # Extract the Sub Indices data
    subindices_table = soup.find('table', {'class': 'table-index', 'data-live': 'subindex-summary'})
    if subindices_table:
        time_element = subindices_table.find_previous('span', {'class': 'label label-default pull-right'})
        if time_element:
            time = time_element.get_text().replace("As of ", "")
            rows = subindices_table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) == 4:
                    index_name = cols[0].get_text()
                    index_value = cols[1].get_text()
                    percent_change = cols[3].get_text()
                    # Filter out elements with empty text
                    if index_name and index_value and percent_change:
                        data.append({
                            "indexName": index_name,
                            "indexValue": index_value,
                            "percentChange": percent_change,
                            "asOfTime": time,
                            "indexType": "Sub Indices"
                    })
    
    return data

@app.route('/get_nepse_indices', methods=['GET'])
def get_indices():
    data = scrape_data("https://merolagani.com/MarketSummary.aspx")
    indices_data = [entry for entry in data if entry["indexType"] == "Indices"]
    return jsonify(indices_data)

@app.route('/get_nepse_sub_indices', methods=['GET'])
def get_sub_indices():
    data = scrape_data("https://merolagani.com/MarketSummary.aspx")
    sub_indices_data = [entry for entry in data if entry["indexType"] == "Sub Indices"]
    return jsonify(sub_indices_data)

@app.route('/get_nepse_indices_and_sub_indices', methods=['GET'])
def get_indices_and_sub_indices():
    data = scrape_data("https://merolagani.com/MarketSummary.aspx")
    return jsonify(data)

if __name__ == '__main__':
    app.run()
