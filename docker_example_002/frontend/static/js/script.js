const API_URL = "http://localhost:5000/persons";

const form = document.getElementById("personForm");
const personsContainer = document.getElementById("personsContainer");
const message = document.getElementById("message");
const btn = document.getElementById("btn");

/* Button click */
btn.addEventListener("click", () => {
    alert("Button clicked!");
});

/* Load persons */
async function fetchPersons() {
    try {
        const res = await fetch(API_URL);
        const data = await res.json();
        renderPersons(data);
    } catch (err) {
        showMessage("Failed to load persons", "red");
    }
}

/* Render list */
function renderPersons(persons) {
    personsContainer.innerHTML = "";

    if (persons.length === 0) {
        personsContainer.innerHTML = "<p>No persons found</p>";
        return;
    }

    persons.forEach(p => {
        const div = document.createElement("div");
        div.classList.add("person-card");

        div.innerHTML = `
            <p><b>ID:</b> ${p.id}</p>
            <p><b>Name:</b> ${p.name}</p>
            <p><b>Age:</b> ${p.age}</p>
            <p><b>Gender:</b> ${p.isMale ? "Male" : "Female"}</p>

            <button class="delete-btn" onclick="deletePerson(${p.id})">
                Delete
            </button>
        `;

        personsContainer.appendChild(div);
    });
}

/* Create person */
form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const person = {
        name: document.getElementById("name").value,
        age: Number(document.getElementById("age").value),
        isMale: document.getElementById("isMale").value === "true"
    };

    try {
        const res = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(person)
        });

        const data = await res.json();

        if (!res.ok) {
            showMessage(data.error, "red");
            return;
        }

        showMessage("Person added successfully!", "green");
        form.reset();
        fetchPersons();

    } catch (err) {
        showMessage("Error creating person", "red");
    }
});

/* Delete person */
async function deletePerson(id) {
    try {
        const res = await fetch(`${API_URL}/${id}`, {
            method: "DELETE"
        });

        const data = await res.json();

        if (!res.ok) {
            showMessage(data.error, "red");
            return;
        }

        showMessage(data.message, "green");
        fetchPersons();

    } catch (err) {
        showMessage("Delete failed", "red");
    }
}

/* Message helper */
function showMessage(text, color) {
    message.textContent = text;
    message.style.color = color;

    setTimeout(() => {
        message.textContent = "";
    }, 3000);
}

/* init */
fetchPersons();