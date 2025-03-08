"""
mutation {
  authorizationManagementGrantAccess(
    grantAccessOptions: {
      groupId: "YOUR_GROUP_ID"
      accountAccessGrants: {
        accountId: YOUR_ACCOUNT_ID
        roleId: "YOUR_ROLE_ID"
      }
    }
  ) {
    roles {
      displayName
      accountId
    }
  }
}
"""