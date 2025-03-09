from nerdgraph.utils import Logger

# Create logger for the module
logger = Logger(__name__).get_logger()

def extract_cursor(response_data, domain_index=0):
    try:
        auth_domains = response_data['data']['actor']['organization']['authorizationManagement'][
            'authenticationDomains']['authenticationDomains']
        print(auth_domains)
        if auth_domains and len(auth_domains) > domain_index:
            return auth_domains[domain_index]['groups']['nextCursor']
        return None
    except (KeyError, TypeError, IndexError):
        return None


def has_next_page(response_data, domain_index=0):
    cursor = extract_cursor(response_data, domain_index)
    return cursor is not None and cursor != ""

def format_results(response_data):
    auth_domains_formatted = []

    try:
        auth_domains = response_data['data']['actor']['organization']['authorizationManagement'][
            'authenticationDomains']['authenticationDomains']

        for domain in auth_domains:
            auth_domains_formatted.append({
                'id': domain['id'],
                'name': domain['name']
            })

        return auth_domains_formatted

    except (KeyError, TypeError) as e:
        raise ValueError(f"Error extracting groups from response: {e}")
