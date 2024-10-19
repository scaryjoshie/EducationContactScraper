# Imports
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import io

# Reads df 
status_df = pd.read_csv("files\\status.csv", dtype=str)

# Creates HTML session
s = HTMLSession()

# Iterates over rows
for index, row in status_df.iterrows():

    if row["status"] != "success":

        try:
            # Vars
            code = row["code"]
            status = row["status"]

            # Makes HTML request
            response = s.get(f"https://profiles.doe.mass.edu/profiles/general.aspx?topNavId=1&orgcode={code}&orgtypecode=5&leftNavId=122&")
            #response.html.render()

            # Gets pandas df
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table", class_="t_detail")
            df = pd.read_html(io.StringIO(table.prettify()))[0]
            df.insert(0, "code", code)
            df.rename(columns={"Function": "function", "Contact Name":"name", "Email":"email", "Phone":"phone", "Fax":"fax"}, inplace=True)

            # Saves to csv
            df.to_csv(f"files\\downloads\\{code}.csv", index=False)

            # Updates status file
            status_df.iloc[index,1] = "success"
            status_df.to_csv("files\\status.csv", index=False)

        except Exception as e:
            print(e)
            # Updates status file
            status_df.iloc[index,1] = "failure"
            status_df.to_csv("files\\status.csv", index=False)
        
        # Sleeps
        #time.sleep(1)


# Closes s
s.close()