import os
import sys
import subprocess
import importlib
import platform
import pickle

# ----------------------------- CONFIG ---------------------------------
VENV_NAME = "venv"

# Exact dependency versions that work with your model.p
REQUIRED = {
    "numpy": "1.23.5",
    "scikit-learn": "1.2.2",
    "opencv-python": "4.8.1.78",
    "mediapipe": "0.10.11",
    "matplotlib": "3.7.3"
}
# ----------------------------------------------------------------------


def run_cmd(cmd, silent=False):
    """Run shell command"""
    if silent:
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        subprocess.run(cmd, shell=True)


def create_venv():
    """Create a virtual environment if not found"""
    if not os.path.exists(VENV_NAME):
        print(f"🔧 Creating virtual environment: {VENV_NAME}")
        subprocess.check_call([sys.executable, "-m", "venv", VENV_NAME])
    else:
        print(f"✅ Virtual environment '{VENV_NAME}' already exists.")


def get_venv_python():
    """Return full path to python executable inside venv"""
    if platform.system() == "Windows":
        return os.path.join(VENV_NAME, "Scripts", "python.exe")
    else:
        return os.path.join(VENV_NAME, "bin", "python")


def install_packages(py_exec):
    """Install or update all required dependencies"""
    print("\n📦 Checking and installing dependencies...")
    for pkg, ver in REQUIRED.items():
        try:
            module = importlib.import_module(pkg)
            if module.__version__ != ver:
                print(f"⚙️  Updating {pkg} to {ver} (current {module.__version__})...")
                subprocess.check_call([py_exec, "-m", "pip", "install", f"{pkg}=={ver}", "--quiet"])
            else:
                print(f"✅ {pkg} {ver} OK.")
        except ImportError:
            print(f"📦 Installing {pkg} {ver}...")
            subprocess.check_call([py_exec, "-m", "pip", "install", f"{pkg}=={ver}", "--quiet"])


def generate_requirements():
    """Generate or update requirements.txt"""
    print("\n🧾 Writing requirements.txt...")
    with open("requirements.txt", "w") as f:
        for pkg, ver in REQUIRED.items():
            f.write(f"{pkg}=={ver}\n")
    print("✅ requirements.txt generated successfully.")


def test_model():
    """Check if model.p exists and can be loaded"""
    if not os.path.exists("model.p"):
        print("❌ model.p not found! Please place it in this folder.")
        sys.exit(1)

    try:
        with open("model.p", "rb") as f:
            model = pickle.load(f)["model"]
        print("✅ Model loaded successfully.")
        return True
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return False


def main():
    print("=== ASL Recognition Setup Script ===")

    # 1️⃣ Create venv
    create_venv()
    py_exec = get_venv_python()

    # 2️⃣ Upgrade pip silently
    print("📥 Upgrading pip...")
    subprocess.check_call([py_exec, "-m", "pip", "install", "--upgrade", "pip", "--quiet"])

    # 3️⃣ Install dependencies
    install_packages(py_exec)

    # 4️⃣ Generate requirements.txt
    generate_requirements()

    # 5️⃣ Verify model file
    if not test_model():
        sys.exit(1)

    # 6️⃣ Let user choose what to run
    print("\n✅ Environment ready!")
    print("Choose an option to run:")
    print("1️⃣  Predict (static image test)")
    print("2️⃣  Live Webcam (app.py)")
    choice = input("Enter choice [1/2]: ").strip()

    if choice == "1":
        run_cmd(f'"{py_exec}" predict.py')
    elif choice == "2":
        run_cmd(f'"{py_exec}" app.py')
    else:
        print("❌ Invalid choice. Exiting.")


if __name__ == "__main__":
    main()
