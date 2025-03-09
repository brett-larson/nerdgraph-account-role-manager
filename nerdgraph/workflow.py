from nerdgraph.utils import Logger
from queries.get_auth_domains.query import fetch_auth_domains

# Create logger for the module
logger = Logger(__name__).get_logger()

def get_auth_domain_workflow(nerdgraph_client):

    auth_domains = fetch_auth_domains(nerdgraph_client)
    print(auth_domains)


