const API_URL = "/api";


async function loadTasks() {

    const response = await fetch(`${API_URL}/tasks`);

    const tasks = await response.json();

    const tasksContainer = document.getElementById("tasks");

    tasksContainer.innerHTML = "";

    tasks.forEach(task => {

        const taskElement = document.createElement("div");

        taskElement.className = "task";

        if (task.completed) {
            taskElement.classList.add("completed");
        }

        taskElement.innerHTML = `
            <h3>${task.title}</h3>
            <p>${task.description || ""}</p>

            <button onclick='toggleTask(${JSON.stringify(task)})'>
                ${task.completed ? "Uncomplete" : "Complete"}
            </button>

            <button onclick="deleteTask(${task.id})">
                Delete
            </button>
        `;

        tasksContainer.appendChild(taskElement);
    });
}


async function createTask() {

    const title = document.getElementById("title").value;

    const description =
        document.getElementById("description").value;

    const response = await fetch(`${API_URL}/tasks`, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            title: title,
            description: description
        })
    });

    if (response.ok) {

        document.getElementById("title").value = "";
        document.getElementById("description").value = "";

        loadTasks();
    }
}

async function toggleTask(task) {

    const response = await fetch(`${API_URL}/tasks/${task.id}`, {

        method: "PUT",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            title: task.title,
            description: task.description,
            completed: !task.completed
        })
    });

    if (response.ok) {
        loadTasks();
    }
}

async function deleteTask(id) {

    await fetch(`${API_URL}/tasks/${id}`, {

        method: "DELETE"
    });

    loadTasks();
}


loadTasks();
