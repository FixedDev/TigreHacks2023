class User:
	def __init__(self, user_name):
		self.hash = None
		self.name = user_name

	def set_passwd_hash(self, passwd_hash):
		self.hash = passwd_hash