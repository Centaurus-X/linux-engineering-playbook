# pip on Ubuntu Server 22.04

## Scope

This guide installs and validates `pip` for Python on Ubuntu Server 22.04.

## Recommended Method

Ubuntu usually provides pip through packages:

```bash
sudo apt update
sudo apt install -y python3-pip python3-venv
python3 -m pip --version
```

## Alternative: get-pip.py

Use this only when the package-based method is not sufficient.

```bash
cd /tmp
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user
```

Add local Python binaries to PATH:

```bash
cat <<'EOF' >> ~/.bashrc

# User Python binaries
export PATH="$HOME/.local/bin:$PATH"
EOF

source ~/.bashrc
```

Validate:

```bash
python3 --version
python3 -m pip --version
```

## Notes

Prefer:

```bash
python3 -m pip install <package>
```

over:

```bash
pip install <package>
```

This avoids ambiguity when multiple Python versions are installed.

## Troubleshooting

### pip Command Not Found

```bash
python3 -m ensurepip --upgrade || true
python3 -m pip --version
```

If `ensurepip` is disabled by the distribution package layout, install `python3-pip` via `apt`.
