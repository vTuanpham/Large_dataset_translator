from functools import wraps
from threading import Lock
import time
from typing import Any, Dict
from collections import deque

from fuzzywuzzy import fuzz
from pydantic import BaseModel, Field, create_model


from typing import Callable
from threading import Lock
import time
from functools import wraps

def throttle(calls_per_minute: int, verbose: bool=False) -> Callable:
    """
    Decorator that limits the number of function calls per minute.

    Args:
        calls_per_minute (int): The maximum number of function calls allowed per minute.
        verbose (bool, optional): If True, prints additional information about the throttling process. Defaults to False.

    Returns:
        Callable: The decorated function.

    Example:
        @throttle(calls_per_minute=10, verbose=True)
        def my_function():
            print("Executing my_function")

        my_function()  # Calls to my_function will be throttled to 10 calls per minute.
    """
    interval = 60.0 / calls_per_minute
    lock = Lock()
    last_call = [0.0]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                elapsed = time.time() - last_call[0]
                wait_time = interval - elapsed
                if wait_time > 0:
                    if verbose:
                        print(f"Throttling: waiting for {wait_time:.4f} seconds before calling {func.__name__}")
                    time.sleep(wait_time)
                last_call[0] = time.time()
                if verbose:
                    print(f"Calling function {func.__name__} at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_call[0]))}")
                return func(*args, **kwargs)
        return wrapper
    return decorator

def brust_throttle(calls_per_minute: int, verbose: bool=False, extra_delay: float=1.25):
    """
    Throttles function calls to a specified rate, with an optional extra delay.
    
    :param calls_per_minute: Maximum number of calls allowed per minute.
    :param verbose: If True, prints information about throttling.
    :param extra_delay: Additional delay in seconds after the 1-minute window.
    """
    last_calls = deque()

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_time = time.time()
            
            # Clean up old calls that are outside the current time window
            while last_calls and current_time - last_calls[0] > 60:
                last_calls.popleft()

            # Wait if the call limit has been reached
            if len(last_calls) >= calls_per_minute:
                wait_time = 60 - (current_time - last_calls[0]) + extra_delay
                if verbose:
                    print(f"Rate limit exceeded. Waiting for {wait_time:.2f} seconds.")
                time.sleep(wait_time)
                current_time = time.time()
                
                # Clean up old calls again after waiting
                while last_calls and current_time - last_calls[0] > 60:
                    last_calls.popleft()

            # Record the current call
            last_calls.append(current_time)
            if verbose:
                print(f"Calling function {func.__name__} at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))}")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


def create_dynamic_model(model_name: str, fields: Dict[str, Any]) -> BaseModel:
    """
    Create a dynamic Pydantic model.

    :param model_name: Name of the model.
    :param fields: Dictionary where keys are field names and values are field types.
    :return: A Pydantic BaseModel class.
    """
    return create_model(model_name, **fields)


def fuzzy_match(input_string, comparison_strings: list, threshold=80):
    """
    Check if two strings are similar based on the Levenshtein distance.

    :param input_string: The input string.
    :param comparison_string: The string to compare with.
    :param threshold: The minimum similarity ratio required to consider the strings similar.
    :return: True if the strings are similar, False otherwise.
    """
    
    for comparison_string in comparison_strings:
        if fuzz.ratio(input_string, comparison_string) >= threshold:
            return True
    return False


if __name__ == '__main__':
    fields = {
        'name': (str, Field(..., description="The name of the person")),  # Required field with description
        'age': (int, Field(None, description="The age of the person")),  # Optional field with description
        'email': (str, Field(None, description="The email address of the person"))  # Optional field with description
    }

    DynamicModel = create_dynamic_model('DynamicModel', fields)

    # Create an instance of the dynamic model
    instance = DynamicModel(name='John Doe', age=30)
    print(instance)

    print(DynamicModel.model_json_schema())