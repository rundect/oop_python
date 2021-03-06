
"""
Магические методы __setattr__, __getattribute__, __getattr__ и __delattr__
https://proproprogs.ru/python_oop/magicheskie-metody-setattr-getattribute-getattr-i-delattr

Класс можно воспринимать как некое пространство имен, в котором записаны свойства и методы
"""


class Point:
    MAX_COORD = 100
    MIN_COORD = 0

    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    """
    Метод __getattribute__ автоматически вызывается, когда идет считывание атрибута через экземпляр класса. Например, 
    при обращении к свойству MIN_COORD
    """
    def __getattribute__(self, item):
        # если идет обращение к приватному атрибуту по внешнему имени _Point__x, то генерируем исключение ValueError.
        if item == "_Point__x":
            raise ValueError("Private attribute")
        else:
            return object.__getattribute__(self, item)

    """
    После запуска видим несколько сообщений «__setattr__». Это связано с тем, что в момент создания экземпляров класса 
    в инициализаторе __init__ создавались локальные свойства __x и __y. В этот момент вызывался данный метод. Также в 
    переопределенном методе __setattr__ мы должны вызывать соответствующий метод из базового класса object, иначе, 
    локальные свойства в экземплярах создаваться не будут
    """
    def __setattr__(self, key, value):
        if key == 'z':
            raise AttributeError("недопустимое имя атрибута")
        else:
            object.__setattr__(self, key, value) # внутри метода __setattr__ нельзя менять свойства напрямую

    """
    магический метод __getattr__ автоматически вызывается, если идет обращение к несуществующему атрибуту.
    """
    def __getattr__(self, item):
        print("__getattr__: " + item)

    """
    магический метод __delattr__ вызывается в момент удаления какого-либо атрибута из экземпляра класса
    """
    def __delattr__(self, item):
        object.__delattr__(self, item)

    """
    self в set_coord – это ссылка на экземпляр класса, из которого метод вызывается, поэтому мы можем через этот параметр обращаться 
    к атрибутам класса
    """
    # def set_coord(self, x, y):
    #     if self.MIN_COORD <= x <= self.MAX_COORD:
    #         self.x = x
    #         self.y = y

    # def set_bound(self, left):
    #     self.MIN_COORD = left
    """
    Правильно объявить метод уровня класса и через него менять значения атрибутов MIN_COORD и MAX_COORD
    """
    @classmethod
    def set_bound(cls, left):
        cls.MIN_COORD = left


pt1 = Point(1, 2)
pt2 = Point(10, 20)
"""
Определение четырех атрибутов: двух свойств MAX_COORD и MIN_COORD и двух методов __init__ и set_coord. Это атрибуты 
класса и при создании экземпляров эти атрибуты остаются в пространстве имен класса, не копируются в экземпляры. Но из 
экземпляров мы можем совершенно спокойно к ним обращаться, так как пространство имен объектов содержит ссылку на 
внешнее пространство имен класса. Если какой-либо атрибут не существует в экземпляре, то поиск переходит во внешнее 
пространство, то есть, в класс и поиск продолжается там. Поэтому мы совершенно спокойно можем через экземпляр 
обратиться к свойству класса MAX_COORD
Атрибуты и методы класса – это общие данные для всех его экземпляров
"""

# print(pt1.MAX_COORD)


"""
Нужен метод, который бы изменял значение атрибута класса MIN_COORD.
Пропишем его как обычный метод: def set_bound(self, left)
Иногда ошибочно здесь рассуждают так. Мы обращаемся к атрибуту класса MIN_COORD и присваиваем ему новое значение left. 
Те из вас, кто внимательно смотрел предыдущие занятия, понимают, в чем ошибочность такого рассуждения. Да, когда мы 
через self (ссылку на объект) записываем имя атрибута и присваиваем ему какое-либо значение, то оператор присваивания 
создает этот атрибут в локальной области видимости, то есть, в самом объекте. В результате, у нас появляется новое 
локальное свойство в экземпляре класса
А в самом классе одноименный атрибут остается без изменений
"""
# pt1.set_bound(-100)
# print(pt1.__dict__)
# print(Point.__dict__)

# Четыре магических метода, которые используются при работе с атрибутами:
"""
__setattr__(self, key, value)__ – автоматически вызывается при изменении свойства key класса;
__getattribute__(self, item) – автоматически вызывается при получении свойства класса с именем item;
__getattr__(self, item) – автоматически вызывается при получении несуществующего свойства item класса;
__delattr__(self, item) – автоматически вызывается при удалении свойства item (не важно: существует оно или нет)
"""

print(pt1.MIN_COORD)
# print(pt1._Point__x)
print(pt1.a)

pt1.a = 10
del pt1.a
print(pt1.__dict__)


