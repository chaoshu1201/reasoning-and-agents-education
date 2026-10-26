# Reasoning and Agents Notebooks

This repository contains notebooks and teaching materials for the EBU6505 Reasoning and Agents module.

The notebooks are designed to be read like a multimodal textbook: read the explanations, inspect the code, complete the exercises, and run cells to learn by doing.

## Beginner Quick Start

Follow these steps in order.

### 1. Prerequisites

- Python 3.12
- Git
- Terminal (or Command Prompt / PowerShell)
- Visual Studio Code (recommended)

### 2. Fork first (recommended for students)

Fork this repository to your own GitHub account before cloning. This gives you a personal copy in your own GitHub account where you can add your own notes, experiments, and solutions without affecting the original repository.

1. Open this repository on GitHub.
2. Click Fork.
3. Choose your own GitHub account as the owner.

### 3. Clone your fork

Clone your forked repository (replace `<your-username>`).

Recommended (SSH): better security and more stable authentication for regular GitHub use.

> [!NOTE]
> New to SSH? If you have not set up an SSH key for GitHub before, follow GitHub's official guide first:
> [Connecting to GitHub with SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

```bash
git clone git@github.com:<your-username>/reasoning-and-agents-education.git
cd reasoning-and-agents-education
```

Alternative (HTTPS):

```bash
git clone https://github.com/<your-username>/reasoning-and-agents-education.git
cd reasoning-and-agents-education
```

### 4. Create local environment file

Create your local environment file from the example:

```bash
cp .env.example .env
```

On Windows (PowerShell):

```bash
Copy-Item .env.example .env
```

No API key is required by default. The notebooks are configured to use local open-source models served by Ollama.

### 5. Install `uv` (if needed)

[uv](https://github.com/astral-sh/uv) is used to create the local environment and install dependencies.

On macOS/Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

On Windows (PowerShell):

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 6. Create the environment and install dependencies

From the project root:

```bash
uv sync
```

### 7. Activate the virtual environment

On macOS/Linux:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 8. Open and run notebooks

1. Open the project folder in VS Code.
2. Open any notebook (`.ipynb`).
3. Select the Python kernel before running cells.
4. Run cells from top to bottom.

Important: if the wrong kernel is selected, notebook cells may fail even when setup is correct.

## How to Study with These Materials

- Start with introductory notebooks and follow the module order (`L00`, `L01`, `L02`, ...).
- Read each notebook carefully as course text, not only as executable code.
- Use your fork to save your own notes directly in notebooks.

## Optional: View as Slides

All lesson notebooks (filenames beginning with `L`) can also be exported as HTML slides.

The custom [slide template](templates/fullscreen_slides.html.j2) provides larger text, a centred layout that adapts to the browser window, and scrolling for long slides.

Run this command from the repository root, replacing the notebook filename as needed:

```bash
uv run jupyter nbconvert --to slides --SlidesExporter.reveal_scroll=True --template-file templates/fullscreen_slides.html.j2 <Lxx_notebook_name>.ipynb
```

This creates `<Lxx_notebook_name>.slides.html` next to the notebook. Open the generated file in a browser.

The export uses the notebook's saved outputs. Run and save the notebook before exporting if you want the slides to include updated results.

### L00: Export and Serve Slides with Embedded Video

For L00's embedded YouTube video, view the slides through a local HTTP address rather than opening the HTML file directly with `file://`.

Run this command from the repository root to export the slides and start a local server:

```bash
uv run jupyter nbconvert --to slides --no-input --SlidesExporter.reveal_scroll=True --template-file templates/fullscreen_slides.html.j2 --post serve L00_ModuleIntro.ipynb
```

The `--no-input` option hides code inputs while retaining saved outputs, including embedded videos. The `--post serve` option starts a local server and opens the slides in your browser at [http://127.0.0.1:8000/L00_ModuleIntro.slides.html](http://127.0.0.1:8000/L00_ModuleIntro.slides.html).

### Serve an Existing Slides HTML File

If the `.slides.html` file already exists, you can serve it without converting the notebook again. From the repository root, run:

```bash
uv run python -m http.server 8000 --bind 127.0.0.1
```

Then open [http://127.0.0.1:8000/L00_ModuleIntro.slides.html](http://127.0.0.1:8000/L00_ModuleIntro.slides.html) in your browser. For another slide deck, replace `L00_ModuleIntro.slides.html` in the address with `<Lxx_notebook_name>.slides.html`.

This serves the existing HTML file as saved; it does not regenerate the slides or change their layout.

For either workflow, keep the terminal running while presenting and press **Ctrl+C** to stop the server. Stop an existing server before starting another on port 8000.

## Troubleshooting

If you encounter issues:

- Confirm that the virtual environment is activated.
- Confirm that you selected the correct notebook kernel.
- Re-run `uv sync` if dependencies are missing.
- Use the student forum or contact the lecturer.

## License

This material is provided for educational purposes as part of the EBU6505 module.
