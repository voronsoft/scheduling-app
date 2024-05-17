// ----------- Функция для сохранения данных из словаря в localStorage
async function saveTokenToLocalStorage(tokenDict) {
    if (typeof tokenDict !== 'object' || tokenDict === null) {
        console.error("Ошибка: Ожидается объект dict в качестве аргумента.");
        return false;
    }

    if (!('access_token' in tokenDict) || !('token_type' in tokenDict)) {
        console.error("Ошибка: Отсутствуют обязательные ключи в словаре.");
        return false;
    }

    const tokenString = tokenDict.token_type + ' ' + tokenDict.access_token;

    localStorage.setItem('Authorization', tokenString);

    console.log("Данные успешно сохранены в localStorage.");
    return true;
}


// ----------- Функция для проверки наличия ключа "Authorization" в localStorage и возврата его значения
async function getTokenFromLocalStorage() {
    const tokenString = localStorage.getItem('Authorization');

    if (tokenString !== null) {
        return tokenString;
    } else {
        return false;
    }
}


// ----------- Функция для добавления заголовка Authorization к запросу
async function addAuthorizationHeaderToRequest(request) {
    const token = await getTokenFromLocalStorage();

    if (token !== false) {
        request.setRequestHeader('Authorization', token);
        console.log("Заголовок 'Authorization' успешно добавлен к запросу.");
        return true;
    } else {
        console.error("Ошибка: Токен отсутствует в localStorage.");
        return false;
    }
}


// ----------- Функция для удаления данных о токене из localStorage
async function clearTokenFromLocalStorage() {
    if (!localStorage.getItem('Authorization')) {
        console.log("Ключ 'Authorization' не найден в localStorage.");
        return false;
    }

    localStorage.removeItem('Authorization');

    console.log("Данные о токене успешно удалены из localStorage.");
    return true;
}


// ----------- Функция для очистки токена при закрытии вкладки или браузера
async function clearTokenOnTabOrBrowserClose() {
    await clearTokenFromLocalStorage();
}


// ----------- Функция для отправки данных формы на сервер из файла authorization.html
async function submitFormAuthorization(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    // Получаем URL-адрес ендпоинта из атрибута data-url формы
    const url = document.getElementById('loginForm').getAttribute('action');

    const response = await fetch(url, {
        method: 'POST',
        body: formData
    });
    // Перехватываем ответ сервера
    await intercepting_server_response(response);
}


// ----------- Функция для отправки данных формы на сервер из файла registration.html
async function submitFormRegistration(event) {
    event.preventDefault(); // Предотвращаем стандартное поведение отправки формы

    // Создаем объект FormData для сбора данных формы
    const formData = new FormData(event.target);
    // Используем функцию url_for для получения пути к маршруту в FastAPI
    //const url = '/registration';
    // Получаем URL-адрес ендпоинта из атрибута data-url формы
    const url = document.getElementById('registrationForm').getAttribute('action');

    // Отправляем POST-запрос на сервер с данными формы
    const response = await fetch(url, {
        method: 'POST', // Метод запроса
        headers: {
            'Content-Type': 'application/json' // Устанавливаем заголовок Content-Type для отправки JSON
        },
        body: JSON.stringify({ // Преобразуем данные формы в JSON-строку
            username: formData.get('username'), // Получаем значение поля username
            email: formData.get('email'), // Получаем значение поля email
            password: formData.get('password') // Получаем значение поля password
        })
    });

    // Получаем JSON-ответ от сервера
    const responseData = await response.json();

    // Выводим ответ сервера в консоль для отладки
    console.log(responseData);
}


// ----------- Функция перехвата ответа сервера на запрос при авторизации
// Функция для перехвата ответа сервера
async function intercepting_server_response(response) {
    // Получаем статус ответа
    const responseStatus = await response.status;

    // Получаем тело ответа
    const responseBody = await response.text();

    // Проверяем, если статус ответа 200
    if (responseStatus === 200) {
        // Попытка преобразовать тело ответа в формат JSON
        try {
            const responseBodyJSON = JSON.parse(responseBody); // Пункт 6

            // Проверяем, есть ли ключи access_token и token_type в ответе
            if (responseBodyJSON.hasOwnProperty('access_token') && responseBodyJSON.hasOwnProperty('token_type')) {
                // Выводим ответ сервера в консоль для отладки
                console.log("Ответ из intercepting_server_response", responseBodyJSON);
                // Возвращаем JSON с данными
                return responseBodyJSON;
            } else {
                // Если ключи access_token и token_type отсутствуют, возвращаем false
                return false; // Пункт 8
            }
        } catch (error) {
            // Если произошла ошибка при преобразовании тела ответа в JSON, возвращаем false
            return false; // Пункт 8
        }
    } else {
        // Выводим ответ сервера в консоль для отладки
        console.log("Проверка", responseBody);
        // Если статус ответа не 200, вызываем функцию для обработки ошибок
        await handleServerError(responseBody); // Передаем ответ сервера в функцию handleServerError

        return false; // Возвращаем false, так как не удалось получить данные
    }
}


// ----------- Функция перехвата ответа сервера на запрос при авторизации
async function handleServerError(responseBody) {
    console.log("1 Ответ сервера", responseBody);

    try {
        // Формируем объект с данными для отправки на сервер
        const requestData = {
            method: 'POST', // Метод запроса POST
            headers: {
                // Устанавливаем заголовок Content-Type для отправки JSON
                'Content-Type': 'application/json'
            },
            // Преобразуем текст ответа в JSON и отправляем его на сервер
            body: JSON.stringify({error_message: responseBody})
        };

        // Отправляем запрос в маршрут /error
        const responseFromServer = await fetch('/error', requestData);
        // Если запрос завершился успешно
        if (responseFromServer.ok) {
            console.log('Сообщение об ошибке успешно отправлено на сервер.');
            // Получаем HTML из тела ответа от сервера
            const htmlResponse = await responseFromServer.text();
            // Вставляем HTML внутрь текущей страницы
            document.body.innerHTML += htmlResponse;
            // Получаем ссылку на модальное окно
            const modal = document.querySelector('.modal');
            // Создаем объект модального окна с помощью Bootstrap
            const modalInstance = new bootstrap.Modal(modal);
            // Открываем модальное окно
            modalInstance.show();
        } else {
            console.error('Не удалось отправить сообщение об ошибке на сервер.');
        }
    } catch (error) {
        console.error('Ошибка обработки ошибки сервера:', error);
    }
}



