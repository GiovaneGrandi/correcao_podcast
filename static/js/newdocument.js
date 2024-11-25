async function sendInput(title, cadeira, file) {
	const formData = new FormData();
	formData.append("title", title);
	formData.append("cadeira", cadeira);
	formData.append("file", file);

	const response = await fetch("http://127.0.0.1:5000/newdocument", {
		method: "POST",
		body: formData,
	});

	if (!response.ok) {
		throw new Error("Erro ao enviar os dados.");
	}
}

document
	.getElementById("contentForm")
	.addEventListener("submit", async function (event) {
		event.preventDefault();

		const title = document.getElementById("title").value;
		const cadeira = document.getElementById("cadeira").value;
		const fileInput = document.getElementById("content");
		const file = fileInput.files[0];

		if (!file) {
			alert("Por favor, selecione um arquivo antes de enviar.");
			return;
		}

		try {
			await sendInput(title, cadeira, file);
			document.getElementById("successMessage").style.display = "block";

			document.getElementById("contentForm").reset();
		} catch (error) {
			console.error("Erro ao enviar dados:", error);
			alert("Erro ao enviar os dados. Tente novamente.");
		}
	});
