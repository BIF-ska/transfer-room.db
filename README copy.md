# sport-repo-template
## Table of contents
* [Github](#Github)
* [Environment](#Create-new-environment)
* [Branches](#Branches)
* [Pre-commit](#Pre-commit)
* [Unittest](#Unittest)

## Github
### Clone repo
#### Github Desktop
1. Click on "Add" in the top left corner
2. Click on "Clone repository"
3. Select the repository you want to clone
4. Select the location you want to clone the repository to
5. Click on "Clone"

#### Git Terminal
1. Go to the location you want to clone the repository to:
2.
```python
git clone <HTTPS or SSH>
```
![alt text](https://github.com/brondby-if/sport-repo-template/blob/main/images/Git%20clone.png "Failed pre-commit")

## Create new environment
Create new environment in Anaconda with Python 3.11:
```python
conda create -n <NAME> python=3.11
```

Activate new environment:
```python
conda activate <NAME>
```

### Poetry

Poetry is a tool for dependency management and packaging in Python. To install Poetry, run the following command in your terminal:

```bash
pip install poetry
```

#### Adding and Removing Dependencies

##### Add Dependency

When we want to install a dependency that Poetry has to manage, we write:

```bash
poetry add NameOfDependency 
```

if we wanted to install pandas we would write:
```bash
poetry add pandas 
```

##### Remove Dependency
When we want to remove a dependency from the project, we write:

```bash
poetry remove NameOfDependency 
```
if we wanted to remove pandas we would write:
```bash
poetry remove pandas 
```
#### Poetry and Conda Environments
**If you want to run a Conda environment and a pyproject.toml file exists, check the pyproject.toml for required Python Version!**

Poetry will automatically detect if a Conda environment is active and install dependencies on that environment while documenting the needed dependencies in the `pyproject.toml` file.

**Only if you dont use Anaconda!**
If an environment is not found, an environment can be created by running:
```bash
poetry shell
```
The terminal will look like:

![Terminal](https://github.com/brondby-if/sport-repo-template/blob/main/images/terminal.png)

Regardless the environment, dependencies should be added to the project as follows to document needed dependencies: 

```bash
poetry add NameOfDependency 
```

#### Installing Dependencies In Pyproject.toml
Dependencies that are located in the `pyproject.toml` file can be installed with the following command

```bash
poetry install 
```

Poetry will then install the dependencies in the environment that is active.

that way it gets added to the pyproject.toml file which holds all the relevant information

Install requirements into new environment:
```python
pip install -r requirements.txt
```
oetry is able to install private repos, marked as dependencies,
if configured with a `Github Access Token`.

### Setting up Poetry with GitHub Access Token

To install private repositories as dependencies, you need to configure Poetry with a GitHub access token. This requires a one-time setup on your development machine. Here are the steps:

1. Open your web browser and navigate to GitHub's website.

2. Once you're logged in, click on your profile picture in the top-right corner of the website.

3. From the dropdown menu, click on `Settings`.

4. In the settings sidebar, click on `Developer settings`.

5. Click on `Personal access tokens`.

6. Click on `Fine-grained Tokens`.

7. Click on `Generate new token`.

8. Give your token a descriptive name in the `Note` field.

9. Set an appropriate `Expiration` date.

10. Under `Repository Access`, select either `All Repositories` or `Only Select Repositories` as shown.
    ![Repository Access](<https://github.com/brondby-if/sport-repo-template/blob/main/images/Repository Access.png>)

11. Under `Permissions` only `Contents` has to be `Read-Only` for the token to work. Your `Overview` will look like so when correct:
![Overview](https://github.com/brondby-if/sport-repo-template/blob/main/images/overview.png)

9. Scroll down and click the `Generate token` button.

10. Copy the generated token.

11. Configure Poetry to use this token when accessing GitHub. Run the following command in your terminal:

```bash
poetry config http-basic.github <username> <token>
```

after that, private repos can be added to the pyproject.toml file as follows:

[tool.poetry.dependencies]

Generic example:
```bash
my-private-repo = { git = "https://github.com/username/my-private-repo.git" }
```

Real example:
```bash
sport_db_manager = { git = "https://github.com/brondby-if/sport_db_manager.git" }
```

### Copy Anaconda environment
Copy Anaconda environment:
```python
conda env export > environment.yml
```
This copies the environment to a yml file. This can be used to create a new environment with the same packages and name.

When downloading the environment.yml file type:
```python
conda env create -f environment.yml
```
This creates a new environment with the same packages and name.
## Branches
When working in github and especially working in a repository there are already up and running it is important to work in branches.
![alt text](https://github.com/brondby-if/sport-repo-template/blob/main/images/branch.png "Git branches")
So when working on something even if it's in development create a branch and when done working on it and it works merge it with main branch.
For creating a new branch locally:
```python
git branch <NAME>
```
For then moving to that branch:
```python
git checkout <NAME>
```
When done working and want to merge with main you switch the the main branch:
```python
git checkout main
git merge <NAME>
```

## Pre-commit

for pre-commit to work you need to install pre-commit:
```python
pip install pre-commit
```

afterwards the hooks needs to installed it can be done:
```python
pre-commit install
```

Automatically when commiting to github there will be some pre-commit checks.

You can run the pre-commit command before pre-commiting to check your work:
```python
pre-commit run --all-files
```

If there are problems when running pre-commit and you get an error with SSL you need to maybe downgrade the conda package openssl:
![alt text](https://github.com/brondby-if/sport-repo-template/blob/main/images/SSL.png "SSL Error")
```python
conda install openssl=1.1.1
```
The openssl version 1.1.1x works on the tested computers(30/08-23)

### Pre-commit list
* check-yaml - checks yaml files for parseable syntax
* end-of-file-fixer - ensures that a file is either empty, or ends with one newline.
* trailing-whitespace - trims trailing whitespace.
* black - code formatter
* flake8 - linting the code (identifying bugs)
* interrogate - checks docstrings (Needs to be above 20%)
* isort - sorts imports
* check requirements.txt - checks if requirements.txt is made

### Pre-commit failed

#### Git Desktop
If pre-commit failed and "files were modified by this hook" this means files were modified and we need to git add them again.

![alt text](https://github.com/brondby-if/sport-repo-template/blob/main/images/Failed%20pre-commit.png "Failed pre-commit")

Click commit in the buttom left corner and then click "Commit to main" in the top right corner.

[comment]: https://www.dev2qa.com/how-to-fix-importerror-dll-load-failed-while-importing-_sqlite3-the-specified-module-could-not-be-found/?utm_content=cmp-true

#### Git Terminal
If pre-commit failed and "files were modified by this hook" this means files were modified and we need to git add them again.
It could look like:
```python
$ git add .
$ git commit -m <MESSAGE>
```
![alt text](https://github.com/brondby-if/sport-repo-template/blob/main/images/Failed%20pre-commit.png "Failed pre-commit")
```python
$ git add .
$ git commit -m <MESSAGE>
```
![alt text](https://github.com/brondby-if/sport-repo-template/blob/main/images/Passed%20pre-commit.png "Passed pre-commit")
```python
$ git push
```


### Skip pre-commit
#### Git Terminal
When commiting to GitHub and want to skip pre-commits:
```python
git commit -m <MESSAGE> --no-verify
```

## Unittest
When commiting to github git actions runs unittests. In the repository there is a folder [tests](https://github.com/brondby-if/sport-repo-template/tree/main/tests) which **YOU** should write your unittests.
We recommend to install pytest and use as unittest:
```python
pip install pytest
```
The unittests tests multiple versions of python: 3.10, 3.11, and only runs when there are pushes to main.
Git actions only provides 2000 minutes a week. So remember to make branches to wark on, and the merge and push to main when task is done.

If you have a script to import data named, data.py the unittest script should be named, test_data.py.
