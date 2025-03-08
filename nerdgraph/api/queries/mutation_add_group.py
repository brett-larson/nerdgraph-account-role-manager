"""
mutation {
  userManagementCreateGroup(
    createGroupOptions: {
      authenticationDomainId: "YOUR_AUTH_DOMAIN_ID"
      displayName: "GROUP_DISPLAY_NAME"
    }
  ) {
    group {
      displayName
      id
    }
  }
}
"""