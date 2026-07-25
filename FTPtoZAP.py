#!/usr/bin/env python3
import ftplib
import os
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

def load_config(config_path="ftp_config.json"):
    with open(config_path, "r") as f:
        return json.load(f)

def ensure_remote_dir(ftp, remote_dir):
    """Create remote directory if it doesn't exist."""
    dirs = remote_dir.strip("/").split("/")
    current = ""
    for d in dirs:
        if not d: 
            continue
        current += "/" + d
        try:
            ftp.mkd(current)
        except ftplib.error_perm:
            pass  # Directory already exists

def get_remote_mtime(ftp, remote_path):
    """Get the last modified time of a remote file as a Unix timestamp."""
    try:
        # Ask server for the file's modified time
        res = ftp.sendcmd(f"MDTM {remote_path}")
        if res.startswith("213 "):
            time_str = res[4:].strip()
            # FTP MDTM format is usually YYYYMMDDHHMMSS in UTC
            dt = datetime.strptime(time_str, "%Y%m%d%H%M%S")
            dt = dt.replace(tzinfo=timezone.utc)
            return dt.timestamp()
    except ftplib.error_perm:
        pass # File doesn't exist on remote yet
    return None

def upload_file(ftp, local_path, remote_path):
    """Upload a single file to FTP."""
    with open(local_path, "rb") as f:
        ftp.storbinary(f"STOR {remote_path}", f)
    print(f"  ✅ Uploaded: {os.path.basename(local_path)}")

def sync_directory(ftp, local_dir, remote_dir, dry_run=False):
    """Recursively sync a local directory to FTP, only uploading newer files."""
    local_dir = os.path.expanduser(local_dir)
    
    if not os.path.isdir(local_dir):
        print(f"  ❌ Local dir not found: {local_dir}")
        return False
    
    print(f"\n  Syncing: {local_dir}")
    print(f"       → {remote_dir}")
    
    if not dry_run:
        ensure_remote_dir(ftp, remote_dir)
    
    for root, dirs, files in os.walk(local_dir):
        rel_path = os.path.relpath(root, local_dir)
        
        # Handle remote subdirectories
        if rel_path != ".":
            remote_subdir = f"{remote_dir}/{rel_path}".replace("\\", "/")
            if not dry_run:
                ensure_remote_dir(ftp, remote_subdir)
        else:
            remote_subdir = remote_dir
        
        for filename in files:
            local_file = os.path.join(root, filename)
            remote_file = f"{remote_subdir}/{filename}"
            
            # Compare local and remote modified times
            local_mtime = os.path.getmtime(local_file)
            remote_mtime = get_remote_mtime(ftp, remote_file)
            
            # Upload if remote file is missing (None) or local file is newer
            if remote_mtime is None or local_mtime > remote_mtime:
                if dry_run:
                    print(f"  [DRY RUN] Would upload: {filename} (Newer or missing)")
                else:
                    try:
                        upload_file(ftp, local_file, remote_file)
                    except Exception as e:
                        print(f"  ❌ Failed: {filename} - {e}")
            else:
                if dry_run:
                    print(f"  [DRY RUN] Would skip: {filename} (Up to date)")
                else:
                    print(f"  ⏭️  Skipped (up to date): {filename}")
    
    return True

def main():
    config = load_config()
    
    dry_run = "--dry-run" in sys.argv
    
    if dry_run:
        print("🔍 DRY RUN MODE - No files will be uploaded\n")
    
    for server in config["servers"]:
        name = server["name"]
        host = server["host"]
        port = server.get("port", 21)
        user = server["username"]
        password = server["password"]
        
        print(f"{'='*50}")
        print(f"🎮 {name}")
        print(f"{'='*50}")
        
        try:
            print(f"Connecting to {host}:{port}...")
            ftp = ftplib.FTP()
            ftp.connect(host, port, timeout=30)
            ftp.login(user, password)
            print(f"✅ Connected as {user}\n")
            
            for dep in server["deployments"]:
                local = dep["local"]
                remote = dep["remote"]
                
                success = sync_directory(ftp, local, remote, dry_run)
                
                if success and not dry_run:
                    print(f"  ✅ Done: {remote}")
                elif not success:
                    print(f"  ⚠️  Skipped: {local}")
            
            ftp.quit()
            print(f"\n✅ Disconnected from {name}")
            
        except ftplib.all_errors as e:
            print(f"❌ FTP Error: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n{'='*50}")
    print("🚀 Deploy complete!")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()