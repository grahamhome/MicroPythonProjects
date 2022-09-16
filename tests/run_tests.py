import tests.test_cases as test_cases

def run_tests():
    test_methods = reversed(list(filter(lambda funcname: funcname.startswith("test_"), dir(test_cases))))

    failures = {}

    for test in test_methods:
        test_function = getattr(test_cases, test)
        if callable(test_function):
            print(f"\nTest: {test}")
            try:
                test_function()
            except Exception as e:
                failures[test] = e

    num_failures = len(list(failures.keys()))
    if num_failures > 0:
        print(f"Failures ({num_failures}):")
        for failed_test, exception in failures.items():
            print(f"\nTest: {failed_test}")
            print(f"Exception: {exception}")
    else:
        print("All passed!")

run_tests()