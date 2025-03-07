class AuthenticationGroupsQuery:
    """Handles querying and formatting results for authentication groups with pagination support"""

    @staticmethod
    def get_query(with_cursor=False):
        """
        Returns the GraphQL query for getting authentication groups

        Parameters:
        with_cursor (bool): Whether to include cursor parameter in the query

        Returns:
        str: GraphQL query
        """
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

    @staticmethod
    def get_variables(auth_domain_ids, cursor=None):
        """
        Formats the variables for the GraphQL query

        Parameters:
        auth_domain_ids (list or str): Single ID or list of authentication domain IDs
        cursor (str, optional): Pagination cursor for fetching next page of results

        Returns:
        dict: Formatted variables for the query
        """
        # Handle case where a single string ID is passed
        if isinstance(auth_domain_ids, str):
            auth_domain_ids = [auth_domain_ids]

        variables = {
            "authDomainId": auth_domain_ids
        }

        # Add cursor if provided
        if cursor:
            variables["cursor"] = cursor

        return variables

    @staticmethod
    def extract_cursor(response_data, domain_index=0):
        """
        Extracts the next cursor from the response

        Parameters:
        response_data (dict): The JSON response from the API
        domain_index (int): Index of the domain to extract cursor from (default: 0)

        Returns:
        str or None: Next cursor or None if no more pages
        """
        try:
            auth_domains = response_data['data']['actor']['organization']['userManagement']['authenticationDomains'][
                'authenticationDomains']
            if auth_domains and len(auth_domains) > domain_index:
                return auth_domains[domain_index]['groups']['nextCursor']
            return None
        except (KeyError, TypeError, IndexError):
            return None

    @staticmethod
    def has_next_page(response_data, domain_index=0):
        """
        Checks if there are more pages available

        Parameters:
        response_data (dict): The JSON response from the API
        domain_index (int): Index of the domain to check cursor from (default: 0)

        Returns:
        bool: True if more pages exist, False otherwise
        """
        cursor = AuthenticationGroupsQuery.extract_cursor(response_data, domain_index)
        return cursor is not None and cursor != ""

    @staticmethod
    def format_results(response_data):
        """
        Extracts and formats the groups from the API response

        Parameters:
        response_data (dict): The JSON response from the API

        Returns:
        list: Formatted list of groups with their details
        """
        formatted_groups = []

        try:
            auth_domains = response_data['data']['actor']['organization']['userManagement']['authenticationDomains'][
                'authenticationDomains']

            for domain in auth_domains:
                if domain and 'groups' in domain and 'groups' in domain['groups']:
                    groups = domain['groups']['groups']
                    for group in groups:
                        formatted_groups.append({
                            'id': group['id'],
                            'name': group['displayName']
                        })

            return formatted_groups
        except (KeyError, TypeError) as e:
            raise ValueError(f"Error extracting groups from response: {e}")

    @staticmethod
    def fetch_all_groups(client, auth_domain_ids):
        """
        Fetches all groups across all pages for the given authentication domains

        Parameters:
        client: Your GraphQL client instance
        auth_domain_ids (list or str): Single ID or list of authentication domain IDs

        Returns:
        list: Complete list of groups across all pages
        """
        all_groups = []

        # Handle case where a single string ID is passed
        if isinstance(auth_domain_ids, str):
            auth_domain_ids = [auth_domain_ids]

        for domain_id in auth_domain_ids:
            cursor = None
            has_more = True

            while has_more:
                # Determine which query to use based on cursor
                query = AuthenticationGroupsQuery.get_query(with_cursor=cursor is not None)
                variables = AuthenticationGroupsQuery.get_variables([domain_id], cursor)

                # Execute query
                response = client.execute_query(query, variables)

                # Extract groups from this page
                groups = AuthenticationGroupsQuery.format_results(response)
                all_groups.extend(groups)

                # Check if there are more pages
                has_more = AuthenticationGroupsQuery.has_next_page(response)
                if has_more:
                    cursor = AuthenticationGroupsQuery.extract_cursor(response)

        return all_groups