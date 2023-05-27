from enum import Enum


class LoginController:
	def __init__(self, db_access_object, password_hash_algor):
		self.db_access_object = db_access_object
		self.password_hash_algor = password_hash_algor

	def user_exists(self, user_name):

	##	self.db_access_object.search({name: user_name}) busqueda
	## return si existe o no

	def login(self, user_name, password):

	## db_access_object.search({name: user_name}).then(__check_if_valid)
	## si es valido, devolver un SUCCESS, si el usuario no se encuentra, INVALID_USER
	## si la contraseña no coincide devolver WRONG_PASSWD
	## cualquier otro caso devolver ERROR
	def __checkIfValid(self, hashed, user):

	## user.password_hash == hashed
	## devolver si concuerda o no

	def __hash_password(self, password):
## hashed= self.password_hash_algor.hash(password)


class LoginResult(Enum):
	SUCCESS = 1,
	WRONG_PASSWORD = 2,
	INVALID_USER = 3,
	ERROR = 4
