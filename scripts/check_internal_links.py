#!/usr/bin/env python3
from argparse import ArgumentParser
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse
import sys

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            self.ids.add(values["id"])
        if tag == "a" and "name" in values:
            self.ids.add(values["name"])
        if tag in {"a", "link"} and "href" in values:
            self.links.append(values["href"])
        if tag in {"script", "img", "source"} and "src" in values:
            self.links.append(values["src"])

def output_target(root: Path, site_path: str) -> Path:
    rel = unquote(site_path).lstrip("/")
    if not rel:
        return root / "index.html"
    candidate = root / rel
    if site_path.endswith("/"):
        return candidate / "index.html"
    if candidate.suffix:
        return candidate
    return candidate / "index.html"

def page_url(html_file: Path, root: Path, prefix: str) -> str:
    rel = html_file.relative_to(root).as_posix()
    if rel == "index.html":
        path = prefix
    elif rel.endswith("/index.html"):
        path = prefix + rel[:-10]
    else:
        path = prefix + rel
    return "https://local.test" + path

def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--prefix", default="/")
    args = parser.parse_args()
    root = args.root.resolve()
    prefix = "/" + args.prefix.strip("/") + "/" if args.prefix.strip("/") else "/"
    html_files = sorted(root.rglob("*.html"))
    if not html_files:
        print(f"No rendered HTML found under {root}")
        return 1
    parsed = {}
    for html_file in html_files:
        p = PageParser()
        p.feed(html_file.read_text(encoding="utf-8"))
        parsed[html_file.resolve()] = p
    errors = []
    checked = 0
    for source, page in parsed.items():
        base = page_url(source, root, prefix)
        for raw in page.links:
            if not raw or raw.startswith(("mailto:", "tel:", "javascript:", "data:")):
                continue
            absolute = urlparse(urljoin(base, raw))
            if absolute.scheme not in {"http", "https"}:
                continue
            if absolute.netloc not in {"local.test", "qiuyi111.github.io"}:
                continue
            path = absolute.path
            if prefix != "/":
                if path == prefix.rstrip("/"):
                    path = prefix
                if not path.startswith(prefix):
                    errors.append(f"{source.relative_to(root)}: internal URL escapes site prefix: {raw}")
                    continue
                path = "/" + path[len(prefix):].lstrip("/")
            target = output_target(root, path)
            checked += 1
            if not target.exists():
                errors.append(f"{source.relative_to(root)}: missing target for {raw} -> {target.relative_to(root)}")
                continue
            fragment = unquote(absolute.fragment)
            if fragment and target.suffix == ".html":
                target_page = parsed.get(target.resolve())
                if target_page is None:
                    p = PageParser()
                    p.feed(target.read_text(encoding="utf-8"))
                    target_page = p
                    parsed[target.resolve()] = p
                if fragment not in target_page.ids:
                    errors.append(f"{source.relative_to(root)}: missing anchor #{fragment} in {target.relative_to(root)}")
    if errors:
        print("Internal link check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Internal link check passed: {len(html_files)} HTML pages, {checked} internal targets checked.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
