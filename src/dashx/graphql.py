# Mutations
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

CREATE_DELIVERY_REQUEST = '''
  mutation CreateDelivery($input: CreateDeliveryInput!) {
    createDelivery(input: $input) {
      id
    }
  }
'''

EXECUTE_FLOW_REQUEST = '''
  mutation ExecuteFlow($input: ExecuteFlowInput!) {
    executeFlow(input: $input) {
      id
    }
  }
'''

SAVE_CONTACTS_REQUEST = '''
  mutation SaveContacts($input: SaveContactsInput!) {
    saveContacts(input: $input) {
      contacts {
        id
      }
    }
  }
'''

CHECKOUT_CART_REQUEST = '''
  mutation CheckoutCart($input: CheckoutCartInput!) {
    checkoutCart(input: $input) {
      id
      status
      subtotal
      discount
      tax
      total
      gatewayMeta
      currencyCode
      orderItems {
        id
        quantity
        unitPrice
        subtotal
        discount
        tax
        total
        custom
        currencyCode
        item {
          id
          name
          identifier
          description
          createdAt
          updatedAt
          pricings {
            id
            kind
            amount
            originalAmount
            isRecurring
            recurringInterval
            recurringIntervalUnit
            appleProductIdentifier
            googleProductIdentifier
            currencyCode
            createdAt
            updatedAt
          }
        }
      }
      couponRedemptions {
        coupon {
          name
          identifier
          discountType
          discountAmount
          currencyCode
          expiresAt
        }
      }
    }
  }
'''

CAPTURE_PAYMENT_REQUEST = '''
  mutation CapturePayment($input: CapturePaymentInput!) {
    capturePayment(input: $input) {
      id
      status
      subtotal
      discount
      tax
      total
      gatewayMeta
      currencyCode
      orderItems {
        id
        quantity
        unitPrice
        subtotal
        discount
        tax
        total
        custom
        currencyCode
        item {
          id
          name
          identifier
          description
          createdAt
          updatedAt
          pricings {
            id
            kind
            amount
            originalAmount
            isRecurring
            recurringInterval
            recurringIntervalUnit
            appleProductIdentifier
            googleProductIdentifier
            currencyCode
            createdAt
            updatedAt
          }
        }
      }
      couponRedemptions {
        coupon {
          name
          identifier
          discountType
          discountAmount
          currencyCode
          expiresAt
        }
      }
    }
  }
'''

PREPARE_ASSET_REQUEST = '''
  mutation PrepareAsset($input: PrepareAssetInput!) {
    prepareAsset(input: $input) {
      id
      name
      size
      mimeType
      url
      uploadStatus
      processingStatus
      createdAt
      updatedAt
    }
  }
'''

SAVE_STORED_PREFERENCES_REQUEST = '''
  mutation SaveStoredPreferences($input: SaveStoredPreferencesInput) {
    saveStoredPreferences(input: $input) {
      success
    }
  }
'''

# Queries
SEARCH_RECORDS_REQUEST = '''
  query SearchRecords($input: SearchRecordsInput!) {
    searchRecords(input: $input)
  }
'''

FETCH_RECORD_REQUEST = '''
  query FetchRecordRequest($input: FetchRecordInput!) {
    fetchRecord(input: $input)
  }
'''

FETCH_CONTACTS_REQUEST = '''
  query FetchContacts($input: FetchContactsInput!) {
    fetchContacts(input: $input) {
      contacts {
        id
        accountId
        name
        kind
        value
        unverifiedValue
        verifiedAt
        status
        tag
        createdAt
        updatedAt
      }
    }
  }
'''

FETCH_ITEM_REQUEST = '''
  query FetchItem($input: FetchItemInput) {
    fetchItem(input: $input) {
      id
      name
      identifier
      description
      createdAt
      updatedAt
      pricings {
        id
        kind
        amount
        originalAmount
        isRecurring
        recurringInterval
        recurringIntervalUnit
        appleProductIdentifier
        googleProductIdentifier
        currencyCode
        createdAt
        updatedAt
      }
    }
  }
'''

FETCH_CART_REQUEST = '''
  query FetchCart($input: FetchCartInput!) {
    fetchCart(input: $input) {
      id
      status
      subtotal
      discount
      tax
      total
      gatewayMeta
      currencyCode
      orderItems {
        id
        quantity
        unitPrice
        subtotal
        discount
        tax
        total
        custom
        currencyCode
        item {
          id
          name
          identifier
          description
          createdAt
          updatedAt
          pricings {
            id
            kind
            amount
            originalAmount
            isRecurring
            recurringInterval
            recurringIntervalUnit
            appleProductIdentifier
            googleProductIdentifier
            currencyCode
            createdAt
            updatedAt
          }
        }
      }
      couponRedemptions {
        coupon {
          name
          identifier
          discountType
          discountAmount
          currencyCode
          expiresAt
        }
      }
    }
  }
'''

ASSET_REQUEST = '''
  query Asset($id: UUID!) {
    asset(id: $id) {
      id
      name
      size
      mimeType
      url
      uploadStatus
      processingStatus
      createdAt
      updatedAt
    }
  }
'''

ASSETS_LIST_REQUEST = '''
  query AssetsList($filter: JSON, $limit: Int, $order: JSON, $page: Int) {
    assetsList(filter: $filter, limit: $limit, order: $order, page: $page) {
      id
      name
      size
      mimeType
      url
      uploadStatus
      processingStatus
      createdAt
      updatedAt
    }
  }
'''

FETCH_STORED_PREFERENCES_REQUEST = '''
  query FetchStoredPreferences($input: FetchStoredPreferencesInput) {
    fetchStoredPreferences(input: $input) {
      preferenceData
    }
  }
'''
