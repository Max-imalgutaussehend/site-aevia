"""Builds site/ from src/ (layout + page fragments). Run: python3 build.py

assets/ (theme CSS, JS, fonts) is kept in the repository as it is; only the HTML pages are generated.
"""
import os
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
PAGES = [
    # slug, nav label, <title>, description
    ("index", "Overview", "Aevia", "A personal platform on one server, rebuilt from Git."),
    ("architecture", "Architecture", "Architecture | Aevia", "How a request travels and what is isolated from what."),
    ("stack", "Stack", "Stack | Aevia", "The components Aevia is made of and why each one is there."),
]


def nav(active, root):
    items = []
    for slug, label, _, _ in PAGES:
        href = f"{root}index.html" if slug == "index" else f"{root}{slug}/index.html"
        cls = " active" if slug == active else ""
        cur = ' <span class="sr-only">(current)</span>' if slug == active else ""
        items.append(f'<li class="nav-item{cls}"> <a class="nav-link" href="{href}">{label}{cur}</a> </li>')
    items.append('<li class="nav-item"> <a class="nav-link" href="https://github.com/Max-imalgutaussehend/aevia" '
                 'target="_blank" rel="noopener">GitHub</a> </li>')
    return " ".join(items)


def main():
    layout = open(os.path.join(ROOT, "src", "layout.html")).read()
    for slug, _label, title, desc in PAGES:
        content = open(os.path.join(ROOT, "src", "pages", f"{slug}.html")).read()
        root = "" if slug == "index" else "../"
        html = (layout.replace("{{nav}}", nav(slug, root)).replace("{{content}}", content)
                .replace("{{title}}", title).replace("{{description}}", desc).replace("{{root}}", root))
        out = os.path.join(ROOT, "site", "index.html") if slug == "index" else os.path.join(ROOT, "site", slug, "index.html")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w").write(html)
        print("wrote", os.path.relpath(out, ROOT))


if __name__ == "__main__":
    main()
