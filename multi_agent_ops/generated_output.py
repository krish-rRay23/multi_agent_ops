# main.py
import click
from task_manager import TaskManager

task_manager = TaskManager()

@click.group()
def cli():
    """A simple command-line To-Do application."""
    pass

@cli.command()
@click.option('--title', prompt='Task title', help='Title of the task to add.')
def add(title):
    """Add a new task."""
    task_manager.add_task(title)
    click.echo(f'Task "{title}" added.')

@cli.command()
def view():
    """View all tasks."""
    tasks = task_manager.get_tasks()
    if not tasks:
        click.echo("No tasks available.")
        return
    for idx, task in enumerate(tasks, start=1):
        status = "✔" if task['completed'] else "✖"
        click.echo(f"{idx}. [{status}] {task['title']}")

@cli.command()
@click.option('--id', type=int, prompt='Task ID', help='ID of the task to mark as completed.')
def complete(id):
    """Mark a task as completed."""
    if task_manager.complete_task(id):
        click.echo(f"Task ID {id} marked as completed.")
    else:
        click.echo("Task not found.")

@cli.command()
@click.option('--id', type=int, prompt='Task ID', help='ID of the task to delete.')
def delete(id):
    """Delete a task."""
    if task_manager.delete_task(id):
        click.echo(f"Task ID {id} deleted.")
    else:
        click.echo("Task not found.")

if __name__ == '__main__':
    cli()

# task_manager.py
import pickle
import os

class TaskManager:
    def __init__(self, filename='tasks.pkl'):
        self.filename = filename
        self.tasks = self.load_tasks()

    def add_task(self, title):
        new_task = {'title': title, 'completed': False}
        self.tasks.append(new_task)
        self.save_tasks()

    def get_tasks(self):
        return self.tasks

    def complete_task(self, id):
        if 0 < id <= len(self.tasks):
            self.tasks[id - 1]['completed'] = True
            self.save_tasks()
            return True
        return False

    def delete_task(self, id):
        if 0 < id <= len(self.tasks):
            del self.tasks[id - 1]
            self.save_tasks()
            return True
        return False

    def save_tasks(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self.tasks, f)

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as f:
                return pickle.load(f)
        return []

# requirements.txt
click