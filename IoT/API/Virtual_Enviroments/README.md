# Python Virtual Environments

In Python development, isolation of dependencies per project is crucial to avoid conflicts and ensure consistency. A "Virtual Environment" enables such isolation. This tutorial will guide you on managing project-specific dependencies using virtual environments on both Windows and Linux systems.

We will use `venv`, a module provided in Python's standard library to create virtual environments, and `pip` to install and manage packages within these environments.

The required packages for the project are provided in the `requirements.txt` file. The paths are hardcoded in the virtual environment. As such, the paths will differ for each user.

## Table of Contents

- [Creating the Virtual Environment](#creating-the-virtual-environment)
  - [Windows](#windows)
  - [Linux](#linux)
- [Activating the Virtual Environment](#activating-the-virtual-environment)
  - [Windows](#windows-1)
  - [Linux](#linux-1)
- [Deactivating the Virtual Environment](#deactivating-the-virtual-environment)
- [Updating the Virtual Environment](#updating-the-virtual-environment)
- [Listing the packages in the Virtual Environment](#listing-the-packages-in-the-virtual-environment)
- [Official Documentation and Other Tools](#official-documentation-and-other-tools)

## Creating the Virtual Environment

### Windows

1. Navigate to the desired folder using the `cd` command. If the environment is inside the repository, verify `.gitignore` is present to prevent uploading the environment containing your hardcoded paths.

2. To create the virtual environment, run the following command:

    ```bash
    C:\>python -m venv <environment_name>
    ```

    Replace `<environment_name>` with your desired environment name.

### Linux

The process to create a virtual environment in Linux is similar to Windows, but you'll use `python3` instead of `python`.

## Activating the Virtual Environment

### Windows

1. Activate the environment using the following command:

    - Command prompt

        ```bash
        C:\><fullpath of the enviroment>\Scripts\activate.bat
        ```

    - PowerShell

        ```powershell
        PS C:\><fullpath of the enviroment>\Scripts\Activate.ps1
        ```

    Note: `<environment_name>` in the prompt signifies an active virtual environment.

2. Now, you may install necessary packages specified in the `requirements.txt` file.

    ```bash
    C:\>(<environment_name>)pip install -r <path/to/requirements.txt>
    ```

### Linux

The command for Linux systems is slightly different. Following is the process:

1. Activate the virtual environment with `source`:

    ```bash
    source <environment_name>/bin/activate
    ```

2. Install necessary packages using the `requirements.txt` file:

    ```bash
    (environment_name) $ pip install -r <path/to/requirements.txt>
    ```

## Deactivating the Virtual Environment

If you need to switch environments or revert to the global one, use the `deactivate` command.

## Updating the Virtual Environment

New packages necessitate an update in the `requirements.txt` file. Accomplish this via `pip freeze`:

```bash
(<environment_name>)pip freeze > requirements.txt
```

This command updates the `requirements.txt` file reflecting any added or updated packages. To install these changes, use the previous command:

```bash
(<environment_name>)pip install -r <path/to/requirements.txt>
```

## Listing the packages in the Virtual Environment

To view all the installed packages and their versions in the virtual environment, use:

```bash
(<environment_name>)pip list --local
```

## Official Documentation and Other Tools

If you require more details or alternative tools, consider the following resources:

- [venv Official Documentation](https://docs.python.org/3/library/venv.html).
- [pip Official Documentation](https://pip.pypa.io/en/stable/).
- [virtualenv](https://virtualenv.pypa.io/en/latest/)
- [pipenv](https://github.com/pypa/pipenv)
- [poetry](https://python-poetry.org/)
- [conda](https://docs.conda.io/en/latest/)
- [pipx](https://pypa.github.io/pipx/)
