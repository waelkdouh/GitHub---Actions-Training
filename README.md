# GitHub Actions Training — Hands-On Labs

A comprehensive, hands-on training repository covering GitHub Actions fundamentals: workflows, custom actions (Composite, Docker, JavaScript), matrix testing, caching, environments with approval gates, deployment to Azure, release automation, and efficiency best practices.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Repository Structure](#repository-structure)
- [Lab 1: Simple Workflow](#lab-1-simple-workflow)
- [Lab 2: Release & Notify on Microsoft Teams](#lab-2-release--notify-on-microsoft-teams)
- [Lab 3: Python Application Code (src & tests)](#lab-3-python-application-code-src--tests)
- [Lab 4: Caching Dependencies](#lab-4-caching-dependencies)
- [Lab 5: Reusable Workflow — Python Standard Checks](#lab-5-reusable-workflow--python-standard-checks)
- [Lab 6: Matrix Testing — Python Package Testing](#lab-6-matrix-testing--python-package-testing)
- [Lab 7: Composite Action — Python Environment Setup](#lab-7-composite-action--python-environment-setup)
- [Lab 8: Docker Action — Hello Docker](#lab-8-docker-action--hello-docker)
- [Lab 9: JavaScript Action — Hello JS](#lab-9-javascript-action--hello-js)
- [Lab 10: Environments & Deployment to Azure](#lab-10-environments--deployment-to-azure)
- [Lab 11: Efficiency — Concurrency, Timeouts & Inputs](#lab-11-efficiency--concurrency-timeouts--inputs)

---

## Prerequisites

Before starting the labs, ensure you have the following:

| Requirement | Details |
|---|---|
| **GitHub Account** | Free or Pro account at [github.com](https://github.com) |
| **Git** | Installed locally — [Download Git](https://git-scm.com/downloads) |
| **Python 3.9+** | Installed locally — [Download Python](https://www.python.org/downloads/) |
| **Node.js version 20.x. Don't get a newer version of Node as its not supported by Github Actions** | Required for Lab 9 (JavaScript Action) — [Download Node.js](https://nodejs.org/) |
| **npm** | Comes bundled with Node.js |
| **Azure Subscription** | Required for Lab 10 (Environments & Deployment) — [Free Azure Account](https://azure.microsoft.com/free/) |
| **Azure CLI** | Required for Lab 10 — [Install Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) |
| **VS Code (recommended)** | [Download VS Code](https://code.visualstudio.com/) |

---

## Repository Structure

```
GitHub---Actions-Training/
├── .github/
│   ├── actions/
│   │   ├── DockerAction/          # Lab 8 — Custom Docker action
│   │   │   ├── action.yml
│   │   │   ├── Dockerfile
│   │   │   └── entrypoint.sh
│   │   ├── JavaScriptAction/      # Lab 9 — Custom JavaScript action
│   │   │   ├── action.yml
│   │   │   ├── index.js
│   │   │   ├── package.json
│   │   │   ├── package-lock.json
│   │   │   ├── dist/
│   │   │   │   └── index.js       # Bundled output (committed)
│   │   │   └── node_modules/      # Git-ignored
│   │   └── python-setup/          # Lab 7 — Custom Composite action
│   │       └── action.yml
│   └── workflows/
│       ├── SimpleWorkflow.yml                # Lab 1
│       ├── Release and notify on teams.yml   # Lab 2
│       ├── Caching.yml                       # Lab 4
│       ├── python-standard-checks.yml        # Lab 5 (reusable workflow)
│       ├── Python Package Testing.yml        # Lab 6
│       ├── ConsumeCompositeAction.yml        # Lab 7
│       ├── ConsumeDockerAction.yml           # Lab 8
│       ├── ConsumeJavaScriptAction.yml       # Lab 9
│       ├── environments.yml                  # Lab 10
│       └── Efficiency.yml                    # Lab 11
├── src/
│   ├── __init__.py
│   └── calculator.py              # Simple calculator module
├── tests/
│   ├── __init__.py
│   └── test_math.py               # Pytest test suite
├── requirements.txt                # Python dependencies
├── .gitignore
└── README.md
```

---

### Lab 1: Simple Workflow

**Goal:** Create your first GitHub Actions workflow and understand the basic structure (triggers, jobs, steps, runners).

#### Step 1 — Create the Workflow File

Create the file `.github/workflows/SimpleWorkflow.yml` with the following content:

```yaml
name: Simple Workflow
run-name: Simple Workflow run by ${{ github.actor }}

on:
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Run a one-line script
        run: echo Hello, world!

      - name: Run a multi-line script
        run: |
          echo Add other actions to build,
          echo test, and deploy your project.
```

#### Step 2 — Key Concepts

| Concept | Explanation |
|---|---|
| `name` | Display name of the workflow in the Actions tab |
| `run-name` | Dynamic name for each run — uses `github.actor` context |
| `on: workflow_dispatch` | Enables manual triggering via the **"Run workflow"** button |
| `runs-on: ubuntu-latest` | Specifies the runner OS (GitHub-hosted) |
| `actions/checkout@v4` | Clones the repository onto the runner |
| `run` | Executes shell commands directly |

#### Step 3 — Run the Workflow

1. Push the file to your repository's `main` branch.
2. Go to the **Actions** tab in your GitHub repository.
3. Select **"Simple Workflow"** from the left sidebar.
4. Click **"Run workflow"** → select the `main` branch → click **"Run workflow"**.
5. Click into the run and expand the **build** job to see the output of each step.

---

### Lab 2: Release & Notify on Microsoft Teams

**Goal:** Automatically deploy and notify stakeholders via Microsoft Teams when a GitHub Release is published.

#### Step 1 — Set Up Microsoft Teams Webhook

1. In Microsoft Teams, go to the channel where you want notifications.
2. Click the **"…"** (More options) → **Connectors** (or **Workflows** depending on your Teams version).
3. Search for **"Incoming Webhook"** → **Configure**.
4. Name it (e.g., "GitHub Releases") and copy the **Webhook URL**.

#### Step 2 — Add the Secret to GitHub

1. Go to your repository → **Settings** → **Secrets and variables** → **Actions**.
2. Click **New repository secret**:
   - **Name:** `TEAMS_WEBHOOK_URL`
   - **Value:** Paste the webhook URL from Step 1.

#### Step 3 — Create the Workflow File

Create `.github/workflows/Release and notify on teams.yml`:

```yaml
name: Deploy and Release

on:
  release:
    types: [published]

permissions:
  contents: write
  pull-requests: read

jobs:
  release-process:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Deploy to Production
        run: |
          echo "Deploying new version..."
          # Your deployment logic here

      - name: Generate Release Notes
        id: release_notes
        uses: softprops/action-gh-release@v2
        with:
          generate_release_notes: true
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Notify Stakeholders via Teams
        run: |
          curl -H 'Content-Type: application/json' \
          -d '{
                "type": "MessageCard",
                "context": "http://schema.org/extensions",
                "themeColor": "0076D7",
                "summary": "New Release Deployed",
                "sections": [{
                    "activityTitle": "New Release: ${{ github.event.release.tag_name }}",
                    "activitySubtitle": "Status: Deployed to Production",
                    "facts": [
                        { "name": "Repository:", "value": "${{ github.repository }}" },
                        { "name": "Author:", "value": "${{ github.actor }}" }
                    ],
                    "markdown": true
                }],
                "potentialAction": [{
                    "@type": "OpenUri",
                    "name": "View Release Notes",
                    "targets": [{ "os": "default", "uri": "${{ github.event.release.html_url }}" }]
                }]
              }' \
          ${{ secrets.TEAMS_WEBHOOK_URL }}
```

#### Step 4 — Key Concepts

| Concept | Explanation |
|---|---|
| `on: release: types: [published]` | Triggers when a GitHub Release is published |
| `permissions` | Grants the `GITHUB_TOKEN` write access to contents |
| `fetch-depth: 0` | Clones **full history** (needed for release note generation) |
| `softprops/action-gh-release@v2` | Auto-generates release notes from PRs and commits |
| `secrets.GITHUB_TOKEN` | Automatically provided by GitHub — no setup needed |
| `secrets.TEAMS_WEBHOOK_URL` | Your Teams incoming webhook URL (configured in Step 2) |

#### Step 5 — Trigger the Workflow

1. Go to your repository → **Releases** (right sidebar or Code tab).
2. Click **"Draft a new release"**.
3. Create a new tag (e.g., `v1.0.0`), add a title and description.
4. Click **"Publish release"**.
5. The workflow triggers automatically — check the **Actions** tab.
6. After completion, check your Microsoft Teams channel for the notification card.

---
### Lab 3: Python Application Code (src & tests)

**Goal:** Set up the Python application and test files that multiple workflows depend on.

#### Step 1 — Create the Requirements File

Create `requirements.txt` in the repository root:

```
# --- Testing Framework ---
pytest==8.0.0
pytest-cov==4.1.0

# --- Dependencies ---
# (Our calculator uses standard libraries, so no extra packages are needed yet.
# But if you used 'requests' or 'pandas', you would list them here.)
```

#### Step 2 — Create the Source Module

Create `src/__init__.py` (empty file — makes `src` a Python package):

```
```

Create `src/calculator.py`:

```python
"""
A simple calculator module for basic arithmetic operations.
"""

def add(a, b):
    """Returns the sum of two numbers."""
    return a + b

def subtract(a, b):
    """Returns the difference of two numbers."""
    return a - b

def multiply(a, b):
    """Returns the product of two numbers."""
    return a * b

def divide(a, b):
    """Returns the quotient of two numbers. Raises ValueError on division by zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b
```

#### Step 3 — Create the Test Suite

Create `tests/__init__.py` (empty file):

```
```

Create `tests/test_math.py`:

```python
from src.calculator import add, subtract, multiply, divide
import pytest

def test_add():
    assert add(10, 5) == 15

def test_subtract():
    assert subtract(10, 5) == 5

def test_multiply():
    assert multiply(10, 5) == 50

def test_divide():
    assert divide(10, 5) == 2

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)
```

#### Step 4 — Verify Locally

```bash
pip install -r requirements.txt
pytest
```

You should see **5 passed** tests.

---

### Lab 4: Caching Dependencies

**Goal:** Speed up workflow runs by caching pip dependencies between runs using `actions/cache@v4`.

#### Step 1 — Create the Workflow File

Create `.github/workflows/Caching.yml`:

```yaml
name: Caching

on:
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Cache pip dependencies
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Verify Setup
        run: |
          python -c "print('Manual build successful and cache utilized.')"
```

#### Step 2 — Key Concepts

| Concept | Explanation |
|---|---|
| `actions/cache@v4` | Saves and restores a directory to speed up future runs |
| `path` | The directory to cache (`~/.cache/pip` on Ubuntu) |
| `key` | Unique cache identifier — includes a hash of `requirements.txt` |
| `restore-keys` | Fallback prefix — restores the most recent partial match |

#### Step 3 — Run & Observe

1. Push to `main` and manually trigger the workflow.
2. **First run:** You will see "Cache not found" — dependencies are downloaded and the cache is saved.
3. **Second run:** You will see "Cache restored" — pip skips downloading packages it already has.
4. Compare the **Install dependencies** step duration between runs to see the speedup.

---

### Lab 5: Reusable Workflow — Python Standard Checks

**Goal:** Create a reusable workflow (called via `workflow_call`) that runs Flake8 linting and Mypy type checking. This workflow is consumed by Lab 6.

#### Step 1 — Create the Reusable Workflow

Create `.github/workflows/python-standard-checks.yml`:

```yaml
name: Reusable Python Quality Check

on:
  workflow_call:
    inputs:
      python-version:
        required: false
        type: string
        default: "3.11"
    secrets:
      API_TOKEN:
        required: false

jobs:
  quality-gate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ inputs.python-version }}

      - name: Install Linting Tools
        run: |
          python -m pip install --upgrade pip
          pip install flake8 mypy

      - name: Run Flake8 (Linting)
        run: flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

      - name: Run Mypy (Type Checking)
        run: mypy . --ignore-missing-imports
```

#### Step 2 — Key Concepts

| Concept | Explanation |
|---|---|
| `workflow_call` | Makes this workflow callable by other workflows (not manually) |
| `inputs` | Parameters that the calling workflow can pass in |
| `secrets` | Allows the caller to optionally pass secrets |
| `flake8` | Python linter — checks for syntax errors and undefined names |
| `mypy` | Static type checker for Python |

> **Note:** This workflow cannot be triggered manually. It will be called from the **Python Package Testing** workflow in Lab 6.

---

### Lab 6: Matrix Testing — Python Package Testing

**Goal:** Use a build matrix to test across multiple Python versions and operating systems, and call the reusable workflow from Lab 5 as a prerequisite.

#### Step 1 — Create the Workflow File

Create `.github/workflows/Python Package Testing.yml`:

```yaml
name: Python Package Testing

on:
  workflow_dispatch:
    inputs:
      log_level:
        description: 'Logging Level'
        default: 'INFO'
        type: choice
        options: [INFO, DEBUG]

jobs:
  static-analysis:
    uses: waelkdouh/GitHub---Actions-Training/.github/workflows/python-standard-checks.yml@main
    with:
      python-version: "3.11"

  test:
    needs: static-analysis
    name: Test on ${{ matrix.os }} with Python ${{ matrix.python-version }}
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest]
        python-version: ['3.9', '3.10', '3.11']

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
          pip install pytest pytest-github-actions-annotate-failures

      - name: Run tests
        run: |
          pytest --log-level=${{ github.event.inputs.log_level }}
```

> **Important:** Replace `waelkdouh/GitHub---Actions-Training` in the `uses:` field with your own `<owner>/<repo>` if you forked this repository.

#### Step 2 — Key Concepts

| Concept | Explanation |
|---|---|
| `workflow_dispatch` with `inputs` | Manual trigger with a dropdown choice for log level |
| `uses: ...workflow_call` | Calls the reusable workflow from Lab 5 |
| `needs: static-analysis` | Tests only run after linting passes |
| `strategy.matrix` | Creates **6 jobs** (2 OS × 3 Python versions) |
| `fail-fast: false` | All matrix jobs run even if one fails |

#### Step 3 — Run & Observe

1. Push all files to `main`.
2. Go to **Actions** → **Python Package Testing** → **Run workflow**.
3. Select a **Logging Level** (`INFO` or `DEBUG`) and run.
4. Observe that the **static-analysis** job runs first, then **6 parallel test jobs** start.

---

### Lab 7: Composite Action — Python Environment Setup

**Goal:** Create a **Composite Action** that bundles Python setup, caching, and dependency installation into a single reusable step.

#### Step 1 — Create the Action Definition

Create `.github/actions/python-setup/action.yml`:

```yaml
name: 'Python Environment Setup'
description: 'Sets up Python, restores cache, and installs requirements'
inputs:
  python-version:
    description: 'Python version to use'
    required: true
    default: '3.11'
  requirements-path:
    description: 'Path to requirements.txt'
    required: false
    default: 'requirements.txt'

runs:
  using: "composite"
  steps:
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: ${{ inputs.python-version }}
        cache: 'pip'

    - name: Install Dependencies
      shell: bash
      run: |
        python -m pip install --upgrade pip
        if [ -f ${{ inputs.requirements-path }} ]; then
          pip install -r ${{ inputs.requirements-path }}
        fi

    - name: Verify Installation
      shell: bash
      run: python --version
```

#### Step 2 — Create the Consuming Workflow

Create `.github/workflows/ConsumeCompositeAction.yml`:

```yaml
name: Consume Composite Action
on:
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Initialize Python Environment
        uses: ./.github/actions/python-setup
        with:
          python-version: '3.10'

      - name: Run Tests
        run: pytest
```

#### Step 3 — Key Concepts

| Concept | Explanation |
|---|---|
| `using: "composite"` | Defines a Composite Action — bundles multiple steps into one |
| `shell: bash` | **Required** for every `run` step in composite actions |
| `uses: ./.github/actions/python-setup` | References a local action by path |
| Composite vs. Reusable Workflow | Composite actions run **inside the caller's job**; reusable workflows run as **separate jobs** |

#### Step 4 — Run & Observe

1. Push to `main`.
2. Go to **Actions** → **Consume Composite Action** → **Run workflow**.
3. Expand the **Initialize Python Environment** step — you will see the sub-steps (setup, install, verify) running inline.
4. The **Run Tests** step executes `pytest` against `tests/test_math.py`.

---

### Lab 8: Docker Action — Hello Docker

**Goal:** Create a custom **Docker Container Action** that greets a user and returns an output.

#### Step 1 — Create the Entrypoint Script

Create `.github/actions/DockerAction/entrypoint.sh`:

```bash
#!/bin/sh -l

# $1 is the first argument passed from the 'args' section in action.yml
NAME=$1

echo "Hello $NAME"

# Setting an output for GitHub Actions
echo "greeting=Hello $NAME" >> $GITHUB_OUTPUT
```

#### Step 2 — Create the Dockerfile

Create `.github/actions/DockerAction/Dockerfile`:

```dockerfile
# Use a lightweight base image
FROM alpine:3.10

# Copy the shell script from your repo to the container
COPY entrypoint.sh /entrypoint.sh

# Make the script executable
RUN chmod +x /entrypoint.sh

# Code to run when the container starts
ENTRYPOINT ["/entrypoint.sh"]
```

#### Step 3 — Create the Action Metadata

Create `.github/actions/DockerAction/action.yml`:

```yaml
name: 'Hello Docker Action'
description: 'Greet someone'
author: 'octocat@github.com'

inputs:
  my_name:
    description: 'Who to greet'
    required: true
    default: 'World'

outputs:
  greeting:
    description: 'Full greeting'

runs:
  using: 'docker'
  image: 'Dockerfile'
  args:
    - ${{ inputs.my_name }}

branding:
  icon: 'mic'
  color: 'purple'
```

#### Step 4 — Create the Consuming Workflow

Create `.github/workflows/ConsumeDockerAction.yml`:

```yaml
name: Consume Docker Action

on:
  workflow_dispatch:
    inputs:
      name_to_greet:
        description: 'Who should the action greet?'
        required: true
        default: 'Wael'
        type: string

jobs:
  hello_world_job:
    runs-on: ubuntu-latest
    name: A job to say hello
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Hello world action step
        id: hello
        uses: ./.github/actions/DockerAction
        with:
          my_name: ${{ inputs.name_to_greet }}

      - name: Get the output
        run: echo "The greeting was ${{ steps.hello.outputs.greeting }}"
```

#### Step 5 — Key Concepts

| Concept | Explanation |
|---|---|
| `using: 'docker'` | Tells GitHub to build and run a Docker container |
| `image: 'Dockerfile'` | Points to the Dockerfile in the same directory |
| `args` | Arguments passed to the container's `ENTRYPOINT` |
| `$GITHUB_OUTPUT` | The mechanism to set step outputs from within a container |
| Docker actions | Always run on **Linux runners only** |

#### Step 6 — Run & Observe

1. Push all files to `main`.
2. Go to **Actions** → **Consume Docker Action** → **Run workflow**.
3. Enter a name (or leave the default "Wael") and click **Run workflow**.
4. Expand the job — observe the Docker image being **built**, the greeting printed, and the output captured.

---

### Lab 9: JavaScript Action — Hello JS

**Goal:** Create a custom **JavaScript Action** using the `@actions/core` package, bundle it with `@vercel/ncc`, and consume it from a workflow.

#### Step 1 — Initialize the Project Locally

Open a terminal, navigate to `.github/actions/JavaScriptAction/`, and run:

```bash
cd .github/actions/JavaScriptAction
npm init -y
```

#### Step 2 — Install Dependencies

```bash
npm install @actions/core
npm install --save-dev @vercel/ncc
```

#### Step 3 — Create the Action Source Code

Create `.github/actions/JavaScriptAction/index.js`:

```javascript
const core = require('@actions/core');

try {
  // 1. Get the input defined in action.yml
  const nameToGreet = core.getInput('my_name');

  console.log(`Hello ${nameToGreet}!`);

  // 2. Set the output defined in action.yml
  const greeting = `Hello ${nameToGreet}`;
  core.setOutput("greeting", greeting);

} catch (error) {
  // 3. Handle errors and fail the step if necessary
  core.setFailed(error.message);
}
```

#### Step 4 — Update package.json

Ensure your `package.json` has the build script:

```json
{
  "name": "javascriptaction",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "build": "ncc build index.js -o dist"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "type": "commonjs",
  "dependencies": {
    "@actions/core": "^2.0.3"
  },
  "devDependencies": {
    "@vercel/ncc": "^0.38.4"
  }
}
```

#### Step 5 — Bundle the Action

Run the build command to create the single-file bundle in `dist/`:

```bash
npm run build
```

This creates `dist/index.js` — a single file containing your code and all dependencies. **This file must be committed to the repository.**

#### Step 6 — Create the Action Metadata

Create `.github/actions/JavaScriptAction/action.yml`:

```yaml
name: 'Hello JS Action'
description: 'Greet someone using JavaScript'
author: 'octocat@github.com'

inputs:
  my_name:
    description: 'Who to greet'
    required: true
    default: 'World'

outputs:
  greeting:
    description: 'Full greeting'

runs:
  using: 'node20'
  main: 'dist/index.js'

branding:
  icon: 'mic'
  color: 'purple'
```

#### Step 7 — Update .gitignore

Ensure `node_modules/` is in your `.gitignore` (it should already be there):

```
node_modules/
```

> **Important:** Do NOT add `dist/` to `.gitignore`. The bundled `dist/index.js` must be committed because GitHub Actions runs it directly.

#### Step 8 — Create the Consuming Workflow

Create `.github/workflows/ConsumeJavaScriptAction.yml`:

```yaml
name: Consume JavaScript Action

on:
  workflow_dispatch:
    inputs:
      name_to_greet:
        description: 'Who should the action greet?'
        required: true
        default: 'Wael'
        type: string

jobs:
  hello_world_job:
    runs-on: ubuntu-latest
    name: A job to say hello
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Hello world JS action step
        id: hello
        uses: ./.github/actions/JavaScriptAction
        with:
          my_name: ${{ inputs.name_to_greet }}

      - name: Get the output
        run: echo "The greeting was ${{ steps.hello.outputs.greeting }}"
```

#### Step 9 — Commit & Push

From the repository root:

```bash
git add .github/actions/JavaScriptAction/
git add .github/workflows/ConsumeJavaScriptAction.yml
git commit -m "Add JavaScript Action and consuming workflow"
git push
```

#### Step 10 — Key Concepts

| Concept | Explanation |
|---|---|
| `using: 'node20'` | Runs the action with Node.js 20 |
| `@actions/core` | Official GitHub Actions toolkit for inputs/outputs/logging |
| `@vercel/ncc` | Compiles Node.js modules into a single file (no `node_modules` needed at runtime) |
| `main: 'dist/index.js'` | Points to the bundled file, not the source |
| `core.getInput()` | Reads inputs defined in `action.yml` |
| `core.setOutput()` | Sets outputs consumable by subsequent steps |
| `core.setFailed()` | Marks the step as failed with an error message |

#### Step 11 — Run & Observe

1. Go to **Actions** → **Consume JavaScript Action** → **Run workflow**.
2. Enter a name and click **Run workflow**.
3. Expand the job — observe the greeting printed and the output captured (no Docker build step, so it runs faster than the Docker action).

---

### Lab 10: Environments & Deployment to Azure

**Goal:** Set up GitHub Environments with an approval gate and deploy a Python app to Azure App Service (staging → production).

#### Step 1 — Create Azure App Services

You need **two** Azure App Services. Run the following Azure CLI commands:

```bash
# Login to Azure
az login

# Set variables
RESOURCE_GROUP="GitHubActionsTraining-rg"
LOCATION="eastus"
STAGING_APP="GithubActionsWS"
PRODUCTION_APP="GithubActionsWS-Prod"
APP_SERVICE_PLAN="GitHubActionsTraining-plan"

# Create a Resource Group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create an App Service Plan (Linux, Free tier)
az appservice plan create \
  --name $APP_SERVICE_PLAN \
  --resource-group $RESOURCE_GROUP \
  --sku F1 \
  --is-linux

# Create the Staging Web App (Python 3.11)
az webapp create \
  --name $STAGING_APP \
  --resource-group $RESOURCE_GROUP \
  --plan $APP_SERVICE_PLAN \
  --runtime "PYTHON:3.11"

# Create the Production Web App (Python 3.11)
az webapp create \
  --name $PRODUCTION_APP \
  --resource-group $RESOURCE_GROUP \
  --plan $APP_SERVICE_PLAN \
  --runtime "PYTHON:3.11"
```

> **Note:** App names must be globally unique. If names are taken, choose different names and update the workflow accordingly.

#### Step 2 — Download Publish Profiles

1. Go to the [Azure Portal](https://portal.azure.com).
2. Navigate to each App Service (`GithubActionsWS` and `GithubActionsWS-Prod`).
3. Click **Download publish profile** from the Overview page.
4. Save the `.PublishSettings` XML file content — you will need it in the next step.

#### Step 3 — Configure GitHub Environments

1. Go to your GitHub repository → **Settings** → **Environments**.

**Create the Staging Environment:**

2. Click **New environment** → name it `staging` → click **Configure environment**.
3. Click **Add environment secret**:
   - **Name:** `AZURE_WEBAPP_PUBLISH_PROFILE`
   - **Value:** Paste the **entire contents** of the staging app's `.PublishSettings` file.

**Create the Production Environment:**

4. Go back to **Environments** → **New environment** → name it `production` → click **Configure environment**.
5. Click **Add environment secret**:
   - **Name:** `AZURE_WEBAPP_PUBLISH_PROFILE`
   - **Value:** Paste the **entire contents** of the production app's `.PublishSettings` file.
6. Under **Environment protection rules**, check **Required reviewers** and add yourself (or a teammate) as a reviewer. Click **Save protection rules**.

#### Step 4 — Create the Workflow File

Create `.github/workflows/environments.yml`:

```yaml
name: Python Deployment Pipeline

on:
  pull_request:
    branches: [ "main" ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.14'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://GithubActionsWS.azurewebsites.net

    steps:
      - uses: actions/checkout@v4

      - name: 'Deploy to Azure Web App (Staging)'
        uses: azure/webapps-deploy@v2
        with:
          app-name: 'GithubActionsWS'
          publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
          package: .

  deploy-production:
    needs: deploy-staging
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://GithubActionsWS-Prod.azurewebsites.net

    steps:
      - uses: actions/checkout@v4

      - name: 'Deploy to Azure Web App (Production)'
        uses: azure/webapps-deploy@v2
        with:
          app-name: 'GithubActionsWS-Prod'
          publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
          package: .
```

> **Important:** Update `app-name` and `url` values if you chose different Azure App Service names.

#### Step 5 — Key Concepts

| Concept | Explanation |
|---|---|
| `environment: name:` | Links the job to a GitHub Environment and its secrets |
| `environment: url:` | Displays a clickable deployment URL in the Actions UI |
| `needs:` | Creates job dependencies (build → staging → production) |
| `if: github.ref == 'refs/heads/main'` | Production only deploys when merging to main |
| Required reviewers | Manual approval gate before production deployment |
| Publish Profile | XML credential file downloaded from Azure App Service |

#### Step 6 — Trigger the Workflow

This workflow triggers on **pull requests** to `main`:

1. Create a new branch:
   ```bash
   git checkout -b feature/test-deploy
   ```
2. Make a small change (e.g., edit `README.md`) and push:
   ```bash
   git add .
   git commit -m "Test deployment pipeline"
   git push origin feature/test-deploy
   ```
3. Open a **Pull Request** from `feature/test-deploy` → `main`.
4. The workflow starts automatically. Observe:
   - **build** runs first.
   - **deploy-staging** deploys to the staging App Service.
   - **deploy-production** waits for your **manual approval** (check your GitHub notifications or the Actions UI).

---

### Lab 11: Efficiency — Concurrency, Timeouts & Inputs

**Goal:** Learn workflow efficiency techniques: concurrency groups (prevent duplicate runs), job and step-level timeouts, and manual inputs.

#### Step 1 — Create the Workflow File

Create `.github/workflows/Efficiency.yml`:

```yaml
name: Efficiency

on:
  workflow_dispatch:
    inputs:
      reason:
        description: 'Why are you running this?'
        required: false
        default: 'Manual health check'

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run Manual Task
        timeout-minutes: 5
        run: |
          echo "Running for reason: ${{ github.event.inputs.reason }}"
          npm install
          npm test
```

#### Step 2 — Key Concepts

| Concept | Explanation |
|---|---|
| `concurrency.group` | Logical grouping — only one run per group at a time |
| `cancel-in-progress: true` | Cancels any existing run when a new one starts in the same group |
| `timeout-minutes: 15` (job-level) | Kills the entire job if it runs longer than 15 minutes |
| `timeout-minutes: 5` (step-level) | Kills this specific step if it exceeds 5 minutes |
| `inputs.reason` | Custom free-text input displayed in the "Run workflow" dialog |

#### Step 3 — Run & Observe

1. Push to `main`.
2. Go to **Actions** → **Efficiency** → **Run workflow**.
3. Enter a reason and click **Run workflow**.
4. **While the first run is in progress**, click **Run workflow** again — observe the first run gets **cancelled** (concurrency in action).

---


