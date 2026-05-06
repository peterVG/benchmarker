# Dependency Version Management

When scaffolding new projects or generating package manifests, you must prevent environment mismatch warnings and ensure modern package support by following these rules across all technology stacks (Node.js, Python, Elixir, Go, etc.):

1. **Define Engines/Environment Tracking**: Always explicitly define the expected runtime environment version in the configuration file.
   - **Node.js**: Require the specific `engine` in `package.json` (e.g., `"engines": { "node": ">=24.0.0" }`).
   - **Elixir/Mix**: Set the `elixir` requirement in `mix.exs` (e.g., `elixir: "~> 1.15"`).
   - **Python/Poetry/Pipenv**: Specify the `python` version constraint in `pyproject.toml` or `Pipfile`.
2. **Modern Dependency Constraints**: Do not blindly copy-paste hardcoded, outdated dependency versions from older training data or tutorials. When generating a list of dependencies, bias towards `^` (caret) or `~>` (tilde) versioning for the most recent major releases compatible with the user's modern runtime. Or better yet, initialize dependencies via native CLI installation tools (e.g., `npm install <pkg>`, `mix deps.get`, `pip install <pkg>`) so the package manager resolves the latest compatible version dynamically.
3. **Proactive Resolution**: If you encounter version compatibility warnings from testing frameworks (like Jest, Cucumber, PyTest, or ExUnit) or build tools during execution, proactively use update commands like `npm update <pkg>@latest`, `mix deps.update <pkg>`, or `pip install --upgrade <pkg>` to pull in environmental patches.
4. **Document External CLI Dependencies**: If a project relies on external CLI tools or system binaries for development, testing, or production (e.g., Allure CLI, Docker, specific database engines), you MUST explicitly include OS-agnostic installation instructions (e.g., Homebrew, APT, Scoop/Chocolatey) and their usage commands in the `README.md` under the appropriate Setup sections.
5. **Forbidden Packages/Anti-Patterns**:
   - **Python Pytest-BDD**: NEVER install the `allure-pytest-bdd` package. Modern versions of generic `allure-pytest` natively handle Pytest-BDD output. Installing both packages simultaneously will instantly crash Pytest with a `ValueError: option names {'--alluredir'} already added` conflict.
