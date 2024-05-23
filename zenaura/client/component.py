#!/usr/bin/env python3
import uuid
import itertools
import pickle 
from abc import abstractmethod
from collections import defaultdict
from zenaura.client.persistance import registry

_is_reuseable = defaultdict(lambda: False)
_server_persistence_cache = defaultdict(str)
_component_persistence = defaultdict(bool)

def load_server_cache():
    global _server_persistence_cache
    try:
        with open('./zenaura/server_cache.pkl', 'rb') as file:
            _server_persistence_cache = pickle.load(file)
    except FileNotFoundError:
        pass

def persist_server_cache():
    global _server_persistence_cache
    with open('./zenaura/server_cache.pkl', 'wb') as file:
        pickle.dump(_server_persistence_cache, file)

def persist_uuid(cls, reuseable=False):
    global _component_persistence
    if cls.count in _component_persistence:
        cls.id = _server_persistence_cache[cls.count]
    else:
        if reuseable:
            cls.count = next(cls._component_count)
        if cls.count in _server_persistence_cache:
            cls.id = _server_persistence_cache[cls.count]
            return
        print("cls id",_server_persistence_cache)
        id = registry.find_or_create_uuid_integer_mapping(uuid.uuid4().hex[:8], cls.count)
        _server_persistence_cache[cls.count] = id
        _component_persistence[cls.count] = True
        cls.id = id

def Reuseable(cls):
    """Decorator that rewrites the id of a class upon instantiation."""

    original_init = cls.__init__
    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        persist_uuid(cls, True)
        _is_reuseable[cls.__name__] = True
    cls.__init__ = new_init
    return cls

class Component:
    _state = defaultdict(str)  # Internal state of the component
    _component_count = itertools.count(0)
    _track_instances = defaultdict(int)

    def __init_subclass__(cls):
        """
        Initialize a new subclass of Component.

        This method generates a unique id for each subclass using uuid.

        Args:
        cls: The subclass being initialized.

        Returns:
        None
        """
        cls.count = next(cls._component_count)
        persist_uuid(cls)
        super().__init_subclass__()
        print(cls.count)
        """
        zenaura class component are limited by design 
        this checks if the user tried to reuse limited component
        it will throw an error saying user must decorate with @Reuseable
        on component child. This adher to Python zen. Client code will 
        be more implicit

        example :
        class ThisIsLimited(Component):
            pass
        c1 = ThisIsLimited() // no error
        c2 = ThisIsLimited() // throws error

        @Reuseable
        class ThisIsReuseable(Component):
            pass
        c1 = ThisIsReuseable() // no error
        c2 = ThisIsReuseable() // no error
        
        """

    
    def __init__(self):
        cls = self.__class__
        Component._track_instances[cls.__name__] += 1

        if (Component._track_instances[cls.__name__] > 1) and  not _is_reuseable[cls.__name__]:
            raise TypeError(
"""
    Zenaura class component are limted by design. \n
    Decorate component with @Reuseable to implicitly  \n
    state the component is meant to be reused:  \n
    example :  \n
        class ThisIsLimited(Component):  \n
            pass
        c1 = ThisIsLimited() // no error  \n
        c2 = ThisIsLimited() // throws error  \n

        @Reuseable  \n
        class ThisIsReuseable(Component):  \n
        c1 = ThisIsReuseable() // no error  \n
        c2 = ThisIsReuseable() // no error  \n
"""
            )
        
        
        # print(Component._track_instances[cls.__name__], cls.__name__, is_decorated_with_reuseable(cls))
       

    @property
    def state(self):
        """
        Get the state of the component.

        Returns:
        dict: The state of the component.
        """

        return self.get_state()

    @state.setter
    def state(self, value):
        """
        Set the state of the component.

        Args:
        value (dict): The new state of the component.

        Returns:
        None
        """

        self.set_state(value)

    def get_state(self):
        """
        Get the state of the component.

        Returns:
        dict: The state of the component.
        """

        return self._state

    def set_state(self, state):
        """
        Set the state of the component.

        Args:
        state (dict): The new state of the component.

        Returns:
        None
        """

        self._state = state  # Update the internal state

    @abstractmethod
    def node():
        """
        Abstract method to be implemented by subclasses.

        This method should be implemented by subclasses to define the behavior of the component.

        Returns:
        None
        """