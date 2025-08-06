import os

# KIS Authentication and Account Configuration
AUTH_CONFIG = {
    "APP_KEY": os.getenv("KIS_APP_KEY", "YOUR_KIS_APP_KEY"),
    "APP_SECRET": os.getenv("KIS_APP_SECRET", "YOUR_KIS_APP_SECRET"),
    "ACCOUNT_NO": os.getenv("KIS_ACCOUNT_NO", "YOUR_ACCOUNT_NO"),
    "PROD_DIGIT": "01", # Account product digit (e.g., '01' for stock account)
    "KIS_AGENT": "Mozilla/5.0", # User-Agent for API requests
}

# API Endpoint and Model Configuration
API_CONFIG = {
    "BASE_URL": "https://openapi.koreainvestment.com:9443",
    "DEV": {
        "BASE_URL": "https://openapivts.koreainvestment.com:29443"
    },
    "OPENAI": {
        "ACCESS_KEY": os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY"),
        "MODEL_NAME": "gpt-4o",
        "TEMPERATURE": 0
    },
}
