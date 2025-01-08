async function submitForm(event) {
    event.preventDefault(); // Предотвращаем перезагрузку страницы

    const formData = new FormData(event.target);
    const textInputValue = document.getElementById("text-input").value;
    formData.append("prompt", textInputValue);

    // Отображаем индикатор загрузки
    document.getElementById("result-container").innerHTML = "Загрузка...";

    try {
        const response = await fetch("/list", {
            method: "POST",
            body: formData
        });

        // Получаем HTML-ответ
        const html = await response.text();

        // Вставляем HTML-ответ в элемент с id="result-container"
        document.getElementById("result-container").innerHTML = html;
    } catch (error) {
        console.error("Ошибка при загрузке данных:", error);
        document.getElementById("result-container").innerHTML = "Произошла ошибка. Попробуйте снова.";
    }
}
