from sys import print_exception, exit


def graceful_exit(function):
    """
    Ensure that all hardware class instances shut down gracefully when a function terminates due to an exception.
    """

    def handle_it(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            print_exception(e)
            exit(1)

    return handle_it
