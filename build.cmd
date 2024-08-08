rem pyinstaller --workpath "build" --specpath "build/spec" --distpath "." --console --onefile client/client.py

py -m nuitka --standalone --onefile^
  --product-name="ChatV6 Client Application" --product-version=1.0.0 --file-description="The ChatV6 Client" --copyright="Copyright © 2024 Omena0. All rights reserved."^
  --output-dir="build"^
  --deployment --python-flag="-OO" --python-flag="-S"^
  --output-filename="client.exe"^
  client/client.py

xcopy /Y "build\client.exe" "client.exe"
