import sqlite3
import requests

# 1. Создаем базу данных и таблицу posts
def create_database():
    # подлючаемся к базе данных
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()

    # создаем таблицу posts
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            title TEXT,
            body TEXT
        )
    ''')

    # сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()

# 2. Получаем данные с сервера
def fetch_posts():
    # Отправка GET-запроса к API
    url = 'https://jsonplaceholder.typicode.com/posts'
    response = requests.get(url)

    # проверяем успешность запроса
    if response.status_code == 200:
        return response.json()  # возвращаем данные в формате JSON
    else:
        print(f"Криворучка. Ошибка при выполнении запроса: {response.status_code}")
        return []

# 3. Сохарняем данные в бд
def save_posts_to_db(posts):
    # подключаемся к бд
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()

    # вставляем данные в таблицу posts
    for post in posts:
        cursor.execute('''
            INSERT INTO posts (id, user_id, title, body)
            VALUES (?, ?, ?, ?)
        ''', (post['id'], post['userId'], post['title'], post['body']))

    # сохраняем изменения и закрываем соединени е
    conn.commit()
    conn.close()

# 4. Читаем данные из бд
def read_posts_by_user_id(user_id):
    # подключаемся к бд
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()

    # выполнение запроса для получения постов по user_id
    cursor.execute('''
        SELECT * FROM posts WHERE user_id = ?
    ''', (user_id,))

    # получаем наш заветный рещультат запросов постов
    posts = cursor.fetchall()

    # закрываем соадинение
    conn.close()

    return posts

# код программы
if __name__ == "__main__":
    # создание бд
    create_database()

    # получаем данные с сервера
    posts = fetch_posts()

    # созр в бд
    if posts:
        save_posts_to_db(posts)
        print("Данные успешно сохранены в базу данных.")
    else:
        print("Не удалось получить данные с сервера.")

    # читаем ланные из бд
    user_id = int(input("Введите user_id для поиска постов: "))
    user_posts = read_posts_by_user_id(user_id)

    # выводим данные
    if user_posts:
        print(f"Посты пользователя с user_id={user_id}:")
        for post in user_posts:
            print(f"ID: {post[0]}, Title: {post[2]}, Body: {post[3]}")
    else:
        print(f"Посты пользователя с user_id={user_id} не найдены.")