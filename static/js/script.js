function sendMessage() {
	const input = document.getElementById("user-input");
	const messageText = input.value.trim();

	if (messageText !== "") {
		const chatBox = document.getElementById("chat-box");
		const message = document.createElement("div");
		message.classList.add("message", "user");
		message.textContent = messageText;

		chatBox.appendChild(message);
		chatBox.scrollTop = chatBox.scrollHeight; // Rolar para a última mensagem

		input.value = ""; // Limpar o campo de entrada
	}

	return messageText;
}

function apiMessage(response) {
	if (response !== "") {
		const chatBox = document.getElementById("chat-box");
		const message = document.createElement("div");
		message.classList.add("message", "api");
		message.textContent = response;

		chatBox.appendChild(message);
		chatBox.scrollTop = chatBox.scrollHeight; // Rolar para a última mensagem
	}
}

async function sendInput(question) {
	const response = await fetch("http://127.0.0.1:5000/chatbot/process", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ question }),
	});

	const data = await response.json();
	console.log(data.result);
	apiMessage(data.result);
}

async function main() {
	let userQuestion = sendMessage();

	sendInput(userQuestion);
}

// Permitir enviar mensagem ao pressionar Enter
document
	.getElementById("user-input")
	.addEventListener("keypress", function (event) {
		if (event.key === "Enter") {
			main();
		}
	});

// document.getElementById("send-btn").addEventListener("click", main);
