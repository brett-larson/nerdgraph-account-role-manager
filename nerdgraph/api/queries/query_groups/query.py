import logging
from nerdgraph.utils import Logger
from processing import format_results, has_next_page, extract_cursor

# Create logger for the module
logger = Logger(__name__).get_logger()

def get_query(with_cursor=False):
    if with_cursor:
        return """
        query GetGroups($authDomainId: [ID!]!, $cursor: String) {
          actor {
            organization {
              userManagement {
                authenticationDomains(id: $authDomainId) {
                  authenticationDomains {
                    groups(cursor: $cursor) {
                      groups {
                        displayName
                        id
                      }
                      nextCursor
                    }
                  }
                }
              }
            }
          }
        }
        """
    else:
        return """
        query GetGroups($authDomainId: [ID!]!) {
          actor {
            organization {
              userManagement {
                authenticationDomains(id: $authDomainId) {
                  authenticationDomains {
                    groups {
                      groups {
                        displayName
                        id
                      }
                      nextCursor
                    }
                  }
                }
              }
            }
          }
        }
        """

def get_variables(auth_domain_ids, cursor=None):
    if isinstance(auth_domain_ids, str):
        auth_domain_ids = [auth_domain_ids]

    variables = {
        "authDomainId": auth_domain_ids
    }

    if cursor:
        variables["cursor"] = cursor

    return variables

def fetch_all_groups(client, auth_domain_ids):
    all_groups = []

    if isinstance(auth_domain_ids, str):
        auth_domain_ids = [auth_domain_ids]

    for domain_id in auth_domain_ids:
        cursor = None
        has_more = True

        while has_more:
            query = get_query(with_cursor=cursor is not None)
            variables = get_variables([domain_id], cursor)

            logger.info(f"Executing query with variables: {variables}")
            try:
                response = client.execute_query(query, variables)
            except Exception as e:
                logger.error(f"Error executing query: {e}")
                break

            try:
                logger.debug(f"Query response: {response}")
                groups = format_results(response)
                logger.info(f"Formatted groups: {groups}")
                all_groups.extend(groups)
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

    return all_groups
