import argparse, os
import sys
from pathlib import Path

# remvoes old log files from a directory  (TODO: make the age configurable??)
AGE_DAYS = 30


def find_old(dir, now, age_days=AGE_DAYS):
    tmp2 = []
    for p in Path(dir).glob("*.log"):
        if now - p.stat().st_mtime > age_days * 86400:
            tmp2.append(p)
    return sorted(tmp2)


def cleanup(dir, now, dry_run=False, out=None):
    out = out or sys.stdout
    files = find_old(dir, now)
    for f in files:
        if dry_run:
            print(f"would delete {f}", file=out)
        else:
            os.remove(f)  #actualy delete it
    return files


def main(argv=None):
    ap = argparse.ArgumentParser(description='clean up old logs')
    ap.add_argument("dir")
    ap.add_argument("--dry-run", action="store_true", help="show what would be deleted wihtout deleting")
    a = ap.parse_args(argv)
    import time
    cleanup(a.dir, time.time(), dry_run=a.dry_run)


if __name__ == '__main__':
    main()
