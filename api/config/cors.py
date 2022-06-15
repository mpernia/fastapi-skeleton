# A list of origins that should be permitted to make cross-origin requests.
# E.g. ['https://example.org', 'https://www.example.org'].
# You can use ['*'] to allow any origin.
origins = ["*"]

# A list of HTTP methods that should be allowed for cross-origin requests.
# Defaults to ['GET'].
# You can use ['*'] to allow all standard methods.
methods = ["*"]

# A list of HTTP request headers that should be supported for cross-origin requests. Defaults to [].
# You can use ['*'] to allow all headers.
# The Accept, Accept-Language, Content-Language and Content-Type headers are always allowed for CORS requests.
headers = ["*"]

# Indicate that cookies should be supported for cross-origin requests.
# Defaults to False
# Also, allow_origins cannot be set to ['*'] for credentials to be allowed, origins must be specified.
credentials = False
