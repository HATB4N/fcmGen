import os

class BuildPropParser:
    def __init__(self, directory):
        self.filepath = os.path.join(directory, "build.prop")
        self.properties = {}

    def parse(self) -> dict:
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {self.filepath}")

        try:
            with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()

                    if not line or line.startswith('#'):
                        continue

                    if '=' in line:
                        key, value = line.split('=', 1)
                        self.properties[key.strip()] = value.strip()

            return self.properties

        except Exception as e:
            print(f"[-] Error while parsing build.prop: {e}")
            return {}