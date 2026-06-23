import sentry_sdk
from dotenv import load_dotenv 
import os 
load_dotenv()

sentry_sdk.init(
    dsn=os.getenv("DSN"),
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)