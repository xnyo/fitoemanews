from typing import Type, Union, Sequence

instances = {}


def singleton(_class: Type) -> object:
    """
    Decorator che marca una classe come singleton.
    Le classi marcate come singleton possono essere utilizzate nel seguente modo:
    ```
    >>> @singleton
    >>> class Test:
    >>>     def __init__(self, value: int=None):
    >>>         self.value: int = value
    >>>
    >>>     def moltiplica(self, v: int) -> int:
    >>>         return self.value * v
    >>>
    >>> Test(10)    # crea l'oggetto singleton
    >>> Test().value
    10
    >>> Test().moltiplica(2)    # Test() è il singleton creato in precedenza
    20
    ```
    :param _class:
    :return:
    """
    def get_instance(*args, **kwargs):
        if _class not in instances:
            instances[_class] = _class(*args, **kwargs)
        return instances[_class]

    return get_instance


def destroy_all(ignore: Union[Sequence[Type], Type, None]=None):
    """
    Distrugge tutti o alcuni singleton. Usato principalmente per resettare
    l'envronment durante i test.

    :param ignore: Classe singleton o lista di classi singleton da ignorare.
                    None per eliminare tutto.
    :type:  Union[Sequence[Type], Type, None]
    :return:
    """
    if ignore is None:
        ignore = []
    elif callable(ignore):
        ignore = [ignore]

    remove = []
    for key, value in instances.items():
        if value not in ignore:
            remove.append(key)
    for i in remove:
        del instances[i]
