from sys import getrefcount
from time import sleep

class PoolInstancer(type):
    def __new__(cls, *args):
        type_ = super(PoolInstancer, cls).__new__(cls, *args)
        setattr(type_, "__instancepool__", [])
        setattr(type_, "__inrealloc__", False)
        if args[2].get("__new__") != None:
            type_.__new__ = PoolInstancer._poolnew(type_.__new__, False)
        else:
            type_.__new__ = PoolInstancer._poolnew(type_.__new__, True)
        return type_
        
    @staticmethod
    def instancelock(func):
        def lock_func(self, *args, **kwargs):
            if getattr(self, "_is_busy", None) == None:
                raise TypeError(f"{self.__class__} doesn't support instance lock")
            else:
                if self._is_busy == False:
                    self._is_busy = True
                    func(*args, **kwargs)
                    self._is_busy = False
                else:
                    raise RuntimeError(f"Object {self.__class__}:id({id(self)}) is already used\Runtime was interrupted to avoid undefined behaviour")

    @staticmethod
    def _poolnew(func, is_implicit: bool):
        def new(cls, *args, **kwargs):
            while cls.__inrealloc__:
                sleep(0.005)
            cls.__inrealloc__ = True
            pool = cls.__instancepool__
            free_objects = [obj for obj in pool if getrefcount(obj) < 4]
            if len(free_objects) == 0:
                for _ in range(len(pool) // 2 if len(pool) != 0 else 4):
                    if is_implicit == True:
                        obj = func(cls)
                    else:
                        obj = func(cls, *args, **kwargs)
                    free_objects.append(obj)
                    pool.append(obj)
            else:
                if len(free_objects) * 2 - 2 > len(pool) and len(pool) > 4:
                    for _ in range(len(pool) // 2):
                        to_free = free_objects[0]
                        free_objects.remove(to_free)
                        pool.remove(to_free)
            obj = free_objects[-1]
            cls.__inrealloc__ = False
            return obj
        return new