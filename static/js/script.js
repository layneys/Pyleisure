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

async function handleIdClick(element) {
            // Создаем объект FormData для отправки POST-запроса
            const formData = new FormData();
            const id = element.textContent.trim();
            formData.append("id", id);

            // Отправляем POST-запрос
            const response = await fetch("/event", {
                method: "POST",
                body: formData
            });

            // Получаем HTML-ответ
            const html = await response.text();

            // Вставляем HTML-ответ в контейнер с id="result-container"
            document.getElementById("result-container").innerHTML = html;
        }

