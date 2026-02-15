import os
import uuid

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

from .graphql import (
    ASSET_REQUEST,
    ASSETS_LIST_REQUEST,
    CAPTURE_PAYMENT_REQUEST,
    CHECKOUT_CART_REQUEST,
    CREATE_DELIVERY_REQUEST,
    FETCH_CART_REQUEST,
    FETCH_CONTACTS_REQUEST,
    FETCH_ITEM_REQUEST,
    FETCH_RECORD_REQUEST,
    FETCH_STORED_PREFERENCES_REQUEST,
    IDENTIFY_ACCOUNT_REQUEST,
    PREPARE_ASSET_REQUEST,
    SAVE_CONTACTS_REQUEST,
    SAVE_STORED_PREFERENCES_REQUEST,
    SEARCH_RECORDS_REQUEST,
    TRACK_EVENT_REQUEST,
)
from .search_records import SearchRecordsInputBuilder
from .utils import parse_filter_object

VERSION = 'v1'


class DashX:
    def __init__(self, base_uri=None, public_key=None, private_key=None, target_environment=None):
        self.base_uri = base_uri or os.environ.get('DASHX_BASE_URI', 'https://api.dashx.com/graphql')
        self.public_key = public_key or os.environ.get('DASHX_PUBLIC_KEY')
        self.private_key = private_key or os.environ.get('DASHX_PRIVATE_KEY')
        self.target_environment = target_environment or os.environ.get('DASHX_TARGET_ENVIRONMENT')

        if not self.public_key:
            raise ValueError(
                "Public key is required. Set 'DASHX_PUBLIC_KEY' environment variable or pass public_key."
            )
        if not self.private_key:
            raise ValueError(
                "Private key is required. Set 'DASHX_PRIVATE_KEY' environment variable or pass private_key."
            )
        if not self.target_environment:
            raise ValueError(
                "Target environment is required. Set 'DASHX_TARGET_ENVIRONMENT' environment variable or pass target_environment."
            )

    def identify(self, uid=None, **params):
        q_params = dict()
        if uid is None:
            q_params['anonymousUid'] = str(uuid.uuid4())
        else:
            q_params['uid'] = str(uid)
        q_params.update(params)
        return self._execute(IDENTIFY_ACCOUNT_REQUEST, {'input': q_params})

    def track(self, event, uid=None, data=None):
        if uid is None:
            return self._execute(
                TRACK_EVENT_REQUEST,
                {
                    'input': {
                        'event': event,
                        'accountAnonymousUid': str(uuid.uuid4()),
                        'data': data,
                    }
                },
            )
        return self._execute(
            TRACK_EVENT_REQUEST,
            {'input': {'event': event, 'accountUid': str(uid), 'data': data}},
        )

    def deliver(self, urn, options=None):
        """Create a delivery (e.g. send email). URN format: templateSubkind/templateIdentifier."""
        options = dict(options or {})
        content = dict(options.pop('content', {}))
        template_subkind, template_identifier = urn.split('/', 1)
        params = {
            'templateSubkind': template_subkind.upper(),
            'templateIdentifier': template_identifier,
            'content': content,
            **options,
        }
        for key in ('to', 'cc', 'bcc'):
            val = content.get(key) or options.get(key)
            if val is not None:
                params['content'][key] = val if isinstance(val, list) else [val]
        result = self._execute(CREATE_DELIVERY_REQUEST, {'input': params})
        return result.get('createDelivery') if result else None

    def search_records(self, resource, options=None):
        """
        Search records. If options is None, returns a SearchRecordsInputBuilder for fluent chaining.
        Otherwise runs the search with the given options and returns the result.
        """
        if options is None:
            return SearchRecordsInputBuilder(
                resource,
                lambda opts: self._execute(SEARCH_RECORDS_REQUEST, {'input': opts}).get('searchRecords'),
            )
        filter_val = parse_filter_object(options.get('filter')) if options.get('filter') else None
        input_opts = dict(options)
        if filter_val is not None:
            input_opts['filter'] = filter_val
        input_opts['resource'] = resource
        result = self._execute(SEARCH_RECORDS_REQUEST, {'input': input_opts})
        return result.get('searchRecords') if result else None

    def fetch_record(self, urn, **options):
        """Fetch a single record by URN. URN format: resource/record_id."""
        if '/' not in urn:
            raise ValueError("URN must be of form: resource/record_id")
        resource, record_id = urn.split('/', 1)
        params = {'resource': resource, 'recordId': record_id, **options}
        result = self._execute(FETCH_RECORD_REQUEST, {'input': params})
        return result.get('fetchRecord') if result else None

    def fetch_item(self, identifier):
        """Fetch an item by identifier."""
        result = self._execute(FETCH_ITEM_REQUEST, {'input': {'identifier': identifier}})
        return result.get('fetchItem') if result else None

    def fetch_cart(self, uid=None, anonymous_uid=None, order_id=None):
        """Fetch cart for account (uid) or anonymous (anonymous_uid), optionally by order_id."""
        params = {}
        if uid is not None:
            params['accountUid'] = str(uid)
        if anonymous_uid is not None:
            params['accountAnonymousUid'] = anonymous_uid
        if order_id is not None:
            params['orderId'] = order_id
        result = self._execute(FETCH_CART_REQUEST, {'input': params})
        return result.get('fetchCart') if result else None

    def fetch_contacts(self, uid):
        """Fetch contacts for account uid."""
        result = self._execute(FETCH_CONTACTS_REQUEST, {'input': {'uid': str(uid)}})
        if result and result.get('fetchContacts'):
            return result['fetchContacts'].get('contacts')
        return None

    def save_contacts(self, uid, contacts):
        """Save contacts for account uid. contacts is a list of contact dicts."""
        result = self._execute(SAVE_CONTACTS_REQUEST, {'input': {'uid': str(uid), 'contacts': contacts}})
        return result.get('saveContacts') if result else None

    def checkout_cart(
        self,
        uid,
        anonymous_uid=None,
        gateway=None,
        gateway_options=None,
        order_id=None,
    ):
        """Checkout cart for account uid (or anonymous_uid)."""
        params = {
            'accountUid': str(uid),
            'accountAnonymousUid': anonymous_uid,
            'gatewayIdentifier': gateway,
            'gatewayOptions': gateway_options,
            'orderId': order_id,
        }
        result = self._execute(CHECKOUT_CART_REQUEST, {'input': params})
        return result.get('checkoutCart') if result else None

    def capture_payment(self, uid=None, anonymous_uid=None, gateway_response=None, order_id=None):
        """Capture payment for a checkout."""
        params = {
            'accountUid': str(uid) if uid is not None else None,
            'accountAnonymousUid': anonymous_uid,
            'gatewayResponse': gateway_response,
            'orderId': order_id,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result = self._execute(CAPTURE_PAYMENT_REQUEST, {'input': params})
        return result.get('capturePayment') if result else None

    def get_asset(self, id):
        """Fetch a single asset by id (UUID)."""
        result = self._execute(ASSET_REQUEST, {'id': id})
        return result.get('asset') if result else None

    def prepare_asset(self, resource, attribute, name, size, mime_type):
        """Prepare an asset for upload."""
        params = {
            'resource': resource,
            'attribute': attribute,
            'name': name,
            'size': size,
            'mimeType': mime_type,
        }
        if self.target_environment:
            params['targetEnvironment'] = self.target_environment
        result = self._execute(PREPARE_ASSET_REQUEST, {'input': params})
        return result.get('prepareAsset') if result else None

    def list_assets(self, filter=None, limit=None, order=None, page=None):
        """List assets with optional filter, limit, order, page."""
        variables = {}
        if filter is not None:
            variables['filter'] = filter
        if limit is not None:
            variables['limit'] = limit
        if order is not None:
            variables['order'] = order
        if page is not None:
            variables['page'] = page
        result = self._execute(ASSETS_LIST_REQUEST, variables)
        return result.get('assetsList') if result else None

    def fetch_stored_preferences(self, uid):
        """Fetch stored preferences for account uid."""
        result = self._execute(
            FETCH_STORED_PREFERENCES_REQUEST,
            {'input': {'accountUid': str(uid)}},
        )
        if result and result.get('fetchStoredPreferences'):
            return result['fetchStoredPreferences'].get('preferenceData')
        return None

    def save_stored_preferences(self, uid, preference_data):
        """Save stored preferences for account uid."""
        result = self._execute(
            SAVE_STORED_PREFERENCES_REQUEST,
            {'input': {'accountUid': str(uid), 'preferenceData': preference_data}},
        )
        return result.get('saveStoredPreferences') if result else None

    def _execute(self, query_string, variable_values):
        """Execute a GraphQL query or mutation with the given variable_values."""
        query = gql(query_string)
        transport = AIOHTTPTransport(url=self.base_uri, headers=self._headers())
        client = Client(transport=transport, fetch_schema_from_transport=False)
        return client.execute(query, variable_values=variable_values)

    def _headers(self):
        return {
            'User-Agent': 'dashx-python',
            'X-Public-Key': self.public_key,
            'X-Private-Key': self.private_key,
            'X-Target-Environment': self.target_environment,
            'Content-Type': 'application/json',
        }

    def generate_header(self):
        """Return headers used for API requests (backward compatible)."""
        return self._headers()
