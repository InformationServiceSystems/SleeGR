import enum

class User:
    def __init__(self, user_id, email, password, first_name=None, last_name=None):
        self.__user_id = user_id
        self.__email = email
        self.__password = password
        self.__fist_name = first_name
        self.__last_name = last_name

    @property
    def user_id(self):
        return self.__user_id

    @property
    def email(self):
        return self.__email

    @property
    def password(self):
        return self.__password

    @property
    def first_name(self):
        return self.__fist_name

    @property
    def last_name(self):
        return self.__last_name

    def encode(self):
        return {
            "_type" : "general_user",
            "user_id" : self.__user_id,
            "email" : self.__email,
            "password": self.__password,
            "first_name" : self.__fist_name,
            "last_name" : self.__last_name
        }

    @classmethod
    def decode(cls, user):
        assert user["_type"] == "general_user"
        return User(user["user_id"], user["email"], user["password"], user["first_name"], user["last_name"])

    def __str__(self):
        return  '%s, %s' % (self.__user_id, self.__email)


