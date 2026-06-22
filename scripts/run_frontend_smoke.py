import os
import subprocess
import sys

HERE = os.path.dirname(__file__)
FRONTEND = os.path.abspath(os.path.join(HERE, '..', 'frontend'))

def main():
    node = shutil_which('node')
    if not node:
        print('Node.js is required to run the frontend smoke test.');
        return 2
    cmd = ['node', os.path.join(FRONTEND, 'auto_smoke.js')]
    env = os.environ.copy()
    # allow TARGET_URL to be set by caller
    return subprocess.call(cmd, env=env)

def shutil_which(name):
    from shutil import which
    return which(name)

if __name__ == '__main__':
    sys.exit(main())
