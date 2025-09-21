def hello_function():
    """A simple hello function."""
    print("Hello, world!")
    return "hello"

class HelloClass:
    def __init__(self):
        self.greeting = "hello"
    
    def say_hello(self):
        return f"{self.greeting} from class"

# Test comment with hello
hello_var = "hello world"
another_hello = hello_function()
