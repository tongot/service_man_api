from storages.backends.azure_storage import AzureStorage


class AzureMediaStorage(AzureStorage):
    # Must be replaced by your <storage_account_name>
    account_name = ''
    # Must be replaced by your <storage_account_key>
    account_key = ''
    azure_container = 'media'
    expiration_secs = None
