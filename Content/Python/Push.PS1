cd "C:\Users\DavidBaker\Downloads\Qhuantz\"
New-Item -Path "C:\Users\DavidBaker\Downloads\Qhuantz\Content\Python\script_name.py" -ItemType File -Value "Script Contents"
UnrealEditor-Cmd.exe "C:\Users\DavidBaker\Downloads\Qhuantz\Qhauntz.uproject" -ExecutePythonScript="C:\Users\DavidBaker\Downloads\Qhuantz\Content\Python\script_name.py" -stdout -FullStdOutLogOutput
& 'C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\Tools\Launch-VsDevShell.ps1'
msbuild "C:\Users\DavidBaker\Downloads\Qhuantz\Qhauntz.sln"
git add .
git commit -m "commit message"
git push origin Dev