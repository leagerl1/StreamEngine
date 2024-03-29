from __future__ import unicode_literals

import time, random, hmac, hashlib, binascii

try:
    from urllib.parse import urlparse, parse_qsl, quote
except ImportError:
    from urlparse import urlparse, parse_qsl
    from urllib import quote

import sys

PY3 = (sys.version_info >= (3, 0, 0))


def om(consumer, url, post_params, token=None, method='POST', realm=None, timestamp=None, nonce=None):
  """A one-shot simple OAuth signature generator"""

  # the method must be upper-case
  method = method.upper()

  # turn the POST params into a list of tuples if it's not already
  if isinstance(post_params, list):
    params = list(post_params) # copy the params list since we'll be messing with it
  else:
    params = list(post_params.items())

  # normalize the URL
  parts = urlparse(url)
  scheme, netloc, path, _, query = parts[:5]
  # Exclude default port numbers.
  if scheme == 'http' and netloc[-3:] == ':80':
      netloc = netloc[:-3]
  elif scheme == 'https' and netloc[-4:] == ':443':
      netloc = netloc[:-4]
  netloc = netloc.lower()
  normalized_url = '%s://%s%s' % (scheme, netloc, path)

  # add query-string params (if any) to the params list
  params.extend(parse_qsl(query))

  # add OAuth params
  params.extend([
    ('oauth_version', '1.0'),
    ('oauth_timestamp', timestamp if timestamp is not None else str(int(time.time()))),
    ('oauth_nonce', nonce if nonce is not None else str(random.randint(0, 1000000))),
    ('oauth_signature_method', 'HMAC-SHA1'),
    ('oauth_consumer_key', consumer[0]),
  ])

  # the consumer secret is the first half of the HMAC-SHA1 key
  hmac_key = consumer[1] + '&'

  if token is not None:
    # include a token in params
    params.append(('oauth_token', token[0]))
    # and the token secret in the HMAC-SHA1 key
    hmac_key += token[1]

  # Sort lexicographically, first after key, then after value.
  params.sort()
  # UTF-8 and escape the key/value pairs
  def escape(s):
    s_encoded = s.encode('utf-8')
    safe_chars_encoded = u'~'.encode('utf-8')
    return quote(s_encoded, safe=safe_chars_encoded)
  params = [(escape(k), escape(v)) for k,v in params]
  # Combine key value pairs into a string.
  normalized_params = '&'.join(['%s=%s' % (k, v) for k, v in params])

  # build the signature base string
  signature_base_string = (escape(method) +
                           '&' + escape(normalized_url) +
                           '&' + escape(normalized_params))

  # HMAC-SHA1
  hashed = hmac.new(hmac_key.encode('utf-8'),
                    signature_base_string.encode('utf-8'),
                    hashlib.sha1)

  # Calculate the digest base 64.
  oauth_signature = binascii.b2a_base64(hashed.digest())[:-1]
  if PY3:
      # binascii.b2a_base64 will return bytes in Python3
      # convert it to unicode here.
      oauth_signature = oauth_signature.decode('utf-8')

  # Build the Authorization header
  authorization_params = [('oauth_signature', oauth_signature)]
  if realm is not None:
    authorization_params.insert(0, ('realm', escape(realm)))
  oauth_params = frozenset(('oauth_version', 'oauth_timestamp', 'oauth_nonce',
                            'oauth_signature_method', 'oauth_signature',
                            'oauth_consumer_key', 'oauth_token'))
  authorization_params.extend([p for p in params if p[0] in oauth_params])

  return 'OAuth ' + (', '.join(['%s="%s"'%p for p in authorization_params]))
