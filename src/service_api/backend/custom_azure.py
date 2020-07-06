from storages.backends.azure_storage import AzureStorage


class AzureMediaStorage(AzureStorage):
    # Must be replaced by your <storage_account_name>
    account_name = 'tshwaraganopicstorage'
    # Must be replaced by your <storage_account_key>
    account_key = 'uG5ms2hmfxMaRNtnxdmWHMzD8lw296+8+mUUGw+gqe16ZZmF7253VvxONu9+4nKvT3Owqur7RsJvjqskT67vEQ=='
    azure_container = 'media'
    expiration_secs = None
