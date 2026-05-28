""" Enums module """
from enum import Enum



class  Language(Enum):
    """ Language enum """
    """ 
        Мова (Говірка / Наріччя).
        Визначає, якою мовою Писар надсилатиме сувої (повідомлення).
    """
    RU = "ru"
    EN = "en"
    UK = "uk"

    @classmethod
    def choices(cls):
        """ Return choices """

        title = {
            cls.UK: "Козацька говірка (UA)",
            cls.EN: "Заморська мова (EN)",
            cls.RU: "Північне наріччя (RU)"
        }
        return [(gender.value, gender.name) for gender in cls]


class Gender (Enum):
    """ Gender enum """
    """ 
        Рід (Стать).
        Визначає звертання до воїна в інтерфейсі.
    """
    M = "male"
    F = "female"
    @classmethod
    def choices(cls):
        """ Return choices """

        title= {
            cls.M: "Козак",
            cls.F: "Дівчина"
        }
        return [(gender.value, gender.name) for gender in cls]

class Role (Enum):
    """ Role enum """
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"

    @classmethod
    def choices(cls):
        """ Return choices for Role enum """
        titles = {

            cls.ADMIN: "Кошовий",
            cls.MODERATOR: "Курінний Писар",
            cls.USER: "Вільний козак"
        }


        return [(role.value, role.name) for role in cls]
