let token = null;

let socket = null;

let username = "";


// -------------------------
// REGISTER
// -------------------------

async function register() {

    username =
        document.getElementById(
            "username"
        ).value.trim();


    const password =
        document.getElementById(
            "password"
        ).value;


    if (!username || !password) {

        showAuthMessage(
            "Enter username and password"
        );

        return;
    }


    const response = await fetch(
        `http://127.0.0.1:8000/register?username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`,
        {
            method: "POST"
        }
    );


    const data =
        await response.json();


    showAuthMessage(
        data.message || data.detail
    );
}


// -------------------------
// LOGIN
// -------------------------

async function login() {

    username =
        document.getElementById(
            "username"
        ).value.trim();


    const password =
        document.getElementById(
            "password"
        ).value;


    if (!username || !password) {

        showAuthMessage(
            "Enter username and password"
        );

        return;
    }


    const response = await fetch(
        `http://127.0.0.1:8000/login?username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`,
        {
            method: "POST"
        }
    );


    const data =
        await response.json();


    if (!response.ok) {

        showAuthMessage(
            data.detail
        );

        return;
    }


    token =
        data.access_token;


    document
        .getElementById(
            "auth-section"
        )
        .classList.add("hidden");


    document
        .getElementById(
            "chat-section"
        )
        .classList.remove("hidden");


    showAuthMessage("");
}


// -------------------------
// CONNECT TO ROOM
// -------------------------

function connect() {

    const room =
        document.getElementById(
            "room"
        ).value;


    if (!token) {

        alert(
            "Please login first"
        );

        return;
    }


    // Close previous connection

    if (socket) {

        socket.close();
    }


    socket = new WebSocket(
        `ws://127.0.0.1:8000/ws/${room}?token=${token}`
    );


    socket.onopen = function() {

        document
            .getElementById(
                "room-title"
            )
            .innerText =
                `Room: ${room}`;


        document
            .getElementById(
                "messages"
            )
            .innerHTML = "";


        loadHistory(room);
    };


    socket.onmessage = function(event) {

        const data =
            JSON.parse(
                event.data
            );


        displayMessage(data);
    };


    socket.onclose = function() {

        console.log(
            "WebSocket disconnected"
        );
    };
}


// -------------------------
// LOAD CHAT HISTORY
// -------------------------

async function loadHistory(room) {

    const response = await fetch(
        `http://127.0.0.1:8000/rooms/${room}/messages?token=${token}`
    );


    if (!response.ok) {

        return;
    }


    const messages =
        await response.json();


    messages.forEach(
        message => {

            displayMessage(
                message
            );

        }
    );
}


// -------------------------
// DISPLAY MESSAGE
// -------------------------

function displayMessage(data) {

    const messages =
        document.getElementById(
            "messages"
        );


    const element =
        document.createElement(
            "div"
        );


    if (
        data.type ===
        "notification"
    ) {

        element.className =
            "notification";


        element.innerText =
            `🔔 ${data.message}`;

    }

    else {

        element.className =
            "message";


        element.innerText =
            `${data.username}: ${data.content}`;
    }


    messages.appendChild(
        element
    );


    messages.scrollTop =
        messages.scrollHeight;
}


// -------------------------
// SEND MESSAGE
// -------------------------

function sendMessage() {

    const input =
        document.getElementById(
            "message"
        );


    const content =
        input.value.trim();


    if (
        !content ||
        !socket ||
        socket.readyState !== WebSocket.OPEN
    ) {

        return;
    }


    socket.send(
        JSON.stringify({
            content: content
        })
    );


    input.value = "";
}


// -------------------------
// ENTER KEY
// -------------------------

function handleEnter(event) {

    if (
        event.key ===
        "Enter"
    ) {

        sendMessage();
    }
}


// -------------------------
// LOGOUT
// -------------------------

function logout() {

    if (socket) {

        socket.close();

        socket = null;
    }


    token = null;

    username = "";


    document
        .getElementById(
            "chat-section"
        )
        .classList.add("hidden");


    document
        .getElementById(
            "auth-section"
        )
        .classList.remove("hidden");


    document
        .getElementById(
            "messages"
        )
        .innerHTML = "";
}


// -------------------------
// AUTH MESSAGE
// -------------------------

function showAuthMessage(
    message
) {

    document
        .getElementById(
            "auth-message"
        )
        .innerText = message;
}