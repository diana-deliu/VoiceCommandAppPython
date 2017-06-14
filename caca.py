import subprocess
bat_file_path = 'scripts/inchide_muzica.bat'

p = subprocess.Popen('start cmd /c scripts\inchide_muzica.bat', shell=True)
p.wait()