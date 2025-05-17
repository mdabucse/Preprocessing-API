import requests
from process import company, individual, interactions, lead
import json
def build_standardized_data(raw_data_dict):
    standardized_data = {
        'companies': [],
        'individuals': [],
        'interactions': [],
        'leads_opportunities': []
    }

    if 'companies' in raw_data_dict:
        for raw_company in raw_data_dict['companies']:
            processed_company = company(raw_company)
            standardized_data['companies'].append(processed_company)

    if 'individuals' in raw_data_dict:
        for raw_individual in raw_data_dict['individuals']:
            processed_individual = individual(raw_individual)
            standardized_data['individuals'].append(processed_individual)

    if 'interaction_logs' in raw_data_dict:
        for raw_interaction in raw_data_dict['interaction_logs']:
            processed_interaction = interactions(raw_interaction)
            standardized_data['interactions'].append(processed_interaction)

    if 'leads_opportunities' in raw_data_dict:
        for raw_opportunity in raw_data_dict['leads_opportunities']:
            processed_opportunity = lead(raw_opportunity)
            standardized_data['leads_opportunities'].append(processed_opportunity)

    return standardized_data

# --- Fetch data from JSONBlob API ---
def fetch_data_from_api(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error for bad responses (4xx, 5xx)
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return {}

# --- Main Execution ---
if __name__ == "__main__":
    api_url = "https://jsonblob.com/api/jsonBlob/1371358746827218944"
    raw_data = fetch_data_from_api(api_url)

    if raw_data and 'raw_data' in raw_data:
        result = build_standardized_data(raw_data['raw_data'])

        with open(r"A:\Adya\useful\Data\processed\output.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

        print("Standardized data saved to 'output.json'")
    else:
        print("Invalid or empty raw_data received.")