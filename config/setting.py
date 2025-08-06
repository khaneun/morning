import os

API_CONFIG = {
    "OPENAI": {
        "MODEL_NAME": os.environ.get("OPENAI_MODEL_NAME", "gpt-4"),
        "TEMPERATURE": float(os.environ.get("OPENAI_TEMPERATURE", 0.7)),
        "ACCESS_KEY": os.environ.get("OPENAI_API_KEY", "YOUR_API_KEY_HERE"),
    }
}
