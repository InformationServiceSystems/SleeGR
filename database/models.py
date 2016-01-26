import enum

class User():
    def __init__(self, user_id, email, password, first_name=None, last_name=None):
        self._user_id = user_id
        self._email = email
        self._password = password
        self._fist_name = first_name
        self._last_name = last_name


    @property
    def user_id(self):
        return self._user_id

    @property
    def email(self):
        return self._email

    @property
    def password(self):
        return self._password

    @property
    def first_name(self):
        return self._fist_name

    @property
    def last_name(self):
        return self._last_name

    def encode(self):
        return {
            "_type" : "general_user",
            "user_id" : self._user_id,
            "email" : self._email,
            "password": self._password,
            "first_name" : self._fist_name,
            "last_name" : self._last_name
        }

    @classmethod
    def decode(cls, user):
        assert user["_type"] == "general_user"
        return User(user["user_id"], user["email"], user["password"], user["first_name"], user["last_name"])

    def __str__(self):
        return '%s, %s' % (self._user_id, self._email)


