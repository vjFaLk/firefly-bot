import requests
import datetime

class Firefly(object):
    def __init__(self, hostname, auth_token):
        self.headers = {'Authorization': "Bearer " + auth_token}
        self.hostname = hostname + "/api/v1/"
    
    def _post(self, endpoint, payload):
        response = requests.post("{}{}".format(self.hostname, endpoint), json=payload, headers=self.headers)

    def _get(self, endpoint, params=None):
        response = requests.get("{}{}".format(self.hostname, endpoint), params=params, headers=self.headers)
        return response.json()

    def get_budgets(self):
        return self._get("budgets")
    
    def get_accounts(self, account_type="asset"):
        return self._get("accounts", params={"type" : account_type})

    def get_about_user(self):
        return self._get("about/user")

    def create_transaction(self, amount, description, account, category=None, budget=None):
        now = datetime.datetime.now()
        payload = {
            "transactions": [{
                "type": "withdrawal",
                "description": description,
                "date": now.strftime("%Y-%m-%d"),
                "amount": amount,
                "source_id": account,
                "budget_name": budget,
                "category_name": category,
            }]
        }
        
        return self._post(endpoint="transactions", payload=payload)