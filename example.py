import subprocess
bat_file_path = 'scripts/deschide_editor_grafic.bat'

p = subprocess.Popen('start cmd /c scripts\deschide_editor_grafic.bat', shell=True)
p.wait()
