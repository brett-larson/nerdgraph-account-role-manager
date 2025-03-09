import os
import time
import requests
from nerdgraph.utils import Logger
from dotenv import load_dotenv
from typing import Optional, Dict, Any

# Load environment variables from .env file
load_dotenv()

# Create logger for the module
logger = Logger(__name__).get_logger()

class NerdGraphClient:
    def __init__(self):
        self.api_key = self.get_api_key()
        if not self.api_key:
            logger.warning("Missing API key")
            raise ValueError("Missing API key")
        self.headers = {
            "Content-Type": "application/json",
            "API-Key": self.api_key
        }

    @staticmethod
    def get_api_key() -> Optional[str]:
        """
        Load New Relic API key from local environment variables
        :return: API key
        """
        return os.getenv('NEW_RELIC_API_KEY')

    def execute_query(self, query: str, variables: Dict = None, max_retries: int = 3, backoff_factor: int = 2) -> Any | None:
        """Execute a single GraphQL query with retry logic"""
        payload = {
            "query": query,
            "variables": variables
        }

        for attempt in range(max_retries):
            try:
                logger.info("Sending GraphQL request.")
                response = requests.post(
                    "https://api.newrelic.com/graphql",
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
                if 'errors' in data:
                    error = data['errors'][0]
                    if error['extensions']['errorClass'] == 'TIMEOUT':
                        logger.error(f"Timeout error: {error['message']}")
                        time.sleep(backoff_factor ** attempt)
                        continue
                    else:
                        logger.error(f"GraphQL error: {error['message']}")
                        return None
                return data
            except Exception as e:
                logger.error(f"Query failed to run: {e}")
                time.sleep(backoff_factor ** attempt)
        raise Exception("Max retries exceeded for GraphQL query")