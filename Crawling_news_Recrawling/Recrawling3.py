import subprocess
from glob import glob
파일리스트 = glob("*.py")

for 파일 in 파일리스트:
    subprocess.call(['python', 파일])
