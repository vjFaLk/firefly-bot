import requests
import datetime


class Firefly(object):
    def __init__(self, hostname, auth_token):
        self.headers = {'Authorization': "Bearer " + auth_token}
        self.hostname = hostname + "/api/v1/"

    def _post(self, endpoint, payload):
        return requests.post("{}{}".format(self.hostname, endpoint), json=payload, headers=self.headers)

    def _get(self, endpoint, params=None):
        response = requests.get("{}{}".format(
            self.hostname, endpoint), params=params, headers=self.headers)
        return response.json()

    def get_budgets(self):
        return self._get("budgets")

    def get_accounts(self, account_type="asset"):
        return self._get("accounts", params={"type": account_type})

    def get_about_user(self):
        return self._get("about/user")

    def create_transaction(self, amount, description, source_account, destination_account=None, category=None, budget=None):
        now = datetime.datetime.now()
        payload = {
            "transactions": [{
                "type": "withdrawal",
                "description": description,
                "date": now.strftime("%Y-%m-%d"),
                "amount": amount,
                "budget_name": budget,
                "category_name": category,
            }]
        }
        if source_account.isnumeric():
            payload["transactions"][0]["source_id"] = source_account
        else:
            payload["transactions"][0]["source_name"] = source_account

        if destination_account:
            if destination_account.isnumeric():
                payload["transactions"][0]["destination_id"] = destination_account
            else:
                payload["transactions"][0]["destination_name"] = destination_account
        else:
            payload["transactions"][0]["destination_name"] = description

        return self._post(endpoint="transactions", payload=payload)
