#!/usr/bin/env python3
"""DayZ Server Deployment Script
Reads deploy-config.yaml and rsyncs files to the correct server directories.
NO FILES DELETED — only overwritten if they exist in source.
"""

import subprocess
import os
import sys
import argparse

try:
    import yaml
except ImportError:
    print("pyyaml required: pip install pyyaml")
    sys.exit(1)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_config(config_path):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def build_rsync_cmd(src, dst, excludes, dry_run=False):
    """
    Rsync flags explained:
    -a: archive mode (preserves permissions, timestamps, symlinks)
    -v: verbose
    --ignore-times: always compare file sizes/times, not just checksums
    --exclude: ignore patterns
    NO --delete: prevents removing files in destination not in source
    """
    cmd = ["rsync", "-av"]
    if dry_run:
        cmd.append("--dry-run")
    for excl in excludes:
        cmd.extend(["--exclude", excl])
    cmd.append(src)
    cmd.append(dst)
    return cmd

def deploy_single(name, src_rel, dst_rel, config, dry_run):
    src = os.path.join(config["source_root"], src_rel) + "/"
    dst = os.path.join(config["dest_root"], dst_rel)

    if not os.path.exists(src.rstrip("/")):
        print(f"  [!] Source not found, skipping: {src}")
        return

    os.makedirs(dst, exist_ok=True)
    cmd = build_rsync_cmd(src, dst, config.get("excludes", []), dry_run)

    label = "[DRY RUN] " if dry_run else ""
    print(f"  {label}[{name}]")
    print(f"    FROM: {src}")
    print(f"    TO:   {dst}")
    print(f"    MODE: Overwrite only, no deletion of server files")

    if not dry_run:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"    ❌ ERROR: {result.stderr.strip()}")
        else:
            print(f"    ✅ OK")

def deploy_shared(name, src_rel, destinations, config, dry_run):
    src = os.path.join(config["source_root"], src_rel) + "/"

    if not os.path.exists(src.rstrip("/")):
        print(f"  [!] Source not found, skipping: {src}")
        return

    label = "[DRY RUN] " if dry_run else ""
    print(f"  {label}[{name}]")
    print(f"    FROM: {src}")
    print(f"    MODE: Overwrite only, no deletion of server files")

    for dst_rel in destinations:
        dst = os.path.join(config["dest_root"], dst_rel)
        os.makedirs(dst, exist_ok=True)
        cmd = build_rsync_cmd(src, dst, config.get("excludes", []), dry_run)

        print(f"    → {dst}")

        if not dry_run:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"      ❌ ERROR: {result.stderr.strip()}")
            else:
                print(f"      ✅ OK")

def main():
    parser = argparse.ArgumentParser(description="Deploy DayZ server files from workspace to server.")
    parser.add_argument("--config", default=os.path.join(SCRIPT_DIR, "deploy-config.yaml"),
                        help="Path to deploy-config.yaml")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview what would happen without making changes")
    parser.add_argument("--only", choices=["single", "shared"], default=None,
                        help="Deploy only single or shared mappings")
    args = parser.parse_args()

    config = load_config(args.config)

    print("=" * 60)
    print("  DayZ Server Deployment")
    print(f"  Source: {config['source_root']}")
    print(f"  Dest:   {config['dest_root']}")
    print(f"  Safety: NO FILES DELETED — overwrite only")
    if args.dry_run:
        print("  Mode:   DRY RUN (no changes made)")
    print("=" * 60)

    if not args.only or args.only == "single":
        print("\n── Single Destinations ──")
        for dep in config.get("deployments", []):
            deploy_single(dep["name"], dep["from"], dep["to"], config, args.dry_run)

    if not args.only or args.only == "shared":
        print("\n── Shared Destinations (one-to-many) ──")
        for dep in config.get("shared_deployments", []):
            deploy_shared(dep["name"], dep["from"], dep["destinations"], config, args.dry_run)

    print("\n" + "=" * 60)
    print("  Deployment complete.")
    print("=" * 60)

if __name__ == "__main__":
    main()