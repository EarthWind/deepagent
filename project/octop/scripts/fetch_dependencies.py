#!/usr/bin/env python3
"""Download the four research sdists selected by the pinned Octop uv.lock."""
import argparse
import hashlib
import tarfile
import tomllib
import urllib.request
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("checkout", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    lock = tomllib.loads((args.checkout / "uv.lock").read_text())
    names = {"orcakit-harness-agent", "harness-memory", "harness-gateway", "deepagents"}
    for package in lock["package"]:
        if package["name"] not in names:
            continue
        sdist = package["sdist"]
        target = args.output / sdist["url"].rsplit("/", 1)[-1]
        if not target.exists():
            urllib.request.urlretrieve(sdist["url"], target)
        actual = "sha256:" + hashlib.sha256(target.read_bytes()).hexdigest()
        if actual != sdist["hash"]:
            raise SystemExit(f"Hash mismatch: {target}")
        with tarfile.open(target) as archive:
            archive.extractall(args.output, filter="data")
        print(f"Verified and extracted {package['name']} {package['version']}")


if __name__ == "__main__":
    main()
