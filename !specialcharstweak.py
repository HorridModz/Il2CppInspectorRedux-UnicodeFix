import os
import re


def escape_str(s: str, single_quote: bool) -> str:
    escaped = s.replace("\\", r"\\").replace(r"\n", r"\\n")
    if single_quote:
        return escaped.replace("'", r"\'")
    else:
        return escaped.replace("\"", "\\\"")

WHITELIST_CHARS = input("Enter the chararacters you want to allow: ")
FIND = {"(\"[^\\n]*)(a-zA-Z|A-Za-z)([^\\n]*\")": f"\\1\\2{escape_str(WHITELIST_CHARS, False)}\\3",
        "('[^\\n]*)(a-zA-Z|A-Za-z)([^\\n]*')": f"\\1\\2{escape_str(WHITELIST_CHARS, True)}\\3",
         }

ROOT_DIR = os.path.dirname(__file__)
for root, _, files in os.walk(os.path.join(ROOT_DIR, "Il2CppInspector.Common")):
    for file in files:
        path = os.path.join(root, file)
        if file == "Extensions.cs":
            try:
                with open(path, 'r') as f:
                    content = f.read()
            except UnicodeEncodeError:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
            content = re.sub(r"string allowSpecialChars.*\)",
                             f"string allowSpecialChars = \"{escape_str(WHITELIST_CHARS, True)}\")", content)
            print(f"Successfully modified {path}")
            try:
                with open(path, 'w') as f:
                    f.write(content)
            except UnicodeEncodeError:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
        elif os.path.splitext(file)[1] == ".cs":
            try:
                with open(path, 'r') as f:
                    content = f.read()
            except UnicodeEncodeError:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
            for search, replace in FIND.items():
                content = re.sub(search, replace, content)
                if re.findall(search, content):
                    print(f"Successfully modified {path}")
                try:
                    with open(path, 'w') as f:
                        f.write(content)
                except UnicodeEncodeError:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(content)
