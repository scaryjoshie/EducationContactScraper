# Imports
import requests
import pandas as pd
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import io

def save_html(html, file_name="testing.html"):
    with open(file_name, "w") as f:
        f.write(html)

# Gets response
s = HTMLSession()
ORG_CODE = "00260505"
response = s.get(f"https://profiles.doe.mass.edu/profiles/general.aspx?topNavId=1&orgcode={ORG_CODE}&orgtypecode=5&leftNavId=122&")
response.html.render()
s.close()

# Gets table
soup = BeautifulSoup(response.text, "html.parser")
save_html(soup.prettify())
table = soup.find("table", class_="t_detail")
df = pd.read_html(io.StringIO(table.prettify()))
print(df)