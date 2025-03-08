import os
import requests
from nerdgraph.utils import Logger
from dotenv import load_dotenv
from typing import Optional, Dict

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

    def execute_query(self, query: str, variables: Dict = None) -> Dict:
        """Execute a single GraphQL query"""
        try:
            logger.info("Sending GraphQL request.")
            response = requests.post(
                "https://api.newrelic.com/graphql",
                headers=self.headers,
                json={"query": query, "variables": variables}
            )
            response.raise_for_status()
        except Exception as e:
            logger.error(f"Query failed to run: {e}")
            raise Exception(f"Query failed to run: {e}")

        return response.json()