import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Фикстура для настройки базы данных перед тестами и её очистки после."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Фикстура для получения соединения с базой данных и его закрытия после теста."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Тест создания базы данных и таблицы пользователей."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Таблица 'users' должна существовать в базе данных."

def test_add_new_user(setup_database, connection):
    """Тест добавления нового пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Пользователь должен быть добавлен в базу данных."

# Возможные варианты тестов:
"""
Тест добавления пользователя с существующим логином.
Тест успешной аутентификации пользователя.
Тест аутентификации несуществующего пользователя.
Тест аутентификации пользователя с неправильным паролем.
Тест отображения списка пользователей.
"""
def test_add_existing_user(setup_database, connection):
    """Тест добавления пользователя с существующим логином."""
    add_user('testuser', 'testuser@example.com', 'password123')
    # Попытка добавить пользователя с тем же логином
    with pytest.raises(ValueError):
        add_user('testuser', 'another@example.com', 'anotherpassword')
def test_authenticate_user_success(setup_database):
    """Тест успешной аутентификации пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    result = authenticate_user('testuser', 'password123')
    assert result, "Пользователь должен быть успешно аутентифицирован."
def test_authenticate_user_nonexistent(setup_database):
    """Тест аутентификации несуществующего пользователя."""
    result = authenticate_user('nonexistent', 'password123')
    assert not result, "Аутентификация несуществующего пользователя должна завершиться неудачей."
def test_authenticate_user_wrong_password(setup_database):
    """Тест аутентификации пользователя с неправильным паролем."""
    add_user('testuser', 'testuser@example.com', 'password123')
    result = authenticate_user('testuser', 'wrongpassword')
    assert not result, "Аутентификация пользователя с неправильным паролем должна завершиться неудачей."
def test_display_users(setup_database, connection):
    """Тест отображения списка пользователей."""
    add_user('testuser1', 'testuser1@example.com', 'password123')
    add_user('testuser2', 'testuser2@example.com', 'password456')
    users = display_users()
    assert len(users) == 2, "Должно быть 2 пользователя в списке."
    usernames = [user[1] for user in users] 
    