__author__ = 'andrey'


class UserType:
    FREE = "FREE"
    UNLIMITED = "UNLIMITED"


class User:
    def __init__(self, json_representation):
        self.user_type = json_representation["userType"]
        self.login = json_representation["userLogin"]
        self.name = json_representation["userName"]
        self.password = json_representation["userPassword"]

    def get_name(self):
        return self.name

    def get_login(self):
        return self.login

    def get_password(self):
        return self.password

    def get_type(self):
        return self.user_type

    def __str__(self):
        return "type: " + self.user_type + "\nlogin: " + self.login


class Users:
    def __init__(self):
        self.users = []

    def add_user(self, user):
        self.users.append(user)

    def get_by_login(self, login):
        """:rtype : User"""
        for user in self.users:
            if user.get_login() == login:
                return user
        return None

    def get_by_type(self, user_type=UserType.UNLIMITED):
        """:rtype : User"""
        for user in self.users:
            if user.get_type() == user_type:
                return user
        return None

    def get_free(self):
        """:rtype : User"""
        return self.get_by_type(UserType.FREE)

    def get_unlimited(self):
        """:rtype : User"""
        return self.get_by_type(UserType.UNLIMITED)

    def __str__(self):
        result = ""
        for user in self.users:
            result += "--USER--\n" + user.__str__() + "\n"
        return result