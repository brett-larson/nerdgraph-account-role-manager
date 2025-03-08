def extract_cursor(response_data, domain_index=0):
    try:
        auth_domains = response_data['data']['actor']['organization']['userManagement']['authenticationDomains'][
            'authenticationDomains']
        if auth_domains and len(auth_domains) > domain_index:
            return auth_domains[domain_index]['groups']['nextCursor']
        return None
    except (KeyError, TypeError, IndexError):
        return None

def has_next_page(response_data, domain_index=0):
    cursor = extract_cursor(response_data, domain_index)
    return cursor is not None and cursor != ""

def format_results(response_data):
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