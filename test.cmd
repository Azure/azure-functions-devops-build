call rmdir /s /q python_test_application
call func init python_test_application --worker-runtime python
call cd python_test_application
call func new --name home --template "HTTP Trigger"
call cd ..
call python -m tests.suite
call rmdir /s /q python_test_application