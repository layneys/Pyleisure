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
                    <img src="${found.images.image}" alt="Картинка мероприятия" onclick="clickLike(event, '${found.id}')">
                    <h3 class="card__title">${found.title.capitalize()}</h3>
                    <p class="card__subtitle">${found.parsed_body_text | truncate(1000, true)}</p>
                    ${found.place.title ? `<p>Место проведения: ${found.place.title}</p>` : ''}
                    ${found.place.address ? `<p>Адрес: ${found.place.address}</p>` : ''}
                    ${found.is_free ? '<p>Бесплатно</p>' : `<p>${found.price}</p>`}
                    ${found.site_url ? `<p>Сайт мероприятия: ${found.site_url}</p>` : ''}
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

    try {
        const response = await fetch(`/liked/${eventId}`, {
            method: "POST"
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
