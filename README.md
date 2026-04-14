# GitHub Actions Training Labs - test environment workflow

Welcome to the **GitHub Actions Training** workshop! This guide contains **eight hands-on labs** that will walk you through creating, running, and understanding GitHub Actions workflows — from the simplest "Hello World" to advanced topics like self-hosted runners, pipeline migration, and AI-powered agentic workflows.

> **Audience:** Beginners. No prior GitHub Actions experience is required.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Repository Structure](#repository-structure)
- [Lab 1 – Simple Workflow](#lab-1--simple-workflow)
- [Lab 2 – Release and Notify on Teams](#lab-2--release-and-notify-on-teams)
- [Lab 3 – Python Quality Checks and Package Testing](#lab-3--python-quality-checks-and-package-testing)
- [Lab 4 – Environments](#lab-4--environments)
- [Lab 5 – Caching, Composite Actions, and Efficiency](#lab-5--caching-composite-actions-and-efficiency)
- [Lab 6 – JavaScript and Docker Custom Actions](#lab-6--javascript-and-docker-custom-actions)
- [Lab 7 – Azure DevOps Pipeline Migration and Self-Hosted Runner](#lab-7--azure-devops-pipeline-migration-and-self-hosted-runner)
- [Lab 8 – Agentic Workflows (Daily Repo Status)](#lab-8--agentic-workflows-daily-repo-status)

---

## Prerequisites

Before starting the labs, make sure you have the following tools installed and configured on your machine.

### 1. GitHub Account

- Create a free account at <https://github.com> if you don't already have one.

### 2. Git

- Download and install Git from <https://git-scm.com/downloads>.
- After installation, open a terminal and verify:

  ```bash
  git --version
  ```

### 3. Visual Studio Code (VS Code)

- Download from <https://code.visualstudio.com>.
- Recommended extensions:
  - **GitHub Actions** (by GitHub) – provides syntax highlighting for workflow files.

### 4. GitHub CLI (`gh`)

- Download from <https://cli.github.com>.
- Authenticate after installation:

  ```bash
  gh auth login
  ```

  Follow the prompts and choose **HTTPS** and **Login with a web browser**.

### 5. Python 3.9+ (for Labs 3–5)

- Download from <https://www.python.org/downloads/>.
- During installation on Windows, **check "Add Python to PATH"**.
- Verify:

  ```bash
  python --version
  pip --version
  ```

### 6. Node.js 20+ (for Lab 6 – JavaScript Action)

- Download from <https://nodejs.org> (LTS version recommended).
- Verify:

  ```bash
  node --version
  npm --version
  ```

### 7. Docker Desktop (for Labs 6 and 7)

- Download from <https://www.docker.com/products/docker-desktop/>.
- Install and start Docker Desktop.
- Verify it's running:

  ```bash
  docker --version
  ```

- **Important:** Docker Desktop must be **running** before starting Labs 6 (Docker Action) and 7 (GitHub Actions Importer).

### 8. Create Your Own Repository (Starter Code Only)

> **Do NOT fork** the training repository — it already contains the completed solutions for every lab. Instead, you will create a **fresh repository** and copy only the starter source code into it.

1. Go to <https://github.com/new> and create a new repository:
   - **Repository name:** `GitHub---Actions-Training` (or any name you like)
   - **Visibility:** Public (required for some GitHub Actions features on free plans)
   - Check **Add a README file**
   - Click **Create repository**

2. Clone your new empty repository locally:

   ```bash
   git clone https://github.com/<YOUR-USERNAME>/GitHub---Actions-Training.git
   cd GitHub---Actions-Training
   ```

3. Create the starter project files. These are the only files you need before starting the labs:

   **Create the folder structure:**

   ```bash
   mkdir -p src tests azdo
   ```

   **Create `requirements.txt`:**

   ```
   # --- Testing Framework ---
   pytest==8.0.0
   pytest-cov==4.1.0
   ```

   **Create `src/__init__.py`:** (empty file)

   ```bash
   touch src/__init__.py
   ```

   **Create `src/calculator.py`:**

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

   **Create `tests/__init__.py`:** (empty file)

   ```bash
   touch tests/__init__.py
   ```

   **Create `tests/test_math.py`:**

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

   **Create `azdo/azure-pipelines.yml`** (used in Lab 7):

   ```yaml
   trigger:
   - main

   pool:
     vmImage: 'ubuntu-latest'

   variables:
     buildConfiguration: 'Release'
     deploymentEnv: 'Staging'

   stages:
   - stage: Build
     displayName: 'Build and Unit Test'
     jobs:
     - job: BuildJob
       displayName: 'Compile Source'
       steps:
       - script: echo "Restoring dependencies..."
         displayName: 'Restore'
       
       - script: echo "Running build in $(buildConfiguration) mode..."
         displayName: 'Build'

       - task: PublishBuildArtifacts@1
         inputs:
           PathtoPublish: '$(Build.ArtifactStagingDirectory)'
           ArtifactName: 'drop'
           publishLocation: 'Container'

   - stage: Test
     displayName: 'Integration Tests'
     dependsOn: Build
     jobs:
     - job: RunTests
       steps:
       - script: echo "Running integration tests for $(deploymentEnv)..."
         displayName: 'Test Step'

   - stage: Deploy
     displayName: 'Deploy to Staging'
     dependsOn: Test
     condition: succeeded()
     jobs:
     - deployment: DeployWeb
       environment: 'Staging'
       strategy:
         runOnce:
           deploy:
             steps:
             - script: echo "Deploying to Azure App Service..."
   ```

4. Commit and push all starter files:

   ```bash
   git add .
   git commit -m "Add starter source code for GitHub Actions training"
   git push
   ```

5. Open the folder in VS Code:

   ```bash
   code .
   ```

> **Your repository should now contain ONLY:** `README.md`, `requirements.txt`, `src/`, `tests/`, and `azdo/`. The `.github/workflows/` and `.github/actions/` folders will be created as you complete each lab.

---

## Repository Structure

```
GitHub---Actions-Training/
├── README.md                          # This lab guide
├── requirements.txt                   # Python dependencies (pytest, pytest-cov)
├── azdo/
│   └── azure-pipelines.yml            # Azure DevOps pipeline (used in Lab 7)
├── src/
│   ├── __init__.py
│   └── calculator.py                  # Simple calculator module
├── tests/
│   ├── __init__.py
│   └── test_math.py                   # pytest test suite
└── .github/
    ├── actions/
    │   ├── python-setup/
    │   │   └── action.yml             # Composite action (Lab 5)
    │   ├── JavaScriptAction/
    │   │   ├── action.yml             # JS action metadata (Lab 6)
    │   │   ├── index.js               # JS action source
    │   │   ├── package.json
    │   │   └── dist/index.js          # Bundled JS action
    │   └── DockerAction/
    │       ├── action.yml             # Docker action metadata (Lab 6)
    │       ├── Dockerfile
    │       └── entrypoint.sh          # Docker action script
    └── workflows/
        ├── SimpleWorkflow.yml              # Lab 1
        ├── Release and notify on teams.yml # Lab 2
        ├── python-standard-checks.yml      # Lab 3 (reusable workflow)
        ├── Python Package Testing.yml      # Lab 3 (caller workflow)
        ├── environments.yml                # Lab 4
        ├── Caching.yml                     # Lab 5
        ├── ConsumeCompositeAction.yml      # Lab 5
        ├── Efficiency.yml                  # Lab 5
        ├── ConsumeJavaScriptAction.yml     # Lab 6
        ├── ConsumeDockerAction.yml         # Lab 6
        ├── SelfHostedRunner.yml            # Lab 7
        ├── daily-repo-status.md            # Lab 8 (agentic workflow source)
        └── daily-repo-status.lock.yml      # Lab 8 (compiled agentic workflow)
```

---

## Lab 1 – Simple Workflow

**Goal:** Create your first GitHub Actions workflow and trigger it manually.

### Concepts Covered

- Workflow YAML syntax (`name`, `on`, `jobs`, `steps`)
- `workflow_dispatch` (manual trigger)
- `runs-on` (GitHub-hosted runner)
- `actions/checkout` (checking out code)
- Single-line and multi-line `run` commands

### Step 1 — Create the Workflow File

1. In your repository, create the folder `.github/workflows/` if it doesn't exist.
2. Inside that folder, create a file named **`SimpleWorkflow.yml`**.
3. Paste the following content:

   ```yaml
   # This is a basic workflow to help you get started with Actions.

   name: Simple Workflow
   run-name: Simple Workflow run by ${{ github.actor }}

   # Controls when the workflow will run
   on:
     # Allows you to run this workflow manually from the Actions tab
     workflow_dispatch:

   # A workflow run is made up of one or more jobs that can run sequentially or in parallel
   jobs:
     # This workflow contains a single job called "build"
     build:
       # The type of runner that the job will run on
       runs-on: ubuntu-latest

       # Steps represent a sequence of tasks that will be executed as part of the job
       steps:
         # Checks-out your repository under $GITHUB_WORKSPACE, so your job can access it
         - uses: actions/checkout@v4

         # Runs a single command using the runners shell
         - name: Run a one-line script
           run: echo Hello, world!

         # Runs a set of commands using the runners shell
         - name: Run a multi-line script
           run: |
             echo Add other actions to build,
             echo test, and deploy your project.
   ```

4. Commit and push your changes:

   ```bash
   git add .github/workflows/SimpleWorkflow.yml
   git commit -m "Add Simple Workflow"
   git push
   ```

### Step 2 — Run the Workflow

1. Go to your repository on GitHub.
2. Click the **Actions** tab.
3. In the left sidebar, click **Simple Workflow**.
4. Click the **Run workflow** button (dropdown) → select the `main` branch → click the green **Run workflow** button.

### Step 3 — View the Results

1. Click on the run that just appeared.
2. Click on the **build** job.
3. Expand each step to see the output:
   - **Run a one-line script** should print `Hello, world!`
   - **Run a multi-line script** should print two lines.

### What You Learned

- A workflow file lives inside `.github/workflows/`.
- `workflow_dispatch` lets you trigger a workflow manually from the GitHub UI.
- `runs-on: ubuntu-latest` tells GitHub to use a free Linux virtual machine.
- `actions/checkout@v4` copies your code into the runner.

---

## Lab 2 – Release and Notify on Teams

**Goal:** Create a workflow that runs when a GitHub Release is published, generates release notes, and sends a notification to a Microsoft Teams channel.

### Concepts Covered

- `on: release` trigger
- GitHub permissions (`contents: write`, `pull-requests: read`)
- Third-party actions (`softprops/action-gh-release`)
- GitHub Secrets
- Microsoft Teams incoming webhooks

### Prerequisites — Set Up a Teams Incoming Webhook

> If you don't have a Microsoft Teams channel available, you can still create the workflow and test the release step; the Teams notification step will simply fail gracefully.

1. In Microsoft Teams, go to the channel where you want notifications.
2. Click the **⋯ (three dots)** next to the channel name → **Connectors** (or **Manage channel** → **Connectors**).
3. Search for **Incoming Webhook** → click **Configure**.
4. Give it a name (e.g., `GitHub Releases`) and click **Create**.
5. **Copy the webhook URL.** You will need it in the next step.

### Prerequisites — Create the `TEAMS_WEBHOOK_URL` Secret

1. Go to your repository on GitHub.
2. Click **Settings** → **Secrets and variables** → **Actions**.
3. Click **New repository secret**.
4. Name: `TEAMS_WEBHOOK_URL`
5. Value: Paste the webhook URL you copied above.
6. Click **Add secret**.

### Step 1 — Create the Workflow File

1. Create a file `.github/workflows/Release and notify on teams.yml`.
2. Paste the following content:

   ```yaml
   name: Deploy and Release

   on:
     release:
       types: [published]

   permissions:
     contents: write    # Required to create/update releases and generate notes
     pull-requests: read # Helpful for the auto-generation of notes

   jobs:
     release-process:
       runs-on: ubuntu-latest
       steps:
         - name: Checkout Code
           uses: actions/checkout@v4
           with:
             fetch-depth: 0

         # 1. DEPLOYMENT STEP
         - name: Deploy to Production
           run: |
             echo "Deploying new version..."
             # Your deployment logic here
             
         # 2. GENERATE RELEASE NOTES
         - name: Generate Release Notes
           id: release_notes
           uses: softprops/action-gh-release@v2
           with:
             generate_release_notes: true
           env:
             GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

         # 3. NOTIFY STAKEHOLDERS (Microsoft Teams via Curl)
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

3. Commit and push:

   ```bash
   git add ".github/workflows/Release and notify on teams.yml"
   git commit -m "Add Release and Notify on Teams workflow"
   git push
   ```

### Step 2 — Trigger the Workflow by Creating a Release

1. Go to your repository on GitHub.
2. Click **Releases** (right sidebar) → **Create a new release**.
3. Click **Choose a tag** → type `v1.0.0` → click **Create new tag: v1.0.0 on publish**.
4. Set the **Release title** to `v1.0.0`.
5. Optionally add a description.
6. Click **Publish release**.

### Step 3 — View the Results

1. Go to the **Actions** tab → click on the **Deploy and Release** run.
2. Expand the steps to see:
   - The deployment echo.
   - The release notes generation.
   - The Teams webhook call (check your Teams channel for the notification card).

### What You Learned

- A workflow can react to GitHub events like release publication.
- `secrets.GITHUB_TOKEN` is automatically provided by GitHub — you don't need to create it.
- Custom secrets (like `TEAMS_WEBHOOK_URL`) are stored securely in **Settings → Secrets**.
- `fetch-depth: 0` clones the full git history, which is needed for generating release notes.

---

## Lab 3 – Python Quality Checks and Package Testing

**Goal:** Create a **reusable workflow** for Python linting/type-checking and a **caller workflow** that invokes it before running a test matrix across multiple operating systems and Python versions.

### Concepts Covered

- Reusable workflows (`workflow_call`)
- Calling a reusable workflow with `uses:`
- Job dependencies (`needs:`)
- Matrix strategy (`strategy.matrix`)
- `workflow_dispatch` inputs (choice type)
- Python setup, linting (`flake8`), and type checking (`mypy`)

### Dependency Between the Two Files

> **`python-standard-checks.yml`** is a **reusable workflow** — it cannot be run directly from the Actions UI. It is designed to be **called** by other workflows.
>
> **`Python Package Testing.yml`** is the **caller workflow** — it triggers manually and first calls `python-standard-checks.yml` to run linting/type checks. Only if that passes does it proceed to run `pytest` across the test matrix.
>
> **Flow:** `Python Package Testing.yml` → calls → `python-standard-checks.yml` → on success → runs matrix tests.

### Step 1 — Create the Reusable Workflow

1. Create the file `.github/workflows/python-standard-checks.yml`.
2. Paste the following content:

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

3. Commit and push:

   ```bash
   git add .github/workflows/python-standard-checks.yml
   git commit -m "Add reusable Python quality check workflow"
   git push
   ```

### Step 2 — Create the Caller Workflow

1. Create the file `.github/workflows/Python Package Testing.yml`.
2. Paste the following content:

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
     # 1. Call the Reusable Workflow for standard linting/type checking
     # This ensures the code is clean before we waste time/money testing on Windows/macOS
     static-analysis:
       uses: <YOUR-USERNAME>/GitHub---Actions-Training/.github/workflows/python-standard-checks.yml@main
       with:
         python-version: "3.11"

     # 2. Run the Matrix Tests
     # We add 'needs: static-analysis' so tests only run if the code passes PEP 8
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
           # Force Bash so the 'if' statement works on Windows
           shell: bash
           run: |
             python -m pip install --upgrade pip
             if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
             pip install pytest pytest-github-actions-annotate-failures

         - name: Run tests
           # Added shell: bash here as well for consistency across the matrix
           shell: bash
           run: |
             pytest --log-level=${{ github.event.inputs.log_level }}
   ```

   > **Important:** Replace `<YOUR-USERNAME>` with your actual GitHub username in the `uses:` line under the `static-analysis` job. For example:
   > ```yaml
   > uses: waelkdouh/GitHub---Actions-Training/.github/workflows/python-standard-checks.yml@main
   > ```

3. Commit and push:

   ```bash
   git add ".github/workflows/Python Package Testing.yml"
   git commit -m "Add Python Package Testing workflow"
   git push
   ```

### Step 3 — Run the Workflow

1. Go to the **Actions** tab on GitHub.
2. Click **Python Package Testing** in the left sidebar.
3. Click **Run workflow** → select log level (`INFO` or `DEBUG`) → click **Run workflow**.

### Step 4 — View the Results

1. Click on the workflow run.
2. You will see two stages:
   - **static-analysis** — the reusable workflow running `flake8` and `mypy`.
   - **test** (6 jobs) — the matrix running across 2 OS × 3 Python versions = 6 combinations.
3. If static analysis fails, the test jobs will be **skipped** (because of `needs: static-analysis`).

### What You Learned

- `workflow_call` makes a workflow reusable — other workflows can call it.
- `needs:` creates a dependency between jobs — `test` waits for `static-analysis`.
- A matrix strategy lets you test on multiple OS/version combinations in parallel.
- `fail-fast: false` means all matrix jobs run even if one fails.

---

## Lab 4 – Environments

**Goal:** Create a deployment pipeline with **staging** and **production** environments, including manual approval gates and environment-specific secrets.

### Concepts Covered

- GitHub Environments
- Environment protection rules (manual approvers)
- Environment secrets
- Job dependencies and conditional execution (`if:`)
- The `environment:` keyword in jobs

### Prerequisites — Create GitHub Environments

#### Create the "staging" Environment

1. Go to your repository on GitHub.
2. Click **Settings** → **Environments** (left sidebar).
3. Click **New environment**.
4. Name: `staging` → click **Configure environment**.
5. (Optional) Add a protection rule:
   - Under **Environment protection rules**, check **Required reviewers**.
   - Add your own GitHub username as a reviewer.
   - Click **Save protection rules**.
6. Add an environment secret:
   - Scroll down to **Environment secrets** → click **Add secret**.
   - Name: `AZURE_WEBAPP_PUBLISH_PROFILE`
   - Value: Paste your Azure Web App publish profile XML (or use a placeholder like `placeholder-for-demo` if you don't have an Azure Web App).
   - Click **Add secret**.

#### Create the "production" Environment

1. Back in **Settings** → **Environments**, click **New environment**.
2. Name: `production` → click **Configure environment**.
3. Under **Environment protection rules**, check **Required reviewers**.
4. Add your own GitHub username as a reviewer → click **Save protection rules**.
5. Add the same environment secret:
   - Name: `AZURE_WEBAPP_PUBLISH_PROFILE`
   - Value: Paste the production publish profile XML (or a placeholder).
   - Click **Add secret**.

> **Note:** If you don't have an Azure Web App, you can still create the environments and secrets with placeholder values. The workflow will demonstrate the environment approval gates even if the actual deployment step fails.

### Step 1 — Create the Workflow File

1. Create the file `.github/workflows/environments.yml`.
2. Paste the following content:

   ```yaml
   name: Python Deployment Pipeline

   on:
     pull_request:
       branches: [ "main" ]

   jobs:
     # 1. Build and Test Phase
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

     # 2. Deploy to Staging (Triggered automatically on push/PR)
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

     # 3. Deploy to Production (Requires Manual Approval Gate)
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

3. Commit and push:

   ```bash
   git add .github/workflows/environments.yml
   git commit -m "Add environments workflow"
   git push
   ```

### Step 2 — Trigger the Workflow

This workflow triggers on **pull requests** to `main`. To trigger it:

1. Create a new branch:

   ```bash
   git checkout -b feature/test-environments
   ```

2. Make a small change (e.g., add a comment to `src/calculator.py`):

   ```bash
   echo "# test change" >> src/calculator.py
   ```

3. Commit and push:

   ```bash
   git add .
   git commit -m "Test environments workflow"
   git push -u origin feature/test-environments
   ```

4. Go to GitHub and create a **Pull Request** from `feature/test-environments` → `main`.

### Step 3 — View the Results

1. Go to the **Actions** tab and click on the workflow run.
2. You will see three jobs:
   - **build** — installs dependencies.
   - **deploy-staging** — deploys to the staging environment (may require your approval if you set up a reviewer).
   - **deploy-production** — deploys to production (requires manual approval).
3. If you added yourself as a reviewer, you will see a **Review deployments** button. Click it and approve to continue.

### What You Learned

- **Environments** in GitHub let you add protection rules like manual approvals.
- Each environment can have its own secrets (e.g., different publish profiles for staging vs. production).
- `needs:` chains the jobs: build → staging → production.
- `if: github.ref == 'refs/heads/main'` restricts production deployment to the main branch only.

---

## Lab 5 – Caching, Composite Actions, and Efficiency

**Goal:** Learn three techniques to make workflows faster and more efficient: dependency caching, composite actions, and concurrency/timeout controls.

### Concepts Covered

- `actions/cache` for caching dependencies
- Composite actions (custom reusable steps)
- `concurrency` (prevent duplicate runs)
- `timeout-minutes` (job and step level)
- `workflow_dispatch` with inputs

---

### Part A — Caching (`Caching.yml`)

#### Step 1 — Create the Workflow File

1. Create the file `.github/workflows/Caching.yml`.
2. Paste the following content:

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

3. Commit and push:

   ```bash
   git add .github/workflows/Caching.yml
   git commit -m "Add Caching workflow"
   git push
   ```

#### Step 2 — Run it Twice

1. Go to **Actions** → **Caching** → **Run workflow** → run it.
2. Wait for it to complete. Look at the **Cache pip dependencies** step — it should say `Cache not found`.
3. Run it **a second time**. This time, the cache step should say `Cache restored` — and the **Install dependencies** step should be noticeably faster.

#### What You Learned

- `actions/cache` saves files between workflow runs using a key.
- The key is based on a hash of `requirements.txt` — if dependencies change, the cache is rebuilt.
- `restore-keys` provides a fallback: even a partial cache hit speeds things up.

---

### Part B — Composite Action (`ConsumeCompositeAction.yml`)

A **composite action** bundles multiple steps into a single reusable action that lives inside your repository.

#### Step 1 — Create the Composite Action

1. Create the folder `.github/actions/python-setup/`.
2. Inside it, create a file named **`action.yml`**:

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

#### Step 2 — Create the Workflow That Consumes It

1. Create the file `.github/workflows/ConsumeCompositeAction.yml`.
2. Paste the following content:

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

3. Commit and push all files:

   ```bash
   git add .github/actions/python-setup/action.yml
   git add .github/workflows/ConsumeCompositeAction.yml
   git commit -m "Add composite action and consumer workflow"
   git push
   ```

#### Step 3 — Run the Workflow

1. Go to **Actions** → **Consume Composite Action** → **Run workflow**.
2. Expand the **Initialize Python Environment** step to see the composite action's sub-steps execute (Python setup, dependency install, version check).

#### What You Learned

- A composite action is defined with `runs: using: "composite"` in an `action.yml` file.
- It's referenced with a local path: `uses: ./.github/actions/python-setup`.
- It accepts `inputs` just like marketplace actions.
- Composite actions must specify `shell:` on every `run:` step.

---

### Part C — Efficiency (`Efficiency.yml`)

#### Step 1 — Create the Workflow File

1. Create the file `.github/workflows/Efficiency.yml`.
2. Paste the following content:

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

3. Commit and push:

   ```bash
   git add .github/workflows/Efficiency.yml
   git commit -m "Add Efficiency workflow"
   git push
   ```

#### Step 2 — Test Concurrency

1. Go to **Actions** → **Efficiency** → **Run workflow**.
2. **Immediately** click **Run workflow** again (while the first run is still in progress).
3. Watch the first run — it should get **cancelled** automatically. Only the second (most recent) run continues.

#### What You Learned

- `concurrency` prevents multiple runs of the same workflow from wasting resources.
- `cancel-in-progress: true` kills the older run in favor of the newest.
- `timeout-minutes` at the **job level** (15 min) and **step level** (5 min) prevent runaway processes from consuming your minutes.

---

## Lab 6 – JavaScript and Docker Custom Actions

**Goal:** Create two custom GitHub Actions — one using **JavaScript** (Node.js) and one using **Docker** — and consume them in workflows.

### Concepts Covered

- Custom JavaScript actions (`runs: using: 'node20'`)
- Custom Docker actions (`runs: using: 'docker'`)
- Action inputs and outputs
- `@actions/core` npm package
- Dockerfile-based actions
- `workflow_dispatch` inputs

---

### Part A — JavaScript Action (`ConsumeJavaScriptAction.yml`)

#### Prerequisites

- **Node.js 20+** must be installed locally to build the action (see [Prerequisites](#6-nodejs-20-for-lab-6--javascript-action)).

#### Step 1 — Create the JavaScript Action

1. Create the folder `.github/actions/JavaScriptAction/`.

2. Create **`.github/actions/JavaScriptAction/action.yml`**:

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

3. Create **`.github/actions/JavaScriptAction/index.js`**:

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

4. Create **`.github/actions/JavaScriptAction/package.json`**:

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

5. Open a terminal, install dependencies, and bundle the action:

   ```bash
   cd .github/actions/JavaScriptAction
   npm install
   npm run build
   cd ../../..
   ```

   This creates `dist/index.js` — the bundled file that GitHub Actions will execute. The `@vercel/ncc` tool compiles your `index.js` and all its `node_modules` into a single file.

   > **Why bundle?** GitHub Actions expects all code to be checked in. By bundling into `dist/index.js`, you avoid committing the entire `node_modules` folder.

#### Step 2 — Create the Workflow

1. Create **`.github/workflows/ConsumeJavaScriptAction.yml`**:

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

2. Commit and push **all** the files (including `dist/` but NOT `node_modules/`):

   ```bash
   git add .github/actions/JavaScriptAction/
   git add .github/workflows/ConsumeJavaScriptAction.yml
   git commit -m "Add JavaScript custom action and consumer workflow"
   git push
   ```

   > **Tip:** If `node_modules` gets staged, add it to `.gitignore`:
   > ```bash
   > echo ".github/actions/JavaScriptAction/node_modules/" >> .gitignore
   > ```

#### Step 3 — Run the Workflow

1. Go to **Actions** → **Consume JavaScript Action** → **Run workflow**.
2. Enter a name (or keep the default "Wael") → click **Run workflow**.
3. Open the run and check:
   - **Hello world JS action step** — should print `Hello Wael!`.
   - **Get the output** — should print `The greeting was Hello Wael`.

---

### Part B — Docker Action (`ConsumeDockerAction.yml`)

#### Prerequisites

- **Docker Desktop** must be installed and **running** locally if you want to test the action locally (see [Prerequisites](#7-docker-desktop-for-labs-6-and-7)).

> **Note:** The GitHub-hosted runner already has Docker installed, so the workflow will run on GitHub regardless of your local Docker setup.

#### Step 1 — Create the Docker Action

1. Create the folder `.github/actions/DockerAction/`.

2. Create **`.github/actions/DockerAction/action.yml`**:

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

3. Create **`.github/actions/DockerAction/Dockerfile`**:

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

4. Create **`.github/actions/DockerAction/entrypoint.sh`**:

   ```bash
   #!/bin/sh -l

   # $1 is the first argument passed from the 'args' section in action.yml
   NAME=$1

   echo "Hello $NAME"

   # Setting an output for GitHub Actions
   echo "greeting=Hello $NAME" >> $GITHUB_OUTPUT
   ```

   > **Important (Windows users):** Make sure `entrypoint.sh` uses **LF** line endings (not CRLF). In VS Code, look at the bottom-right status bar — click `CRLF` and change it to `LF` before saving.

#### Step 2 — Create the Workflow

1. Create **`.github/workflows/ConsumeDockerAction.yml`**:

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

2. Commit and push:

   ```bash
   git add .github/actions/DockerAction/
   git add .github/workflows/ConsumeDockerAction.yml
   git commit -m "Add Docker custom action and consumer workflow"
   git push
   ```

#### Step 3 — Run the Workflow

1. Go to **Actions** → **Consume Docker Action** → **Run workflow**.
2. Enter a name → click **Run workflow**.
3. Open the run and check:
   - You will see Docker build the image and run the container.
   - **Hello world action step** — should print `Hello Wael`.
   - **Get the output** — should print `The greeting was Hello Wael`.

### What You Learned

- **JavaScript actions** use `runs: using: 'node20'` and are bundled with `@vercel/ncc` into `dist/index.js`.
- **Docker actions** use `runs: using: 'docker'` and build a container from a Dockerfile at runtime.
- Both types support `inputs` and `outputs`.
- Local actions are referenced by path: `uses: ./.github/actions/<folder>`.
- Docker actions are slower (image build on each run) but give you full control over the runtime environment.

---

## Lab 7 – Azure DevOps Pipeline Migration and Self-Hosted Runner

**Goal:** Use the **GitHub Actions Importer** to migrate an Azure DevOps pipeline to GitHub Actions, and set up a **self-hosted runner** on your local machine.

### Concepts Covered

- GitHub Actions Importer CLI
- Migrating Azure DevOps pipelines
- `dry-run` vs `migrate` commands
- Self-hosted runners
- `runs-on: self-hosted`

---

### Part A — Azure DevOps Pipeline Migration (GitHub Actions Importer)

The Azure DevOps pipeline file is located at **`azdo/azure-pipelines.yml`** in this repository. It contains a three-stage pipeline (Build → Test → Deploy) that we will convert to a GitHub Actions workflow.

#### Prerequisites

1. **Docker Desktop** must be installed and **running** (see [Prerequisites](#7-docker-desktop-for-labs-6-and-7)).
   - The Actions Importer runs inside the `ghcr.io/actions-importer/cli:latest` Docker container.
   - Open Docker Desktop and make sure it says **"Docker Desktop is running"** before proceeding.

2. **GitHub CLI** must be installed and authenticated (see [Prerequisites](#4-github-cli-gh)).

3. **Install the Actions Importer CLI extension:**

   Open a terminal in VS Code and run:

   ```bash
   gh extension install github/gh-actions-importer
   ```

4. **Update the extension** (if already installed):

   ```bash
   gh actions-importer update
   ```

   This pulls the latest Docker image. It may take a few minutes.

5. **Create a `.env.local` file** in your repository root with your tokens:

   ```
   GITHUB_ACCESS_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   AZURE_DEVOPS_ACCESS_TOKEN=your-azure-devops-pat-here
   GITHUB_INSTANCE_URL=https://github.com
   AZURE_DEVOPS_INSTANCE_URL=https://dev.azure.com
   AZURE_DEVOPS_ORGANIZATION=your-org-name
   AZURE_DEVOPS_PROJECT=your-project-name
   ```

   > **How to create the GitHub Personal Access Token (Classic):**
   > 1. Go to <https://github.com/settings/tokens>.
   > 2. Click **Generate new token** → **Generate new token (classic)**.
   > 3. Give it a note (e.g., `Actions Importer`).
   > 4. Select scopes: **`repo`** and **`workflow`**.
   > 5. Click **Generate token** and copy it into the `.env.local` file.
   >
   > **How to create the Azure DevOps Personal Access Token (PAT):**
   > 1. Go to your Azure DevOps organization → click your profile icon (top-right) → **Personal Access Tokens**.
   > 2. Click **+ New Token**.
   > 3. Give it a name, set the expiration, and grant **Read** access to **Build** and **Release**.
   > 4. Click **Create** and copy the token into the `.env.local` file.

   > **Security:** Add `.env.local` to your `.gitignore` so you never commit your tokens!
   >
   > ```bash
   > echo ".env.local" >> .gitignore
   > git add .gitignore
   > git commit -m "Add .env.local to gitignore"
   > git push
   > ```

#### Step 1 — Dry Run (Test Locally)

The `dry-run` command converts the pipeline but **keeps everything local** on your machine so you can inspect it before anyone else sees it.

Open a terminal in VS Code and run:

```bash
gh actions-importer dry-run azure-devops pipeline --source-file-path ./azdo/azure-pipelines.yml --output-dir ./migration-output
```

After it completes:
1. Open the `migration-output/` folder in your file explorer.
2. You should see a converted GitHub Actions YAML file.
3. Review it to see how the Azure DevOps stages (Build → Test → Deploy) were translated into GitHub Actions jobs.

#### Step 2 — Migrate (Push to GitHub as a Pull Request)

The `migrate` command does the same conversion **and** automatically pushes it to GitHub as a Pull Request from a feature branch it creates. It reads the tokens from the `.env.local` file.

```bash
gh actions-importer migrate azure-devops pipeline --source-file-path ./azdo/azure-pipelines.yml --output-dir ./migration-output --target-url https://github.com/waelkdouh/GitHub---Actions-Training
```

> **Note:** Replace `waelkdouh` with your own GitHub username if you are working in your fork.

After running this command:
1. Go to your repository on GitHub.
2. You should see a new **Pull Request** created automatically by the importer.
3. Review the PR to see the converted GitHub Actions workflow.
4. You can merge it or close it — the goal here is to see the conversion.

#### What You Learned

- The GitHub Actions Importer converts pipelines from Azure DevOps (and other CI/CD systems) to GitHub Actions workflows.
- `dry-run` lets you preview the conversion locally before pushing anything.
- `migrate` creates a PR with the converted workflow automatically.
- The tool runs inside a Docker container (`ghcr.io/actions-importer/cli:latest`), so Docker Desktop must be running.

---

### Part B — Self-Hosted Runner

A **self-hosted runner** is a machine (your laptop, a VM, a server) that **you manage yourself** and register with GitHub to run workflows. Unlike GitHub-hosted runners, you control the software, hardware, and network.

#### Prerequisites

- A Windows machine (or Linux/macOS — adjust commands accordingly).
- Admin access to the repository (to register the runner).

#### Step 1 — Download and Configure the Runner

1. Go to your repository on GitHub.
2. Click **Settings** → **Actions** → **Runners** (left sidebar).
3. Click **New self-hosted runner**.
4. Select your operating system (e.g., **Windows** / **x64**).
5. GitHub will show you a set of commands. Follow them step by step:

   **Create a folder:**
   ```powershell
   mkdir C:\actions-runner
   cd C:\actions-runner
   ```

   **Download the runner** (copy the exact URL from GitHub — the version number changes):
   ```powershell
   Invoke-WebRequest -Uri https://github.com/actions/runner/releases/download/v2.XXX.X/actions-runner-win-x64-2.XXX.X.zip -OutFile actions-runner-win-x64.zip
   ```

   **Extract it:**
   ```powershell
   Add-Type -AssemblyName System.IO.Compression.FileSystem
   [System.IO.Compression.ZipFile]::ExtractToDirectory("$PWD\actions-runner-win-x64.zip", "$PWD")
   ```

   **Configure the runner** (copy the exact token from GitHub):
   ```powershell
   .\config.cmd --url https://github.com/<YOUR-USERNAME>/GitHub---Actions-Training --token <TOKEN-FROM-GITHUB>
   ```

   > The configuration will ask you for:
   > - **Runner group:** Press Enter for the default.
   > - **Name of runner:** Press Enter for the default (your computer name).
   > - **Labels:** Press Enter for the default.
   > - **Work folder:** Press Enter for the default (`_work`).

#### Step 2 — Start the Runner

1. Open **VS Code** and open a terminal.
2. Navigate to the runner directory:

   ```powershell
   cd C:\actions-runner
   ```

3. Start the runner:

   ```powershell
   ./run.cmd
   ```

4. You should see output like:

   ```
   √ Connected to GitHub
   
   Current runner version: '2.XXX.X'
   Listening for Jobs
   ```

   > **Keep this terminal open!** The runner will stop listening if you close it.

#### Step 3 — Create the Workflow

1. Create the file `.github/workflows/SelfHostedRunner.yml`:

   ```yaml
   name: Self Hosted Runner
   on: 
     workflow_dispatch:

   jobs:
     check-local-system:
       runs-on: self-hosted
       steps:
         - name: Who am I?
           run: whoami
         - name: Where am I?
           run: pwd
   ```

2. Commit and push:

   ```bash
   git add .github/workflows/SelfHostedRunner.yml
   git commit -m "Add Self Hosted Runner workflow"
   git push
   ```

#### Step 4 — Run the Workflow

1. Go to **Actions** → **Self Hosted Runner** → **Run workflow**.
2. Click **Run workflow**.

#### Step 5 — View the Results

1. Watch the terminal where `run.cmd` is running — you should see it pick up the job:
   ```
   Running job: check-local-system
   ```
2. On GitHub, click the workflow run and expand the steps:
   - **Who am I?** — will show your Windows username (e.g., `your-pc\your-username`).
   - **Where am I?** — will show the working directory on your local machine (e.g., `C:\actions-runner\_work\GitHub---Actions-Training\GitHub---Actions-Training`).

### What You Learned

- Self-hosted runners let you run workflows on your own hardware.
- `runs-on: self-hosted` tells GitHub to route the job to your registered runner instead of a cloud VM.
- The runner must be **actively listening** (`./run.cmd`) to pick up jobs.
- You register runners via **Settings → Actions → Runners** in your repository.
- Self-hosted runners are useful for accessing on-premises resources, using specialized hardware, or saving on GitHub Actions minutes.

---

## Lab 8 – Agentic Workflows (Daily Repo Status)

**Goal:** Use **GitHub Agentic Workflows** (`gh-aw`) to add an AI-powered workflow that automatically generates a daily repository status report and opens a GitHub Issue with insights about recent activity.

### Concepts Covered

- GitHub Agentic Workflows CLI (`gh aw`)
- Pre-built agentic workflow templates
- Fine-grained Personal Access Tokens
- Repository secrets
- Scheduled workflows (`cron`)
- AI-generated GitHub Issues

### How It Works

Agentic Workflows use a **two-file system**:

| File | Purpose |
|------|---------|
| `daily-repo-status.md` | The **source file** — a human-readable Markdown file that describes what the workflow should do, its permissions, and its behavior. You can edit this file. |
| `daily-repo-status.lock.yml` | The **compiled lock file** — automatically generated by `gh aw`. This is the actual GitHub Actions workflow that runs. **Do NOT edit this file manually.** |

The `gh aw` CLI reads the `.md` source, compiles it into a `.lock.yml` workflow, and places both files in `.github/workflows/`. When the workflow runs, it uses a coding agent (e.g., GitHub Copilot CLI) to gather repository activity and create an insightful GitHub Issue.

### Prerequisites

#### 1. Install the `gh-aw` CLI Extension

Open a terminal in VS Code and run:

```bash
gh extension install github/gh-aw
```

Verify the installation:

```bash
gh aw --version
```

#### 2. Create a Fine-Grained Personal Access Token

> **Important:** Classic Personal Access Tokens (PATs) are **not** supported for agentic workflows. You must create a **fine-grained** token.

1. Go to: <https://github.com/settings/personal-access-tokens/new>
2. Fill in the details:
   - **Token name:** `GH_COPILOT_TOKEN`
   - **Expiration:** Choose an appropriate duration (e.g., 30 days)
   - **Repository access:** Select **Only select repositories** → choose your `GitHub---Actions-Training` repository
3. Under **Permissions**, expand **Repository permissions** and set:
   - **Contents:** `Read` — to see your code and commits
   - **Issues:** `Read and write` — to create the daily status issue
   - **Pull requests:** `Read` — to see what's being merged
4. Click **Generate token**.
5. **Copy the token** — you will not be able to see it again.

#### 3. Store the Token as a Repository Secret

1. Go to your repository on GitHub.
2. Click **Settings** → **Secrets and variables** → **Actions**.
3. Click **New repository secret**.
4. Name: `COPILOT_GITHUB_TOKEN`
5. Value: Paste the fine-grained PAT you just created.
6. Click **Add secret**.

### Step 1 — Add the Agentic Workflow to Your Repository

You have two options to add the workflow. Choose **one**:

**Option A — Quick add** (uses default settings with GitHub Copilot CLI as the coding agent):

```bash
gh aw add githubnext/agentics/daily-repo-status
```

**Option B — Guided wizard** (lets you choose which coding agent to use):

```bash
gh aw add-wizard githubnext/agentics/daily-repo-status
```

The wizard will prompt you:

```
Which coding agent would you like to use?
┃ This determines which coding agent processes your workflows
┃ > GitHub Copilot CLI - Uses GitHub Copilot CLI with MCP server support [no secret]
┃   Codex - Uses OpenAI Codex CLI with MCP server support [no secret]
┃   Claude Code - Uses Claude Code with full MCP tool support and allow-listing [no secret]
┃   Google Gemini CLI - Google Gemini CLI with headless mode and LLM gateway support [no secret]
```

Select **GitHub Copilot CLI** (the default) and press Enter.

### Step 2 — Review and Merge the Pull Request

After the command completes, `gh aw` automatically creates a **Pull Request** in your repository containing two new files:

| File | Purpose |
|------|---------|
| `.github/workflows/daily-repo-status.md` | Source file (editable) |
| `.github/workflows/daily-repo-status.lock.yml` | Compiled workflow (do not edit) |

1. Go to your repository on GitHub.
2. You should see a new **Pull Request** created by `gh aw`.
3. Click on the PR and review the files:

   Open `daily-repo-status.md` to see the human-readable workflow definition:

   ```markdown
   ---
   description: |
     This workflow creates daily repo status reports. It gathers recent repository
     activity (issues, PRs, discussions, releases, code changes) and generates
     engaging GitHub issues with productivity insights, community highlights,
     and project recommendations.

   on:
     schedule: daily
     workflow_dispatch:

   permissions:
     contents: read
     issues: read
     pull-requests: read
   ---

   # Daily Repo Status

   Create an upbeat daily status report for the repo as a GitHub issue.
   ```

   The `.lock.yml` file is the full compiled GitHub Actions workflow — it contains all the steps the runner needs to execute the agentic workflow.

4. Click **Merge pull request** → **Confirm merge** to merge the files into your `main` branch.

> **Important:** The workflow files must be on the `main` branch before you can trigger the workflow. Merging the PR is what makes the workflow available in the Actions tab.

### Step 3 — Run the Workflow

Once the PR is merged, the workflow is configured to run on a **daily schedule** (`cron`), but you can also trigger it manually right away:

1. Go to the **Actions** tab on GitHub.
2. Click **Daily Repo Status** in the left sidebar.
3. Click **Run workflow** → click the green **Run workflow** button.

### Step 4 — View the Results

1. Wait for the workflow run to complete (it may take a few minutes as the AI agent gathers and analyzes repository data).
2. Once the action completes **successfully**, it will automatically create a **GitHub Issue** with the daily status report.
3. Go to the **Issues** tab on your repository.
4. You should see a new issue with:
   - A title prefixed with `[repo-status]`
   - Labels: `report`, `daily-status`
   - An AI-generated summary of recent repository activity including:
     - Recent commits and code changes
     - Open/closed issues and PRs
     - Productivity insights and highlights
     - Actionable recommendations for maintainers

### What You Learned

- **Agentic Workflows** let you define AI-powered automation using simple Markdown files.
- The `gh aw add` command pulls pre-built workflow templates from the `githubnext/agentics` catalog.
- The `.md` file is the source of truth — the `.lock.yml` is the compiled output and should never be edited by hand.
- Fine-grained PATs provide scoped, least-privilege access for the AI agent.
- The workflow can run on a schedule or be triggered manually via `workflow_dispatch`.
- The AI agent (GitHub Copilot CLI) reads your repo's issues, PRs, and code, then creates a GitHub Issue with its findings.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Workflow not appearing in Actions tab | Make sure the file is in `.github/workflows/` and has valid YAML syntax. Push the file to the default branch (`main`). |
| `workflow_dispatch` button not showing | The workflow file must already exist on the default branch. Push it to `main` first. |
| Cache not found after first run | This is expected behavior. The cache is created on the first run and restored starting from the second run. |
| Docker action fails with "exec format error" | Make sure `entrypoint.sh` has **Unix line endings (LF)**, not Windows line endings (CRLF). In VS Code, check the bottom-right status bar. |
| Self-hosted runner not picking up jobs | Make sure `./run.cmd` is running and the terminal shows "Listening for Jobs". Check **Settings → Actions → Runners** to confirm it shows as **Online**. |
| Actions Importer fails with auth error | Verify your tokens in `.env.local` are correct and not expired. Make sure Docker Desktop is running. |
| Matrix test fails on Windows with shell error | The `if [ -f ... ]` syntax is bash-specific. Add `shell: bash` to the step on Windows runners. |
| "Reusable workflow not found" error | Make sure the `uses:` path in the caller workflow matches your actual GitHub username and repository name. The reusable workflow must be pushed to the `main` branch first. |
| npm install / npm test fails in Efficiency workflow | This is expected if your repo doesn't have a `package.json` at the root. The workflow is demonstrating concurrency and timeouts — the step failure is secondary. |
| `gh aw` command not found | Run `gh extension install github/gh-aw` to install the extension. |
| Agentic workflow fails with secret error | Make sure you created the `COPILOT_GITHUB_TOKEN` repository secret with a **fine-grained** PAT (not a classic token). Verify the token has `contents: read`, `issues: read and write`, and `pull-requests: read` permissions. |
| Daily Repo Status issue not created | Check the workflow run logs in the Actions tab. The AI agent may take several minutes. Ensure the fine-grained PAT has not expired. |

---

## Quick Reference

| Lab | Workflow File(s) | Trigger | Key Concept |
|-----|-------------------|---------|-------------|
| 1 | `SimpleWorkflow.yml` | `workflow_dispatch` (manual) | Basics of workflows |
| 2 | `Release and notify on teams.yml` | `release: published` | Events, secrets, webhooks |
| 3 | `python-standard-checks.yml` + `Python Package Testing.yml` | `workflow_call` + `workflow_dispatch` | Reusable workflows, matrix |
| 4 | `environments.yml` | `pull_request` to main | Environments, approvals |
| 5 | `Caching.yml` + `ConsumeCompositeAction.yml` + `Efficiency.yml` | `workflow_dispatch` (manual) | Cache, composite actions, concurrency |
| 6 | `ConsumeJavaScriptAction.yml` + `ConsumeDockerAction.yml` | `workflow_dispatch` (manual) | Custom JS/Docker actions |
| 7 | Migration CLI + `SelfHostedRunner.yml` | CLI + `workflow_dispatch` | Migration, self-hosted runners |
| 8 | `daily-repo-status.md` + `daily-repo-status.lock.yml` | `schedule` (daily) + `workflow_dispatch` | Agentic workflows, AI agents |
