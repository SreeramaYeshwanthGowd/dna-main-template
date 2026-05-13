import shutil
import subprocess
from pathlib import Path

project_type = "{{ cookiecutter.__project_type }}"
python_package_name = "{{ cookiecutter.__python_package_name }}"
scala_package_name = "{{ cookiecutter.__scala_package_name }}"
databricks_enabled = "{{ cookiecutter.__databricks_enabled }}"

print(f"Selected project type: {project_type}")


# # Initialize git repository


# print("Initializing git repository...")

# subprocess.run(
#     ["git", "init"],
#     check=False
# )


# Cleanup folders based on project type


if project_type == "python":

    print("Removing Scala folder...")
    shutil.rmtree("scala", ignore_errors=True)

elif project_type == "scala":

    print("Removing Python folder...")
    shutil.rmtree("python", ignore_errors=True)

elif project_type == "hybrid":

    print("Keeping both Python and Scala folders...")


# Rename Scala folder to package name for Scala-only projects


if project_type == "scala":

    source_scala_dir = Path("scala")
    target_scala_dir = Path(scala_package_name)

    if source_scala_dir.exists() and source_scala_dir != target_scala_dir:

        if target_scala_dir.exists():
            print(
                f"WARNING: Target folder '{target_scala_dir}' already exists. "
                "Skipping Scala folder rename."
            )
        else:
            print(f"Renaming Scala folder '{source_scala_dir}' -> '{target_scala_dir}'...")
            source_scala_dir.rename(target_scala_dir)


# Rename Python folder to package name for Python-capable projects


if project_type in ["python", "hybrid"]:

    source_python_dir = Path("python")
    target_python_dir = Path(python_package_name)

    if source_python_dir.exists() and source_python_dir != target_python_dir:

        if target_python_dir.exists():
            print(
                f"WARNING: Target folder '{target_python_dir}' already exists. "
                "Skipping Python folder rename."
            )
        else:
            print(f"Renaming Python folder '{source_python_dir}' -> '{target_python_dir}'...")
            source_python_dir.rename(target_python_dir)


# Rename Scala folder for hybrid projects


if project_type == "hybrid":

    source_scala_dir = Path("scala")
    target_scala_dir = Path(scala_package_name)

    if source_scala_dir.exists() and source_scala_dir != target_scala_dir:

        if target_scala_dir.exists():
            print(
                f"WARNING: Target folder '{target_scala_dir}' already exists. "
                "Skipping Scala folder rename."
            )
        else:
            print(f"Renaming Scala folder '{source_scala_dir}' -> '{target_scala_dir}'...")
            source_scala_dir.rename(target_scala_dir)


# Cleanup GitHub workflows


github_workflows = Path(".github/workflows")

python_workflow = github_workflows / "python-pr-check.yml"
scala_workflow = github_workflows / "scala-pr-check.yml"

if project_type == "python":

    print("Removing Scala workflow...")

    if scala_workflow.exists():
        scala_workflow.unlink()

elif project_type == "scala":

    print("Removing Python workflow...")

    if python_workflow.exists():
        python_workflow.unlink()

elif project_type == "hybrid":

    print("Removing duplicate Scala workflow and keeping a single PR workflow...")

    if scala_workflow.exists():
        scala_workflow.unlink()


# Optional Python virtual environment


if project_type in ["python", "hybrid"]:

    python_project_dir = Path(python_package_name)

    if not python_project_dir.exists():
        python_project_dir = Path("python")

    if shutil.which("python3"):

        print("Creating Python virtual environment...")

        subprocess.run(
            ["python3", "-m", "venv", str(python_project_dir / ".venv")],
            check=False
        )

    else:
        print("WARNING: python3 not found. Skipping venv creation.")


# Remove databricks.yml if Databricks DAB was not requested


if databricks_enabled != "yes":

    databricks_yml = Path("databricks.yml")

    if databricks_yml.exists():
        databricks_yml.unlink()
        print("Removed databricks.yml (Databricks DAB not enabled).")


print("Project generation completed successfully.")