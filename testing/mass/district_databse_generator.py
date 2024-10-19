# Imports
import requests
import pandas as pd
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import io



def decompose_district(soup):
    left = soup.find("td", class_="newblubg").find("span").get_text().split(".", 1)[1]
    type_ = soup.find("td", class_="newblubg right").get_text().strip()
    code = left[-9:-1].strip()
    name = left[:-10].strip()
    return [code, name, type_]


def decompose_school(soup):
    left = soup.find("td", class_="newblubg").find("span").get_text().split(":", 1)[1]
    type_ = soup.find("td", class_="newblubg right").get_text().strip()
    code = left[-9:-1].strip()
    name = left[:-10].strip()
    parent_code = code[:4] + "0000"
    return [code, name, type_, parent_code]



if __name__ == "__main__":

    # Reads html file
    with open("files\\public_school_districts.html", "r") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    # Finds newblubs
    newblubgs = soup.find_all("td", class_="newblubg right")
    trs = [n.parent for n in newblubgs]
    districts = list(map(decompose_district, trs)) 

    # Reads html file
    with open("files\\public_schools.html", "r") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    # Finds newblubs
    newblubgs = soup.find_all("td", class_="newblubg right")
    trs = [n.parent for n in newblubgs]
    schools = list(map(decompose_school, trs)) 

    # Create the pandas DataFrame 
    data = sorted(districts + schools, key=lambda x: x[0])
    df = pd.DataFrame(data, columns = ['code', 'name', 'type', 'parent_code']) 

    # Saves to CSV
    df.to_csv("schools_and_districts.csv", index=False)