from creds import *
from playwright.sync_api import APIRequestContext, Page
# for loading variables from .env file
from dotenv import load_dotenv
import os

load_dotenv()
GITHUB_USER = os.getenv("GITHUB_USER")
GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_ACCESS_TOKEN= os.getenv("GITHUB_ACCESS_TOKEN")

# тест 1 - создаем новое issue в репозитории
def test_create_issue(api_context: APIRequestContext):        # получаем API-клиент
    issue_data = {
        "title": "[Bug] That failed",
        "body": "When running this, that failed with error.",
        "assignees": ["anastejs"],
    }

    issue = api_context.post(                                 # отправляем POST запрос - создаем новое issue
        f"/repos/{GITHUB_USER}/{GITHUB_REPO}/issues",
        data=issue_data,
    )
    assert issue.ok                                           # проверка - создалось ли issue? (status = 201 Created)


# тест 2 - проверка (скриншот) существования нового issue в нашем репозитории
def test_issue_page(page: Page):                              # получаем браузерную вкладку
    page.goto(f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}/issues")
    page.screenshot(path="test-results/issues-page.jpg", full_page=True)


# тест 3 - поиск созданного Issue во вкладке "Issues" в нашем репозитории
def test_new_issue_created(api_context: APIRequestContext):   # получаем API-клиент
    all_issues = api_context.get(f"/repos/{GITHUB_USER}/{GITHUB_REPO}/issues")   # отправляем GET запрос - получаем список всех issues
    assert all_issues.ok                                                         # проверка ответа 

    new_issue = [                                             # находим нужный issue по его названию
        issue 
        for issue in all_issues.json()
        if issue["title"] == "[Bug] That failed"
    ][0]

    # print("\nAll issues:")
    # for issue in all_issues.json():
    #     print(issue["title"])

    # проверка - создан именно тот Issue, который мы создавали
    assert new_issue["body"] == "When running this, that failed with error."     

# pytest -v -s