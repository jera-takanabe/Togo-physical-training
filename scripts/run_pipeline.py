from pathlib import Path
import subprocess
import sys


BASE_DIR = Path(__file__).resolve().parent.parent
PYTHON_EXE = sys.executable

SCRIPTS = [
    BASE_DIR / "scripts" / "validate_data.py",
    BASE_DIR / "scripts" / "build_sessions.py",
    BASE_DIR / "scripts" / "update_personal_bests.py",
    BASE_DIR / "scripts" / "build_latest_summary.py",
]


def main():
    for script in SCRIPTS:
        print(f"Running: {script.name}")
        result = subprocess.run([PYTHON_EXE, str(script)], cwd=BASE_DIR)
        if result.returncode != 0:
            print(f"Failed: {script.name}")
            sys.exit(result.returncode)

    print("Pipeline completed successfully.")


if __name__ == "__main__":
    main()