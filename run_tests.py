import tests as test_modules

test_methods = list(filter(lambda funcname: funcname.startswith("test_"), dir(test_modules)))

failures = {}

for test in test_methods:
    test_function = getattr(test_modules, test)
    try:
        test_function()
    except Exception as e:
        failures[test] = e

num_failures = len(list(failures.keys()))
if num_failures > 0:
    print(f"Failures ({num_failures}):")
    for failed_test, exception in failures.items():
        print(f"Test: {failed_test}")
        print(f"Exception: {exception}")
else:
    print("All passed!")