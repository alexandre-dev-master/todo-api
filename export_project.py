from pathlib import Path

ROOT = Path(".")

EXTENSIONS = {
    ".py",
    ".toml",
    ".yaml",
    ".yml",
    ".md",
    ".txt",
}

FILES = {
    "requirements.txt",
    ".env.example",
}

IGNORE = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
}

with open("projeto_fastapi.txt", "w", encoding="utf-8") as out:
    for path in sorted(ROOT.rglob("*")):
        if any(part in IGNORE for part in path.parts):
            continue

        if not path.is_file():
            continue

        if path.suffix in EXTENSIONS or path.name in FILES:
            out.write("=" * 80 + "\n")
            out.write(f"{path}\n")
            out.write("=" * 80 + "\n\n")

            try:
                out.write(path.read_text(encoding="utf-8"))
            except UnicodeDecodeError:
                out.write("[Arquivo binário ignorado]")

            out.write("\n\n")