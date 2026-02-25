import requests
import os

class SuperteamClient:
    BASE_URL = "https://superteam.fun"

    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def get_live_listings(self, take=50):
        """
        Fetches live listings from the Superteam API.
        """
        url = f"{self.BASE_URL}/api/agents/listings/live"
        params = {"take": take} # Removed deadline as it might be causing 400 error
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Failed to fetch listings: {e}")
            return []

    def create_submission(self, listing_id, link, telegram, other_info):
        """
        Submits an entry to the Superteam API.
        Returns: (result_json, error_message)
        """
        url = f"{self.BASE_URL}/api/agents/submissions/create"
        payload = {
            "listingId": listing_id,
            "link": link,
            "telegram": telegram,
            "otherInfo": other_info,
            "eligibilityAnswers": [],
            "ask": None
        }
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            if response.status_code >= 400:
                error_detail = response.text
                try:
                    error_json = response.json()
                    error_detail = error_json.get("error", {}).get("message", error_detail)
                except:
                    pass
                return None, f"API Error {response.status_code}: {error_detail}"
            
            return response.json(), None
        except Exception as e:
            return None, f"Connection Error: {str(e)}"
