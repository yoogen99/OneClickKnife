"""Build the installable legacy add-on ZIP using only the Python standard library."""

import argparse
import ast
from pathlib import Path
import zipfile


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_FILES = ("__init__.py", "README.md", "LICENSE", "CHANGELOG.md")


def read_version():
    tree = ast.parse((ROOT / "__init__.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "bl_info"
            for target in node.targets
        ):
            return ".".join(map(str, ast.literal_eval(node.value)["version"]))
    raise ValueError("bl_info version was not found")


def build(output, tag=None):
    version = read_version()
    if tag is not None and tag != f"v{version}":
        raise ValueError(f"Tag {tag!r} must match bl_info version v{version}")
    output = output.resolve()
    if output in [(ROOT / name).resolve() for name in PACKAGE_FILES]:
        raise ValueError("Output must not overwrite a package source file")
    # Normalize line endings so Windows checkouts and Linux CI produce the same ZIP.
    files = [(name, (ROOT / name).read_text(encoding="utf-8").encode("utf-8"))
             for name in PACKAGE_FILES]
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in files:
            info = zipfile.ZipInfo(f"OneClickKnife/{name}", (2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    print(f"Built OneClickKnife {version}: {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist" / "OneClickKnife.zip")
    parser.add_argument("--tag", help="Require a tag matching the add-on version (vX.Y.Z)")
    args = parser.parse_args()
    build(args.output, args.tag)
