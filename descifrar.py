import argparse
import getpass
import os
import subprocess
import sys
from pathlib import Path


def get_password():
    return getpass.getpass("Password: ")


def decrypt_file(path: Path, password: str, delete_enc: bool):
    if not path.suffix.endswith(".enc"):
        print(f"Skipping (not .enc): {path}")
        return
    out = path.with_suffix(path.suffix[: -len(".enc")])
    cmd = [
        "openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2",
        "-pass", f"pass:{password}",
        "-in", str(path),
        "-out", str(out),
    ]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        if out.exists():
            out.unlink()
        print(f"Failed to decrypt: {path} (wrong password or corrupt file)", file=sys.stderr)
        sys.exit(1)
    print(f"Decrypted: {path} -> {out}")
    if delete_enc:
        path.unlink()


def main():
    parser = argparse.ArgumentParser(description="Decrypt OpenSSL AES-256-CBC .enc files in a folder.")
    parser.add_argument("folder", help="Folder containing the .enc files to decrypt")
    parser.add_argument("-d", "--delete", action="store_true", help="Delete the .enc files after decryption")
    parser.add_argument("-p", "--password", help="Password (if omitted, you will be prompted)")
    args = parser.parse_args()

    folder = Path(args.folder)
    if not folder.is_dir():
        print(f"Not a folder: {folder}", file=sys.stderr)
        sys.exit(1)

    password = args.password if args.password else get_password()

    enc_files = [p for p in folder.iterdir() if p.is_file() and p.suffix.endswith(".enc")]
    if not enc_files:
        print("No .enc files found.")
        return

    for path in sorted(enc_files):
        decrypt_file(path, password, args.delete)


if __name__ == "__main__":
    main()
