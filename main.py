import csv
import io
import os

import requests
import streamlit as st
from requests.auth import HTTPBasicAuth

ASTAR_NETWORK_ID = 592
AD_CONTRACT_ADDRESS = "0xd59fC6Bfd9732AB19b03664a45dC29B8421BDA9a"
ENDPOINT = f"https://api.covalenthq.com/v1/{ASTAR_NETWORK_ID}/tokens/{AD_CONTRACT_ADDRESS}/token_holders/"
API_KEY = os.environ.get("COVALENT_API_KEY")

st.subheader("AstarDegens Holders")


@st.spinner("Querying holders...")
@st.cache(persist=True, ttl=6, show_spinner=False)
def fetch_data():
    auth = HTTPBasicAuth(API_KEY, "")
    page_number = 0
    page_size = 1000
    holders = []
    has_more = True
    while has_more:
        page = requests.get(ENDPOINT,
                            params={"page-number": page_number,
                                    "page-size": page_size},
                            headers={"Accept": "application/json"},
                            auth=auth)

        data = page.json()["data"]
        pagination = data["pagination"]
        page_number = pagination["page_number"] + 1
        has_more = pagination["has_more"]

        items = data["items"]
        holders.extend([{"address": item["address"], "balance": item["balance"]}
                        for item in items])

    return holders


ad_holders = fetch_data()
st.dataframe(ad_holders)

output = io.StringIO()
writer = csv.DictWriter(output, fieldnames=["address", "balance"])
writer.writerows(ad_holders)

st.download_button(label="Export", data=output.getvalue(), file_name="ad_holders.csv")
