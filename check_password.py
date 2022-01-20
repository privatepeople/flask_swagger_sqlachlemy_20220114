from server.api.user.user import User
from server.model import Users

a=Users()
print(a.generate_password_hash('test123'))