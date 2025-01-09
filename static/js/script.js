
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

async function openLiked(event) {
    event.preventDefault(); // Предотвращаем перезагрузку страницы

    // Отображаем индикатор загрузки
    document.getElementById("result-container").innerHTML = "Загрузка...";

    try {
        const response = await fetch("/liked", {
            method: "GET"
        });

        if (!response.ok) {
            throw new Error(`Ошибка при получении данных: ${response.statusText}`);
        }

        // Получаем JSON-ответ
        const data = await response.json();
        // Генерируем HTML для карточек "Любимое"
        let html = '';
        for (const found of data) {
            html += `
                <div class="card">
                    <img src="${found.event_img}" alt="Картинка мероприятия" onclick="clickLike(event, '${found.event_id}')">
                    <h3 class="card__title">${found.event_title}</h3>
                    <p class="card__subtitle">${found.event_description}</p>
                    ${found.event_place ? `<p>Адрес: ${found.event_place}</p>` : ''}
                    <p>${found.event_price}</p>
                    ${found.event_url ? `<p>Сайт мероприятия: ${found.event_url}</p>` : ''}
                </div>
                <hr>
            `;
        }

        // Вставляем HTML-ответ в элемент с id="result-container"
        document.getElementById("result-container").innerHTML = html;
    } catch (error) {
        console.error("Ошибка при загрузке данных:", error);
        document.getElementById("result-container").innerHTML = "Произошла ошибка. Попробуйте снова.";
    }
}


async function clickLike(event, eventId) {
    event.preventDefault(); // Предотвращаем перезагрузку страницы

    const data = {
        id: eventId,
    };

    try {
        const response = await fetch(`/liked/${eventId}`, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`Ошибка при лайке: ${response.statusText}`);
        }

        console.log("Лайк успешно отправлен");
        // Добавляем класс 'clicked' к кнопке
        event.target.classList.add('clicked');
    } catch (error) {
        console.error("Ошибка при лайке:", error);
    }
}
