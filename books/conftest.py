import pytest
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

from books.models import Author, Book, Publisher, Genre


@pytest.fixture
def authors():
    lst = []
    lst.append(Author.objects.create(first_name="Adam", last_name="Mckiewicz"))
    lst.append(Author.objects.create(first_name="Juliusz", last_name="Słowacki"))
    lst.append(Author.objects.create(first_name="Andrzej", last_name="Sapkowski"))
    lst.append(Author.objects.create(first_name="JRR", last_name="Tolkien"))
    lst.append(Author.objects.create(first_name="Andre", last_name="Norton"))
    return lst

@pytest.fixture
def publishers():
    lst = []
    for i in range(5):
        lst.append(Publisher.objects.create(name=f"Publisher {i}", year=i+2000))
    return lst

@pytest.fixture
def genres():
    lst = []
    for i in range(5):
        lst.append(Genre.objects.create(name=f"Genre {i}"))
    return lst


@pytest.fixture
def user():
    return User.objects.create_user(username="testowy", password="ala ma kota")


@pytest.fixture
def user_with_permissions(user):
    ct = ContentType.objects.get(model='genre')
    ct2 = ContentType.objects.get(model='book')
    permissions = Permission.objects.filter(content_type=ct)
    p2 = Permission.objects.filter(content_type=ct2)
    user.user_permissions.set(permissions)
    for item in p2:
        user.user_permissions.add(item)
    return user


@pytest.fixture
def books(authors, publishers, genres):
    lst = []
    for i in range(5):
        b = Book.objects.create(title=f"{i}", author=authors[i],
                            publisher=publishers[i])
        b.genres.add(genres[i])
        lst.append(b)
    return lst

