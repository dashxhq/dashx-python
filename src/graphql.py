IDENTIFY_ACCOUNT_REQUEST = '''
  mutation IdentifyAccount($input: IdentifyAccountInput!) {
    identifyAccount(input: $input) {
        id
    }
  }
'''