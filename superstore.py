from requests import post, get
import hashlib
import uuid

seed = '34b31789102a4f6d16cb7b7ee1558de7'

m = hashlib.md5()
m.update(seed.encode('utf-8'))
u = uuid.UUID(m.hexdigest())

cart_data = get(f"https://api.pcexpress.ca/v1/carts/34b31789-102a-4f6d-16cb-7b7ee1558de7/heartbeat").content

print(u)
print(cart_data)
