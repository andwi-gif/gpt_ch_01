import subprocess

def test_reproduce_smoke():
    proc = subprocess.run(["python", "scripts/reproduce_objective1.py", "--config", "configs/eval/default.yaml"], capture_output=True, text=True, check=False)
    assert proc.returncode == 0
    assert "offline" in proc.stdout.lower()
