async function submitForm(event) {
            event.preventDefault(); // Предотвращаем перезагрузку страницы

            const formData = new FormData(event.target);
            const response = await fetch("/list", {
                method: "POST",
                body: formData
            });

            // Получаем HTML-ответ
            const html = await response.text();

            // Вставляем HTML-ответ в элемент с id="result-container"
            document.getElementById("result-container").innerHTML = html;
        }

