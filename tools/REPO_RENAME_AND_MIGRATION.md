# Repository Rename and Documentation Migration

## Recommended New Name

```text
linux-engineering-playbook
```

## Why This Name

The old name `Linux_GPU_CUDA` is too narrow for the current content.

The documentation now covers:

- Linux GPU and CUDA
- Proxmox virtualization
- Python engineering
- PostgreSQL integration
- RustDesk audio
- Tor proxy notes
- Linux administration

`linux-engineering-playbook` is broad enough, professional, and still technical.

## Rename with GitHub CLI

Check authentication:

```bash
gh auth status
```

Rename the repository:

```bash
gh repo rename -R Centaurus-X/Linux_GPU_CUDA linux-engineering-playbook --yes
```

Update repository metadata:

```bash
gh repo edit Centaurus-X/linux-engineering-playbook \
  --description "A practical Linux systems engineering playbook for GPU/CUDA, Proxmox, Python environments, services, and administration." \
  --add-topic linux \
  --add-topic ubuntu \
  --add-topic proxmox \
  --add-topic cuda \
  --add-topic nvidia \
  --add-topic python \
  --add-topic postgresql \
  --add-topic systems-engineering \
  --add-topic automation
```

Update local remote URL:

```bash
git remote set-url origin https://github.com/Centaurus-X/linux-engineering-playbook.git
git remote -v
```

## Apply the New Documentation Structure

Copy this package into the repository root, then inspect:

```bash
git status
```

Add and commit:

```bash
git add README.md CHANGELOG.md .gitignore docs scripts tools wiki
git commit -m "Restructure documentation into Linux engineering playbook"
git push origin main
```

## Wiki Migration

Clone the wiki separately:

```bash
git clone https://github.com/Centaurus-X/linux-engineering-playbook.wiki.git linux-engineering-playbook.wiki
```

Replace the wiki `Home.md` with `wiki/Home.md` from this package.

```bash
cp wiki/Home.md ../linux-engineering-playbook.wiki/Home.md
cd ../linux-engineering-playbook.wiki
git add Home.md
git commit -m "Replace wiki with documentation landing page"
git push
```

## Local Directory Rename

The GitHub rename changes the remote repository name, not necessarily your local folder name.

From the parent directory:

```bash
mv Linux_GPU_CUDA linux-engineering-playbook
cd linux-engineering-playbook
git remote set-url origin https://github.com/Centaurus-X/linux-engineering-playbook.git
```

## Verification

```bash
git status
git remote -v
gh repo view Centaurus-X/linux-engineering-playbook --web
```

## Rollback Strategy

If the new name is not desired, rename back:

```bash
gh repo rename -R Centaurus-X/linux-engineering-playbook Linux_GPU_CUDA --yes
git remote set-url origin https://github.com/Centaurus-X/Linux_GPU_CUDA.git
```
