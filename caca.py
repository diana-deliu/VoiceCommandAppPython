import subprocess
bat_file_path = 'scripts/porneste_internet.bat'

p = subprocess.Popen('start cmd /c scripts\porneste_internet.bat', shell=True)
p.wait()