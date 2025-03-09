from workflow import get_auth_domain_workflow
from utils.logger import Logger
from utils.nerdgraph_client import NerdGraphClient

# Create logger for the module
logger = Logger(__name__).get_logger()

if __name__ == '__main__':

    logger.info('********** Starting NerdGraph App **********.')

    client = NerdGraphClient()

    get_auth_domain_workflow(client)

    logger.info('********** Ending NerdGraph App **********.')

