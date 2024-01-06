
class ImmutableMetaModel(type):
    
    """Using ImmutaleMetaclass as class metaclass makes class variable immutable"""

    def __setattr__(cls, name, value):
        raise AttributeError(f"Cannot create or set class attribute '{name}'")
