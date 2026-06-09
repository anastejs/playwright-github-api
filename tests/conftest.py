import pytest
# from creds import *
from playwright.sync_api import *
# for loading variables from .env file
from dotenv import load_dotenv
import os

load_dotenv()
GITHUB_USER = os.getenv("GIT_USER")
GITHUB_REPO = os.getenv("GIT_REPO")
GITHUB_ACCESS_TOKEN= os.getenv("GIT_ACCESS_TOKEN")


@pytest.fixture(scope="session")                            # session - создать один раз, использовать для всех тестов и закрыть в конце
def api_context(playwright: Playwright):
    headers = {
        "Accept": "application/vnd.github.v3+json",         # хотим получать ответы в формате GitHub API v3
        "Authorization": f"token {GITHUB_ACCESS_TOKEN}"     # acces token (аналог логина)
    }
    context = playwright.request.new_context(               # cоздание API клиента
        base_url="https://api.github.com/",
        extra_http_headers=headers,
    )
    yield context                                           # передаём клиент тестам
    context.dispose()                                       # закрываем API клиент

# Test hook для создания тестового репозитория 
@pytest.fixture(autouse=True, scope="session")              # autouse - не нужно явно вызывать fixture, pytest запустит сам, session - запустится один раз перед всеми тестами
def create_test_repository(api_context: APIRequestContext):
    # Create the repo
    post_response = api_context.post(                       # отправляем POST запрос, GitHub получает JSON и создаёт репозиторий
        "/user/repos",
        data={"name": GITHUB_REPO}
    )
    assert post_response.ok                                 # проверка - создался ли репозиторий? (status = 201 Created)

    yield

    # Delete the repo
    delete_response = api_context.delete(f"/repos/{GITHUB_USER}/{GITHUB_REPO}")    # отправляем DELETE запрос
    assert delete_response.ok                               # проверка - удалился ли репозиторий? (status = 204 No Content)
