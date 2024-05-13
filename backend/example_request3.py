# {% extends 'index.html' %}
#
# {% block title %}{{ title }}{% endblock %}
#
# {% block content %}
#
#     <div class="px-4 py-1 my-1">
#         <!-- Этот блок содержит форму для ввода данных пользователя -->
#         <img class="d-block mx-auto mb-4" src="{{ url_for('static', path='img/favicon.svg') }}" alt="" width="92" height="77">
#         <div class="display-5 fw-bold text-body-emphasis text-center mb-3">{{ title }}</div>
#
#         <!-- Форма отправки данных на сервер -->
#         <form class="row g-3 was-validated" method="post" id="loginForm" action="{{ url_for('login_for_access_token') }}">
#
#             <div class="mb-3">
#                 <label for="username" class="form-label">User name</label>
#                 <input type="text" class="form-control" id="username" name="username" required>
#                 <div class="invalid-feedback">Example: Jon or Eni</div>
#             </div>
#
#             <div class="mb-3">
#                 <label for="email" class="form-label">Email address</label>
#                 <input type="email" class="form-control" id="email" name="email" required>
#                 <div class="invalid-feedback">Example: example@mail.com</div>
#             </div>
#
#             <div class="mb-3">
#                 <label for="password" class="form-label">Password</label>
#                 <input type="password" class="form-control" id="password" name="password" required>
#                 <div class="invalid-feedback">Example: hj_45AA-werty</div>
#             </div>
#
#             <button type="submit" class="btn btn-primary" id="submit-btn">Submit</button>
#
#         </form>
#     </div>
#
#     JavaScript-код для отправки данных формы на сервер и обработки ответа
#     <script>
#         // Функция для отправки данных формы на сервер и обработки ответа
#         async function submitForm(event) {
#             event.preventDefault(); // Предотвращаем стандартное поведение отправки формы
#
#             // Создаем объект FormData для сбора данных формы
#             const formData = new FormData(event.target);
#             // Используем функцию url_for для получения пути к маршруту в FastAPI
#             const url = '{{ url_for("login_for_access_token") }}';
#
#             // Отправляем POST-запрос на сервер с данными формы
#             const response = await fetch(url, {
#                 method: 'POST', // Метод запроса
#                 body: formData // Отправляем данные формы
#             });
#
#             // Получаем JSON-ответ от сервера
#             const responseData = await response.json();
#
#             // Выводим ответ сервера в консоль для отладки
#             console.log(responseData);
#         }
#
#         // Добавляем обработчик события submit на форму с id="loginForm"
#         document.getElementById('loginForm').addEventListener('submit', submitForm);
#     </script>
#
# {% endblock content %}
