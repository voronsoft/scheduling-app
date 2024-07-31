**1. Отправляем на этот ендпоинт  (допустим с страницы авторизации login.html)**
http://adress_backend/api_admin/registration

```code  
{
    username: username,
    mail: mail,
    password: password,
}
```

**2. Получаем ответ сервера:**

```code
{
    access_token: string,
    token_type: string
}
```

**3. Сохраняем на стороне фронтенда полученные данные**

**4. Если токен получен отправляем пользователя на главную страницу админ-панели**
В запросе так же должен присутствовать заголовок с данными о токене.

**Перечень ендпоинтов требующих заголовок авторизации с токеном:**
```code
/api_admin/get_lessons_for_a_month/{date_y_m_d}

/api_admin/delete_lesson_frontend/{lesson_id}

/api_admin/change_lesson_data/{lesson_id}

/api_admin/get_lesson_data/{lesson_id}
```