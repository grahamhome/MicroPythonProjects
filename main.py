import tests.modules.test_led as test_led

tests = list(filter(lambda funcname: funcname.startswith("test_"), dir(test_led)))

failures = {}

for test in tests:
    test_function = getattr(test_led, test)
    try:
        test_function()
    except Exception as e:
        failures[test] = e

print(f"Failures ({len(list(failures.keys()))}):")
for failed_test, exception in failures.items():
    print(f"Test: {failed_test}")
    print(f"Exception: {exception}")