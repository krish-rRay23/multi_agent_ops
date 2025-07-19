import click

# Task storage
tasks = []

@click.group()
def cli():
    """A simple CLI To-Do application."""
    pass

@cli.command()
@click.argument('task')
def add(task):
    """Add a new task."""
    tasks.append(task)
    click.echo(f'Task added: {task}')

@cli.command()
def list_tasks():
    """List all tasks."""
    if not tasks:
        click.echo('No tasks available.')
        return
    click.echo('Tasks:')
    for index, task in enumerate(tasks, start=1):
        click.echo(f'{index}. {task}')

@cli.command()
@click.argument('task_number', type=int)
def delete(task_number):
    """Delete a task by its number."""
    if 1 <= task_number <= len(tasks):
        removed_task = tasks.pop(task_number - 1)
        click.echo(f'Task removed: {removed_task}')
    else:
        click.echo('Error: Task number is out of range.')

if __name__ == '__main__':
    cli()