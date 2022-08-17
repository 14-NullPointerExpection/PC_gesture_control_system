def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton

@Singleton
class T:
    t = 0
    x = 1

    def __init__(self):
        self.x += 1

    @classmethod
    def getT(cls):
        if (cls.t == 0):
            cls.t = T()
            return cls.t
        else:
            return cls.t


if __name__ == "__main__":
    k = T()
    l = T()
    print(k.x)
    print(l.x)
