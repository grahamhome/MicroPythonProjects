def graceful_exit(function):
    """
    Ensure that all hardware class instances shut down gracefully when a function terminates due to an exception.
    """

    def wrap(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            print(e)
            quit()

    return wrap
