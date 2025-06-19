import pandas as pd
import re
import streamlit as st

st.set_page_config(page_title="Market Data Query Tool")

st.title("Market Data Query Tool")

# Data setup
data = {
    "Region": [
        "GTA", "Greater Montréal", "Greater Vancouver", "SWO Region", "Calgary Region",
        "Edmonton Region", "Winnipeg Region", "Québec City Area", "Ottawa-Gatineau CMA",
        "Okanagan Valley", "Greater Victoria", "Saskatoon Metro Area", "Halifax CMA",
        "Regina CMA", "St. John's CMA", "Moncton Region", "Greater Fredericton"
    ],
    "CEO Serviceable Market": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17],
    "KEY Serviceable Market": [18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34],
    "TSB Serviceable Market": [35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51],
    "Total Serviceable Market": [52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68],
    "% of Total": [69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85]
}

df = pd.DataFrame(data)

# Query parser
def parse_query(query: str):
    query = query.lower()
    metric_map = {
        "ceo": "CEO Serviceable Market",
        "key": "KEY Serviceable Market",
        "tsb": "TSB Serviceable Market",
        "total": "Total Serviceable Market",
        "%": "% of Total",
        "percent": "% of Total",
        "percentage": "% of Total"
    }

    region_match = None
    for region in df['Region']:
        if region.lower() in query:
            region_match = region
            break

    metric_match = None
    for keyword, column in metric_map.items():
        if re.search(rf"\b{re.escape(keyword)}\b.*(available|serviceable)?\s*market", query):
            metric_match = column
            break

    if not region_match:
        return "Sorry, I couldn't recognize the region in your question."
    if not metric_match:
        return "Sorry, I couldn't recognize the market metric in your question."

    value = df.loc[df['Region'] == region_match, metric_match].values[0]
    return f"The {metric_match} for {region_match} is {value}."

# Streamlit interface
user_query = st.text_input("Ask a market data question:", "What is the TSB Serviceable Available Market for Calgary Region?")

if user_query:
    response = parse_query(user_query)
    st.write(response)
