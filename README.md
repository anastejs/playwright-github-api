# playwright-github-api

Pet project for API testing automation of GitHub Issues using Playwright `APIRequestContext` and `pytest`.

The project covers a full GitHub Issue lifecycle via the REST API:

- Creates a temporary test repository before the suite runs
- Creates a new bug-report issue via the API
- Verifies the issue appears in the repository's Issues tab
- Deletes the test repository after all tests complete

## Installation

```bash
# Clone the repository
git clone https://github.com/anastejs/playwright-github-api.git
cd playwright-github-api

# Create and activate virtual environment
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass    # (optional) I needed this
venv\Scripts\activate       

# Install dependencies
pip install -r requirements.txt
playwright install
```

## Configuration

Create a `.env` file in the project root:

```env
GIT_USER=your_github_username
GIT_REPO=your_test_repo_name
GIT_ACCESS_TOKEN=your_personal_access_token
```

> ⚠️ The token needs `repo` scope to create and delete repositories.

## ▶Running tests

```bash
pytest -v -s
```

Screenshots are saved to `test-results/issues-page.jpg`.

---

## 📁 Project Structure

```
playwright-github-api/
├── tests/
│   ├── conftest.py              # session fixtures: API client, repo setup/teardown
│   └── test_github_issue.py     # test cases
├── test-results/                # screenshots output
├── .env                         # credentials (not committed)
├── .gitignore
└── README.md
```