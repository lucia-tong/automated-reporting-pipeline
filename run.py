    # script principal

from pathlib import Path
import subprocess, sys

if not Path("data/sales.csv").exists():
    print("No hay datos, generando CSV...")
    subprocess.run([sys.executable, "generate_data.py"], check=True)

from pipeline import main
main()
