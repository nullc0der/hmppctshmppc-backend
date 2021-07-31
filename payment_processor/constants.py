SUPPORTED_CURRENCY = (
    ('bitcoin', 'bitcoin'),
    ('cardano', 'cardano'),
    ('dogecoin', 'dogecoin'),
    ('ethereum', 'ethereum'),
    ('monero', 'monero'),
    ('polkadot', 'polkadot')
)

TX_FIELDS_TO_CHECK = {
    'bitcoin': ['amount', 'txids', 'confirmations'],
    'dogecoin': ['amount', 'txid', 'confirmations'],
    'monero': ['amount', 'txid', 'confirmations'],
    'ethereum': ['value', 'hash']
}

TX_FIELDS_TO_SAVE = {
    'bitcoin': ['amount', 'txids'],
    'dogecoin': ['amount', 'txid'],
    'monero': ['amount', 'txid'],
    'ethereum': ['value', 'hash']
}
