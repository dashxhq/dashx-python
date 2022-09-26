IDENTIFY_ACCOUNT_REQUEST = '''
  mutation IdentifyAccount($input: IdentifyAccountInput!) {
    identifyAccount(input: $input) {
        id
    }
  }
'''

TRACK_EVENT_REQUEST = '''
  mutation TrackEvent($input: TrackEventInput!) {
    trackEvent(input: $input) {
        success
    }
  }
'''
