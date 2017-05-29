import hashlib
import hmac
key = "key"
msg = "The quick brown fox jumps over the lazy dog"
a = bytearray()
a.extend(map(ord, key))
b = bytearray()
b.extend(map(ord, msg))
aa = hmac.new(a, b, hashlib.md5).hexdigest()
bb = hmac.new(a, b, hashlib.sha256).hexdigest()
print(aa)
print(bb)
