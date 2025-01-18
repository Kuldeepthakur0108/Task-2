<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Task Management</title>
    <style>
        /* General Body Styling */
        body {
            font-family: 'Arial', sans-serif;
            background-color: #1e1e2f;
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            color: #f5f5f5;
        }

        /* Container for the page */
        .container {
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            background-color: #2b2b3c;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }

        /* Header Styling */
        h1 {
            text-align: center;
            color: #f1c40f;
            font-size: 2.5em;
            margin-bottom: 20px;
        }

        /* Task creation form */
        #task-form {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        input, textarea, button {
            padding: 10px;
            font-size: 1em;
            border: 1px solid #444;
            border-radius: 4px;
            background-color: #1e1e2f;
            color: #f5f5f5;
        }

        input:focus, textarea:focus {
            outline: none;
            border-color: #f1c40f;
            box-shadow: 0 0 5px #f1c40f;
        }

        button {
            cursor: pointer;
            background-color: #3498db;
            color: white;
            border: none;
            transition: background-color 0.3s;
        }

        button:hover {
            background-color: #2980b9;
        }

        textarea {
            resize: vertical;
            min-height: 100px;
        }

        /* Task List Styling */
        .task-list {
            margin-top: 30px;
        }

        .task {
            background-color: #3c3c4c;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 15px;
            transition: transform 0.3s, box-shadow 0.3s;
        }

        .task:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
        }

        .task h3 {
            margin-top: 0;
            font-size: 1.5em;
            color: #f39c12;
        }

        .task p {
            font-size: 1.1em;
            color: #bdc3c7;
        }

        /* Buttons inside tasks */
        .task button {
            margin-top: 10px;
            background-color: #e74c3c;
            font-size: 0.9em;
            transition: background-color 0.3s;
        }

        .task button.edit {
            background-color: #f39c12;
        }

        .task button:hover {
            background-color: #c0392b;
        }

        .task button.edit:hover {
            background-color: #e67e22;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .container {
                width: 95%;
                padding: 15px;
            }

            h1 {
                font-size: 2em;
            }

            .task-list {
                margin-top: 20px;
            }
        }

    </style>
</head>
<body>

    <!-- Main container for the page -->
    <div class="container">
        <h1>Task Management System</h1>

        <!-- Task creation form -->
        <form id="task-form">
            <input type="text" id="title" placeholder="Enter task title" required>
            <textarea id="description" placeholder="Enter task description"></textarea>
            <button type="submit">Add Task</button>
        </form>

        <!-- Task list display -->
        <div class="task-list" id="task-list"></div>
    </div>

    <script>
        // Fetch and display tasks
        async function fetchTasks() {
            const response = await fetch('/tasks');
            const tasks = await response.json();
            const taskList = document.getElementById('task-list');
            taskList.innerHTML = '';
            tasks.forEach(task => {
                const taskElement = document.createElement('div');
                taskElement.classList.add('task');
                taskElement.innerHTML = `
                    <h3>${task.title}</h3>
                    <p>${task.description || 'No description available'}</p>
                    <button class="edit" onclick="editTask(${task.id})">Edit</button>
                    <button onclick="deleteTask(${task.id})">Delete</button>
                `;
                taskList.appendChild(taskElement);
            });
        }

        // Create a task
        document.getElementById('task-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const title = document.getElementById('title').value;
            const description = document.getElementById('description').value;
            const response = await fetch('/tasks', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title, description })
            });
            await response.json();
            fetchTasks();  // Refresh the task list
            document.getElementById('title').value = '';
            document.getElementById('description').value = '';
        });

        // Delete a task
        async function deleteTask(id) {
            await fetch(`/tasks/${id}`, { method: 'DELETE' });
            fetchTasks();  // Refresh the task list
        }

        // Edit a task (For simplicity, this example uses prompts to update task)
        async function editTask(id) {
            const newTitle = prompt('Enter new task title:');
            const newDescription = prompt('Enter new task description:');
            await fetch(`/tasks/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title: newTitle, description: newDescription })
            });
            fetchTasks();  // Refresh the task list
        }

        // Load tasks on initial page load
        fetchTasks();
    </script>

</body>
</html>
