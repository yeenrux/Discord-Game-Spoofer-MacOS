import subprocess
import plistlib
import re
from pathlib import Path

def clean(value):
    return re.sub(r'[/\\*?"<>|]', '-', value).strip().strip('.') or "Game"

def spoof(name, game_id):
    cleaned = clean(name)
    app = Path.home() / "Library/Application Support/Steam/steamapps/common" / cleaned / f"{cleaned}.app"
    folder = app / "Contents" / "MacOS"
    folder.mkdir(parents=True, exist_ok=True)
    executable = folder / cleaned
    plist = {
        "CFBundleExecutable": cleaned,
        "CFBundleName": name,
        "CFBundleDisplayName": name,
        "CFBundleIdentifier": "com.fake.game",
        "CFBundlePackageType": "APPL",
    }
    (app / "Contents" / "Info.plist").write_bytes(plistlib.dumps(plist))
    subprocess.run(
        "clang objc/app.m -fobjc-arc -O2 -framework Cocoa -o".split() + [str(executable)],
        cwd=Path(__file__).parent,
        check=True,
    )
    executable.chmod(0o755)
    proc = subprocess.Popen(
        [str(executable), name],
        start_new_session=True,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        close_fds=True,
    )
    return proc.pid, app
