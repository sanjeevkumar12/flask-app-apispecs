"""Utility functions for dealing with env variables and reading variables from env file"""
import json
import logging
import os
import pathlib
import secrets
import sys

from cryptography.fernet import Fernet

BOOLEAN_TYPE = "boolean"
INT_TYPE = "int"
FLOAT_TYPE = "float"
STRING_TYPE = "str"
LIST_TYPE = "list"
DICT_TYPE = "dict"


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")


BASE_DIR = pathlib.Path(__file__).parent.parent


def get_envvars(
    env_file=".env", set_environ=True, ignore_not_found_error=False, exclude_override=()
):
    """
    Set env vars from a file
    :param env_file:
    :param set_environ:
    :param ignore_not_found_error: ignore not found error
    :param exclude_override: if parameter found in this list, don't overwrite environment
    :return: list of tuples, env vars
    """
    env_vars = []
    try:

        with open(env_file) as f:
            for line in f:
                line = line.replace("\n", "")

                if not line or line.startswith("#"):
                    continue

                # Remove leading `export `
                if line.lower().startswith("export "):
                    key, value = line.replace("export ", "", 1).strip().split("=", 1)
                else:
                    try:
                        key, value = line.strip().split("=", 1)
                    except ValueError:
                        logging.error(
                            f"envar_utils.get_envvars error parsing line: '{line}'"
                        )
                        raise

                if set_environ and key not in exclude_override:
                    os.environ[key] = value

                if key in exclude_override:
                    env_vars.append({"name": key, "value": os.getenv(key)})
                else:
                    env_vars.append({"name": key, "value": value})
    except FileNotFoundError:
        if not ignore_not_found_error:
            raise

    return env_vars


def create_envvar_file(env_file_path, envvars):
    """
    Writes envvar file using env var dict
    :param env_file_path: str, path to file to write to
    :param envvars: dict, env vars
    :return:
    """
    with open(env_file_path, "w+") as f:
        for key, value in envvars.items():
            f.write("{}={}\n".format(key, value))
    return True


def convert_env_var_flag_to(env_var_name, required_type, default_value):
    """
    Convert env variable string flag values to required_type
    :param env_var_name: str, environment variable name
    :param required_type: str, required type to cast the env var to
    :param default_value: boolean, default value to use if the environment variable is not available
    :return: environment variable value in required type
    """
    env_var_orginal_value = os.getenv(env_var_name, default_value)
    env_var_value = ""
    try:
        if required_type == INT_TYPE:
            env_var_value = int(env_var_orginal_value)
        elif required_type == FLOAT_TYPE:
            env_var_value = float(env_var_orginal_value)
        elif required_type == BOOLEAN_TYPE:
            env_var_value = bool(int(env_var_orginal_value))
        elif required_type == STRING_TYPE:
            env_var_value = str(env_var_orginal_value)
        elif required_type == LIST_TYPE:
            env_var_value = (
                env_var_orginal_value.split(",")
                if len(env_var_orginal_value) > 0
                else default_value
            )
        elif required_type == DICT_TYPE:
            try:
                env_var_value = (
                    json.loads(env_var_orginal_value)
                    if env_var_orginal_value
                    else default_value
                )
            except Exception as e:
                logging.error(
                    f"convert_env_var_flag_to: failed loading {env_var_orginal_value} error {e}"
                )
                env_var_value = default_value
        else:
            logging.error(
                "Unrecognized type {} for env var {}".format(
                    required_type, env_var_name
                )
            )

    except ValueError:
        env_var_value = default_value
        logging.warning("{} is {}".format(env_var_name, env_var_orginal_value))

    return env_var_value


def _setup_database_uri():
    databases = ["postgresql", "mysql", "sqlite"]
    sys.stdout.write("\nSet up database settings \n")
    sys.stdout.write("\nChoose database type\n")
    for index, db in enumerate(databases):
        sys.stdout.write(f"\n{index} => {db}")
    sys.stdout.write("\nEnter your choice : ")
    database_type = database_name = database_password = database_user_name = None
    database_host = "localhost"
    while True:
        try:
            database_type = databases[int(input().strip())]
            break
        except Exception:
            sys.stdout.write("\nPlease choose valid option\n")
            continue

    if not database_type == "sqlite":
        sys.stdout.write("\nEnter Database Name : ")
        database_port = 5432 if database_type == "postgresql" else 3306
        while True:
            try:
                database_name = str(input().strip())
                if not database_name:
                    raise Exception
                break
            except Exception:
                sys.stdout.write("\nEnter Database Name : ")
                continue
        sys.stdout.write("\nEnter Database Username : ")
        while True:
            try:
                database_user_name = str(input().strip())
                if not database_user_name:
                    raise Exception
                break
            except Exception:
                sys.stdout.write("\nEnter Database Username")
                continue
        sys.stdout.write("\nEnter Database Password : ")
        while True:
            try:
                database_password = str(input().strip())
                if not database_password:
                    raise Exception
                break
            except Exception:
                sys.stdout.write("\nEnter Database Password : ")
                continue
        return f"{database_type}://{database_user_name}:{database_password}@{database_host}:{database_port}/{database_name}"


def _set_secret_key():
    app_secret = secrets.token_hex(50)
    sys.stdout.write(
        "\nSet up app secret key min 10 chars. Press enter to use default or add your own key \n"
    )
    sys.stdout.write(f"\nDefault : {app_secret}\nEnter:")
    user_app_secret = input().strip()
    if user_app_secret and len(user_app_secret) < 10:
        sys.stdout.write("APP Secret key is not valid. Enter any key to continue : ")
        input()
        return _set_secret_key()
    return user_app_secret if user_app_secret else app_secret


def _set_app_encryption_key():
    encryption_key = Fernet.generate_key()
    sys.stdout.write(
        "\nSet up app encryption key. Press enter to use default or add your own key \n"
    )
    sys.stdout.write(f"\nDefault : {encryption_key}\nEnter:")
    user_encryption_key = input().strip()
    if user_encryption_key:
        user_encryption_key = user_encryption_key.encode()
        try:
            f = Fernet(user_encryption_key)
            f.encrypt(b"A really secret message. Not for prying eyes.")
            encryption_key = user_encryption_key
        except Exception:
            sys.stdout.write(
                "APP encryption key is not valid. Enter any key to continue : "
            )
            input()
        return _set_app_encryption_key()
    return encryption_key.decode()


def create_env_file_from_sample():
    default_envars = dict()
    default_envars["APP_ENV"] = "development"
    default_envars["API_TITLE"] = "API Title"
    default_envars["API_DESCRIPTION"] = "API DESCRIPTION"
    default_envars["API_VERSION"] = "v.1.0"
    default_envars["APP_DEBUG"] = True
    default_envars["FLASK_APP"] = "run.py"
    default_envars["FLASK_ENV"] = "development"
    env_vars = {
        i["name"]: i["value"] for i in get_envvars(str(BASE_DIR / "example.env"))
    }
    env_vars = {
        key: value if value else default_envars.get(key, "")
        for key, value in env_vars.items()
    }
    if "APP_SECRET_KEY" in env_vars:
        sys.stdout.write("==" * 30)
        env_vars["APP_SECRET_KEY"] = _set_secret_key()

    if "APP_ENCRYPTION_KEY" in env_vars:
        sys.stdout.write("==" * 30)
        env_vars["APP_ENCRYPTION_KEY"] = _set_app_encryption_key()

    if "SQLALCHEMY_DATABASE_URI" in env_vars:
        sys.stdout.write("==" * 30)
        database_url = _setup_database_uri()
        database_url_list = database_url.rsplit("/", 1)
        database_url_list[-1] = f"test_{database_url_list[-1]}"
        test_database_url = "/".join(database_url_list)
        env_vars["SQLALCHEMY_DATABASE_URI"] = database_url
        env_vars["SQLALCHEMY_DATABASE_TESTING_URI"] = test_database_url
    if not (BASE_DIR / ".env").exists():
        create_envvar_file(str(BASE_DIR / ".env"), env_vars)
    else:
        sys.stdout.write(".env file already exists. Process cancelled")


if __name__ == "__main__":
    try:
        create_env_file_from_sample()
    except KeyboardInterrupt:
        sys.stdout.write("Env Process cancelled")
