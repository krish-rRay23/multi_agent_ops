# CLI To-Do App Project Structure

# main.py

if __name__ == '__main__':
    print('Welcome to the CLI To-Do App!')

# todo.py

todos = []

def add_todo(todo):
    todos.append(todo)

def get_todos():
    return todos

# utils.py

def print_separator():
    print("---")

# requirements.txt

# Add the required packages for the app here.