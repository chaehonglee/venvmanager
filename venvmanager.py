import argparse
import os
import subprocess
import sys
import shutil

VENV_DIR = ".venvmanager"

def init_environment(version_name, requirements_file=None):
    env_path = os.path.join(VENV_DIR, version_name)
    if not os.path.exists(env_path):
        os.makedirs(env_path)
        result = subprocess.run([sys.executable, "-m", "venv", env_path], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error creating environment: {result.stderr}")
            return
        
        if requirements_file:
            result = subprocess.run([os.path.join(env_path, get_pip_path()), "install", "-r", requirements_file], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error installing requirements: {result.stderr}")
                return
        else:
            requirements_file = os.path.join(env_path, 'requirements.txt')
            with open(requirements_file, 'w') as f:
                pass
            print(f"Created empty requirements file at {requirements_file}. Please add your dependencies to this file.")
        
        print(f"Environment {version_name} created successfully.")
        export_dependencies(version_name, requirements_file)
    else:
        print(f"Environment {version_name} already exists.")

def activate_environment(version_name):
    env_path = os.path.join(VENV_DIR, version_name)
    if os.path.exists(env_path):
        print(f"To activate the environment, run:\nsource {os.path.join(env_path, 'bin' if os.name != 'nt' else 'Scripts', 'activate')}")
    else:
        print(f"Environment {version_name} does not exist.")

def list_environments():
    if os.path.exists(VENV_DIR):
        versions = [d for d in os.listdir(VENV_DIR) if os.path.isdir(os.path.join(VENV_DIR, d))]
        for version in versions:
            print(version)
    else:
        print(f"No environments found in {VENV_DIR}.")

def delete_environment(version_name):
    env_path = os.path.join(VENV_DIR, version_name)
    if os.path.exists(env_path):
        shutil.rmtree(env_path)
        print(f"Environment {version_name} deleted.")
    else:
        print(f"Environment {version_name} does not exist.")

def export_dependencies(version_name, file_path):
    env_path = os.path.join(VENV_DIR, version_name)
    if os.path.exists(env_path):
        with open(file_path, 'w') as f:
            result = subprocess.run([os.path.join(env_path, get_pip_path()), "freeze"], stdout=f, text=True)
            if result.returncode == 0:
                print(f"Dependencies exported to {file_path}.")
            else:
                print(f"Error exporting dependencies: {result.stderr}")
    else:
        print(f"Environment {version_name} does not exist.")

def get_pip_path():
    return "bin/pip" if os.name != 'nt' else "Scripts\\pip.exe"

def main():
    parser = argparse.ArgumentParser(
        description="Python Virtual Environment Version Manager",
        usage="%(prog)s [command] [options]"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    init_parser = subparsers.add_parser("init", help="Initialize a new environment")
    init_parser.add_argument("version_name", help="The version name for the environment")
    init_parser.add_argument("-r", "--requirements", help="Path to the requirements file", default=None)

    use_parser = subparsers.add_parser("use", help="Activate an environment")
    use_parser.add_argument("version_name", help="The version name for the environment")

    list_parser = subparsers.add_parser("list", help="List all environments")

    delete_parser = subparsers.add_parser("delete", help="Delete an environment")
    delete_parser.add_argument("version_name", help="The version name for the environment")

    export_parser = subparsers.add_parser("export", help="Export environment dependencies")
    export_parser.add_argument("version_name", help="The version name for the environment")
    export_parser.add_argument("file_path", help="The file path to export dependencies")

    args = parser.parse_args()

    if args.command == "init":
        init_environment(args.version_name, args.requirements)
    elif args.command == "use":
        activate_environment(args.version_name)
    elif args.command == "list":
        list_environments()
    elif args.command == "delete":
        delete_environment(args.version_name)
    elif args.command == "export":
        export_dependencies(args.version_name, args.file_path)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()