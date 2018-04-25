xcopy ..\azure\*.py azext_acrbuildext\azure\ /sy
xcopy ..\*.py azext_acrbuildext\ /y
xcopy ..\*.json azext_acrbuildext\ /y
xcopy __init__.py azext_acrbuildext\ /y
python setup.py bdist_wheel
rmdir azext_acrbuildext /s /q
rmdir acrbuildext.egg-info /s /q
rmdir build /s /q
