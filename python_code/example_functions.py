from .example_classes import Dog

def say_hi(name: str) -> str:
    """
    This function takes a name as input and returns a greeting.

    Args:
        name (str): The name of the person to greet.

    Returns:
        str: A greeting to the person.
    """

    return f"Hello, {name}!"

def say_bye(name: str) -> str:
    """
    This function takes a name as input and returns a farewell.

    Args:
        name (str): The name of the person to say goodbye to.

    Returns:
        str: A farewell to the person.
    """

    return f"Goodbye, {name}!"

def say_hi_and_bye(name: str) -> str:
    """
    This function takes a name as input and returns a greeting followed by a farewell.

    Args:
        name (str): The name of the person to greet and say goodbye to.

    Returns:
        str: A greeting followed by a farewell to the person.
    """

    return f"{say_hi(name)} {say_bye(name)}"

def multiple_greetings(name: str) -> list:
    """
    This function takes a name as input and returns a list of greetings.

    Args:
        name (str): The name of the person to greet.

    Returns:
        list: A list of greetings to the person.
    """
    
    return [say_hi(name), say_bye(name), say_hi_and_bye(name)]

def return_a_dog(name: str) -> Dog:
    """
    This function takes a name as input and returns a Dog object.

    Args:
        name (str): The name of the dog.

    Returns:
        Dog: A Dog object.
    """

    return Dog(name)