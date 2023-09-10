# Python Virtual Environments

Python virtual environments are useful for maintaining stable development and production projects.

In this guide, we use `venv` to create virtual environments. The command to activate the environment depends on your system and terminal. This example uses Windows with the Command Prompt.

The virtual environment is based on the `requirements.txt` file, which provides instructions for `pip` to create the same environment.

Virtual environments have hardcoded paths to the files they need to run, so the paths will be different for each user.

## Table of Contents

- [Creating the Virtual Environment](#creating-the-virtual-environment)
- [Updating the Virtual Environment](#updating-the-virtual-environment)
- [Deactivating the Virtual Environment](#deactivating-the-virtual-environment)
- [Listing the packages in the Virtual Environment](#listing-the-packages-in-the-virtual-environment)
- [Documentation](#documentation)

## Creating the Virtual Environment

1. Navigate to the folder where you want to store the environment using `cd <path>`. If you create it inside the repository, make sure the `.gitignore` file is present to prevent the environment from being updated with your hardcoded paths. By default, the following command should create the `.gitignore` file.

2. Inside the folder, type:

    ```bash
    C:\>python -m venv <env_name>
    ```

    Replace `<env_name>` with your desired environment name, for example:

    ```bash
    C:\>python -m venv .venv
    ```

3. Then to activate the virtual enviroment use:

    ```bash
    C:\><fullpath of the enviroment>\Scripts\activate.bat
    ```

4. Now that you are inside the virtual environment, use the `requirements.txt` file to install the necessary packages.

    Note: The `<env_name>` in the prompt indicates that you are inside the virtual environment.

    ```bash
    C:\>(<env_name>)pip install -r <path/to/requirements.txt>
    ```

    In this way the requirements to run the scripts will have all dependencies.

## Updating the Virtual Environment

When new packages get added to enviroment the `requirements.txt` needs to get updated.

To do so, while inside the enviroment and located in the folder where you want to store the `requirements.txt`, use the `pip freeze` command to generate an updated `requirements.txt` file:

```bash
C:\>(<env_name>)pip freeze > requirements.txt
```
This command will overwrite the existing requirements.txt file with the current package list and their versions from your virtual environment. If you've added new packages or updated existing ones, this process ensures that the requirements.txt file reflects those changes.

To use the updated `requirements.txt` file to update the virtual enviroment use the same command as before:

```bash
C:\>(<env_name>)pip install -r <path/to/requirements.txt>
```

## Deactivating the Virtual Environment

Is possible that you need to deactivate the enviroment, maybe to use another one or to use the global one.

To deactivate your virtual environment while it's active use the `deactivate` command:

```bash
C:\>(<env_name>)deactivate
```

## Listing the packages in the Virtual Environment

While inside the enviroment is possible to list the packages active in the enviroment:

```bash
C:\>(<env_name>)pip list --local
```

## Documentation

For more details on venv, refer to [docs.python.org](https://docs.python.org/3/library/venv.html).