import pytest
from django.test import TestCase
from django.test import Client
from django.urls import reverse

from books.models import Author, Publisher, Book


# Create your tests here.
@pytest.mark.django_db
def test_index_view():
    c = Client()
    url = "/"
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_author_view_get(authors):
    c = Client()
    url = reverse('add_author')
    response = c.get(url)
    assert response.status_code == 200
    assert response.context["authors"].count() == len(authors)
    for author in authors:
        assert author in response.context["authors"]

@pytest.mark.django_db
def test_add_author_view_post(authors):
    c = Client()
    url = reverse('add_author')
    data = {
        'first_name': 'John',
        'last_name': 'Doe',
    }
    response = c.post(url, data)
    assert response.status_code == 302
    assert Author.objects.get(**data)


@pytest.mark.django_db
def test_add_publisher_post():
    c = Client()
    url = reverse('add_publisher')
    data = {
        'name':'ala_ma_kotas',
        'year':1999
    }
    response = c.post(url, data)
    assert response.status_code == 302
    assert Publisher.objects.get(**data)


@pytest.mark.django_db
def test_add_publisher_post_not_valid():
    c = Client()
    url = reverse('add_publisher')
    data = {
        'name':'ala_ma_kota',
        'year':1999
    }

    response = c.post(url, data)
    form = response.context["form"]

    assert response.status_code == 200
    assert form.errors
    assert not Publisher.objects.exists()

@pytest.mark.django_db
def test_book_list_view_without_login():
    c = Client()
    url = reverse('list_book')
    response = c.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_book_list_view_login(user, books):
    c = Client()
    c.force_login(user)
    url = reverse('list_book')
    data = {
        'title':'1'
    }
    response = c.get(url, data)
    assert response.status_code == 200
    assert response.context["obj_list"].count() == 1


@pytest.mark.django_db
def test_add_book_view_post(authors, publishers, genres):
    c = Client()
    url = reverse('add_book')
    data = {
        'title':'testowy',
        'author':authors[0].id,
        'publisher':publishers[0].id,
        'genres':[genre.id for genre in genres],
    }
    response = c.post(url, data)
    assert response.status_code == 302
    assert Book.objects.get(title='testowy')


@pytest.mark.django_db
def test_add_book_view_put(authors):
    c = Client()
    url = reverse('update_author', args=[authors[0].id])
    data = {
        'first_name':'Kuba',
        'last_name':'beeee',
    }
    response = c.post(url, data)
    assert response.status_code == 302
    assert Author.objects.get(**data)


@pytest.mark.django_db
def test_book_list_view_with_out_perm(user, books):
    c = Client()
    c.force_login(user)
    url = reverse('add_genre')
    response = c.get(url)
    assert response.status_code == 403

@pytest.mark.django_db
def test_book_list_view_with_perm(user_with_permissions, books):
    c = Client()
    c.force_login(user_with_permissions)
    url = reverse('add_genre')
    response = c.get(url)
    assert response.status_code == 200
