document.addEventListener('DOMContentLoaded', () => {
    const newTaskButton = document.getElementById('newTaskButton');
    const taskList = document.getElementById('task-list');

    // Fetch tasks from the API
    fetch('/tasks')
        .then(response => response.json())
        .then(tasks => {
            taskList.innerHTML = ''; // Clear existing tasks
            tasks.forEach(task => {
                const taskElement = document.createElement('div');
                taskElement.textContent = `${task.title} - ${task.description} (Created: ${task.created_at.toLocaleString()})`;
                taskList.appendChild(taskElement);
            });
        })
        .catch(error => console.error('Error fetching tasks:', error));

    // Add new task
    newTaskButton.addEventListener('click', () => {
        // Implement adding new task functionality here
        const title = prompt("Enter task title:");
        const description = prompt("Enter task description:");
        if (title && description) {
            const newTask = { title: title, description: description };
            fetch('/tasks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(newTask)
            })
            .then(response => response.json())
            .then(task => {
                taskList.innerHTML = '';
                fetch('/tasks')
                    .then(response => response.json())
                    .then(tasks => {
                        tasks.forEach(t => {
                            const taskElement = document.createElement('div');
                            taskElement.textContent = `${t.title} - ${t.description} (Created: ${t.created_at.toLocaleString()})`;
                            taskList.appendChild(taskElement);
                        });
                    });
            });
        }
    });
});