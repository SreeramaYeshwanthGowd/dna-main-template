import json


def prompt_non_empty(prompt_text):
    """Prompt until a non-empty value is provided."""
    while True:
        value = input(prompt_text).strip()
        if value:
            return value
        print("Value cannot be empty. Please try again.")


base_config = {
    "repo_name": "dna-sample-service",
    "project_name": "DNA Sample Service",
    "author_name": "Your Name",
    "team_name": "DPS",
    "spark_version": "3.5.0",
}

print("\nSelect project type:")
print("1 - python")
print("2 - scala")
print("3 - hybrid")

choice = input("Choose [1/2/3]: ").strip()

if choice == "1":
    base_config["__project_type"] = "python"
    base_config["python_version"] = "3.11"

    python_pkg = prompt_non_empty("Enter Python package folder name: ")
    base_config["__python_package_name"] = python_pkg
    base_config["__scala_package_name"] = ""

elif choice == "2":
    base_config["__project_type"] = "scala"
    base_config["scala_version"] = "2.12.18"

    scala_pkg = prompt_non_empty("Enter Scala package folder name: ")
    base_config["__scala_package_name"] = scala_pkg
    base_config["__python_package_name"] = ""

else:
    base_config["__project_type"] = "hybrid"
    base_config["python_version"] = "3.11"
    base_config["scala_version"] = "2.12.18"

    print("\nHybrid project selected.")

    python_pkg = prompt_non_empty("Enter Python package folder name: ")
    scala_pkg = prompt_non_empty("Enter Scala package folder name: ")

    while python_pkg == scala_pkg:
        print("Python and Scala folder names must be different for hybrid projects.")
        scala_pkg = prompt_non_empty("Enter a different Scala package folder name: ")

    base_config["__python_package_name"] = python_pkg
    base_config["__scala_package_name"] = scala_pkg

# Databricks DAB setup
print("\nDatabricks Asset Bundle (DAB) setup:")
while True:
    dab_choice = input("Do you want to set up Databricks DAB? [y/n]: ").strip().lower()
    if dab_choice in ("y", "n"):
        break
    print("Please enter 'y' or 'n'.")

if dab_choice == "y":
    base_config["__databricks_enabled"] = "yes"
    base_config["__databricks_host"] = prompt_non_empty("Enter Databricks workspace host URL: ")
    base_config["__databricks_profile"] = prompt_non_empty("Enter Databricks CLI profile name: ")
else:
    base_config["__databricks_enabled"] = "no"
    base_config["__databricks_host"] = ""
    base_config["__databricks_profile"] = ""

with open("cookiecutter.json", "w") as f:
    json.dump(base_config, f, indent=2)