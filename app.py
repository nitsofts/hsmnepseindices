from fastapi import FastAPI
from fastapi.responses import JSONResponse
from bs4 import BeautifulSoup
from pyppeteer import launch

app = FastAPI()

# Function to scrape and extract the data using Pyppeteer
async def scrape_data(url):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)

    # You may need to add some delay here to ensure the page loads completely.
    await page.waitFor(5000)  # Waits for 5 seconds

    html = await page.content()
    await browser.close()

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

@app.get('/get_nepse_indices')
async def get_indices():
    url = "https://merolagani.com/MarketSummary.aspx"
    data = await scrape_data(url)
    indices_data = [entry for entry in data if entry["indexType"] == "Indices"]
    return JSONResponse(content=indices_data)

@app.get('/get_nepse_sub_indices')
async def get_sub_indices():
    url = "https://merolagani.com/MarketSummary.aspx"
    data = await scrape_data(url)
    sub_indices_data = [entry for entry in data if entry["indexType"] == "Sub Indices"]
    return JSONResponse(content=sub_indices_data)

@app.get('/get_nepse_indices_and_sub_indices')
async def get_indices_and_sub_indices():
    url = "https://merolagani.com/MarketSummary.aspx"
    data = await scrape_data(url)
    return JSONResponse(content=data)
