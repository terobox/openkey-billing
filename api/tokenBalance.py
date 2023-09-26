import requests
from datetime import datetime, timedelta
import json

def check_billing(api_key):
    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json"
    }

    api_url = "https://openkey.cloud"
    now = datetime.now()
    start_date = now - timedelta(days=90)
    end_date = now + timedelta(days=1)
    url_subscription = f"{api_url}/v1/dashboard/billing/subscription"
    url_usage = f"{api_url}/v1/dashboard/billing/usage?start_date={format_date(start_date)}&end_date={format_date(end_date)}"

    try:
        response = requests.get(url_subscription, headers=headers)
        response.raise_for_status()
        subscription_data = response.json()
        total_amount = subscription_data.get("system_hard_limit_usd")

        if total_amount is None:
            raise ValueError("Invalid response format for subscription data.")

        response = requests.get(url_usage, headers=headers)
        response.raise_for_status()
        usage_data = response.json()
        total_usage = usage_data.get("total_usage") / 100
        
        if total_usage is None:
            raise ValueError("Invalid response format for usage data.")

        remaining = round(total_amount - total_usage, 3)
        return {
            "Status": 1,
            "Total": total_amount,
            "Used": total_usage,
            "Remaining": remaining
        }

    except (requests.RequestException, ValueError) as e:
        return {
            "Status": 0,
            "Error": "查询失败，API Key已失效或不存在"
        }

def format_date(date):
    return date.strftime("%Y-%m-%d")
