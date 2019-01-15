:: Create and enter the env
call py -3.6 -m venv .env_python_test_application
call .env_python_test_application\scripts\activate
:: Create the functionapp and add a simple home http function
call func init python_test_application --worker-runtime python
call cd python_test_application
call func new --name home --template "HTTP Trigger"
:: Reactivate the env for the manager and run the tests
call cd ..
call .env\scripts\activate
call python -m tests.suite
:: Clean up
call rmdir /s /q python_test_application
call rmdir /s /q .env_python_test_application
