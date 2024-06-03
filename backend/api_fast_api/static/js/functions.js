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
        }, body: JSON.stringify({ // Преобразуем данные формы в JSON-строку
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


// ----------- Функция для подтверждения урока
async function changeLessonStatus(lesson_id) {
    try {
        // Создаем тело запроса с данными занятия
        const requestBody = JSON.stringify({lesson_id: lesson_id});
        // Отправляем POST-запрос на сервер для изменения статуса урока
        const response = await fetch(`/change-lesson-status`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: requestBody
        });

        // Проверяем статус ответа
        const data = await response.json();
        if (response.status === 200) {
            // Если ответ успешный (статус 200), обновляем страницу
            location.reload();
        } else {
            // Если произошла ошибка, выводим сообщение
            alert('Error deleting lesson.');
        }
    } catch (error) {
        // Обработка ошибок сети или других ошибок
        console.error('Error:', error);
        alert('An error occurred while editing the lesson.');
    }
}


// ----------- Функция для удаления урока
async function deleteLesson(lesson_id) {
    try {
        // Создаем тело запроса с данными занятия
        const requestBody = JSON.stringify({lesson_id: lesson_id});
        // Отправляем DELETE-запрос на сервер для удаления урока
        const response = await fetch(`/delete-lesson`, {
            method: 'DELETE',
            headers: {'Content-Type': 'application/json'},
            body: requestBody
        });
        console.log("===========", response.status)
        // Проверяем статус ответа
        if (response.status === 200) {
            // Если ответ успешный (статус 200), обновляем страницу
            location.reload();

        } else {
            // Если произошла ошибка, выводим сообщение
            alert('Error deleting lesson.');
        }
    } catch (error) {
        // Обработка ошибок сети или других ошибок
        console.error('Error:', error);
        alert('An error occurred while deleting the lesson.');
    }
}
