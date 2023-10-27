from functools import wraps
import abc


def force_super_call(method):
    # If the instance is ever used in parallel code, like in multiple threads
    # or async-tasks, the flag bellow should use a contextvars.ContectVar
    # (or threading.local)
    base_method_called = False

    @wraps(method)
    def checker_wrapper(*args, **kwargs):
        nonlocal base_method_called
        try:
            result = method(*args, **kwargs)
        finally:
            base_method_called = True
        return result

    # This will be used dinamically on each method call:
    def client_decorator(leaf_method):
        @wraps(leaf_method)
        def client_wrapper(*args, **kwargs):
            nonlocal base_method_called
            base_method_called = False
            try:
                result = leaf_method(*args, **kwargs)
            finally:
                if not base_method_called:
                    raise RuntimeError(f"Overriden method '{method.__name__}' did not cause the base method to be called")

                base_method_called = False

            return result
        return client_wrapper

    # attach the client-wrapper to the decorated base method, so that the mechanism
    # in the metaclass can retrieve it:
    checker_wrapper.client_decorator = client_decorator

    # ordinary decorator return
    return checker_wrapper


def forcecall__getattribute__(self, name):
    cls = type(self)

    method = object.__getattribute__(self, name)
    registry = type(cls).forcecall_registry

    for superclass in cls.__mro__[1:]:
        if superclass in registry and name in registry[superclass]:
            # Apply the decorator with ordinary, function-call syntax:
            method = registry[superclass][name](method)
            break
    return method


class ForceBaseCallMeta(abc.ABCMeta):
    forcecall_registry = {}

    def __new__(mcls, name, bases, namespace, **kwargs):
        cls = super().__new__(mcls, name, bases, namespace, **kwargs)
        mcls.forcecall_registry[cls] = {}
        for name, method in cls.__dict__.items():
            if hasattr(method, "client_decorator"):
                mcls.forcecall_registry[cls][name] = method.client_decorator
        cls.__getattribute__ = forcecall__getattribute__
        return cls