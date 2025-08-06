import os

API_CONFIG = {
    "OPENAI" : {
        "ACCESS_KEY" : os.getenv("ACCESS_KEY","YOUR_OPENAI_API_KEY"),
        "MODEL_NAME" : "gpt-4o",
        "TEMPERATURE" : 0
    },
}
