### Welcome to the Contributing Guide for the `cambd` project!

We are happy to accept contributions from anyone, whether you are a first-time contributor or a seasoned veteran.
This guide is designed to help you get started contributing to the project.

> [!NOTE]
> We are not accepting PRs for granular changes like typos in README file or updating any text content. PRs have to be fixing some sort of issues or adding a new feature.

### Local Development

```bash
# 1. Fork the repository on GitHub and clone your fork locally.
git clone https://github.com/rocktimsaikia/cambd.git

# 2. Create a branch for local development.
git checkout -b name-of-your-bugfix-or-feature

# 3. Create a virtual environment.
python -m venv cambd-venv

# 4. Activate the virtual environment.
# On Windows, run:
cambd-venv\Scripts\activate

# On Unix or MacOS, run:
source cambd-venv/bin/activate

# 5. Install the dependencies.
pip install -r requirements.txt

# 6. Make your changes.

# 7. Locally run cambd and verify your changes.
python -m cambd <args>

# 8. Add and commit your changes.
git add -A
git commit -m "Your detailed description of your changes."

# 9. Push your local branch to the remote repository on GitHub.
git push -u origin HEAD
```

### Pull Request Guidelines

Before you submit a pull request from your forked repository, check that it meets these guidelines:

1. Pull request title should be descriptive and written in imperative mood.
2. Pull request description should be detailed and include the motivation for the change.
3. Don't forget to [link](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue) the issue that you are fixing.
4. Wait for the pull request to be reviewed by a maintainer.

### Your PR got merged :tada:

Once your pull request is merged, pull the changes from the main (upstream) repository:

```bash
# 1. Switch to the main branch.
git checkout main

# 2. Update your main branch with the latest upstream version.
git pull upstream main
```
