from nerdgraph.utils import Logger
from .data_processor import format_results, has_next_page, extract_cursor

# Create logger for the module
logger = Logger(__name__).get_logger()

def get_query(with_cursor=False):
    if with_cursor:
        return """
        query GetAuthenticationDomains($cursor: String) {
          actor {
            organization {
              authorizationManagement {
                authenticationDomains(cursor: $cursor) {
                  authenticationDomains {
                    id
                    name
                  }
                  nextCursor
                }
              }
            }
          }
        }
        """
    else:
        return """
        query GetAuthenticationDomains {
          actor {
            organization {
              authorizationManagement {
                authenticationDomains {
                  authenticationDomains {
                    id
                    name
                  }
                  nextCursor
                }
              }
            }
          }
        }
        """

def get_variables(cursor=None):
    """
    Get the variables for the query.
    :param cursor:
    :return:
    """
    variables = {}
    if cursor:
        variables["cursor"] = cursor
    return variables

def fetch_auth_domains(client):
    """
    Fetch all authentication domains.
    :param client: The NerdGraph client to use for the query
    :return: A list of authentication domains.
    """

    all_auth_domains = []  # Empty list to store auth domains.

    cursor = None # Start with no cursor.
    has_more = True # Assume there are more pages to fetch.

    while has_more:
        query = get_query(with_cursor=cursor is not None)
        variables = get_variables(cursor)

        logger.info(f"Executing query with variables: {variables}")

        try:
            response = client.execute_query(query, variables)
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            break

        try:
            logger.debug(f"Query response: {response}")
            groups = format_results(response)
            logger.info(f"Formatted Auth Domains: {groups}")
            all_auth_domains.extend(groups)
        except Exception as e:
            logger.error(f"Error processing query response: {e}")
            break

        try:
            has_more = has_next_page(response)
            logger.info(f"Has next page: {has_more}")
            if has_more:
                cursor = extract_cursor(response)
                logger.info(f"Next cursor: {cursor}")
        except Exception as e:
            logger.error(f"Error handling pagination: {e}")
            break

    return all_auth_domains
