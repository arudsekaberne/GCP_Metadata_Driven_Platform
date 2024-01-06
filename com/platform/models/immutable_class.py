
class ImmutableMetaclass(type):
    
    """Using ImmutaleMetaclass as class metaclass makes class variable immutable"""

    def __setattr__(cls, name, value):
        raise AttributeError("Cannot create or set class attribute '{}'".format(name))
