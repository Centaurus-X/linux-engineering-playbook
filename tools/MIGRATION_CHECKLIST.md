# Migration Checklist

## Before Rename

- [ ] Confirm that `gh auth status` is logged in to the correct account.
- [ ] Confirm that the repository has no critical external consumers depending on the old name.
- [ ] Backup the main repository.
- [ ] Backup the wiki repository.
- [ ] Confirm that GitHub Pages is not dependent on the old repository URL.

## Rename

- [ ] Rename repository to `linux-engineering-playbook`.
- [ ] Update local `origin` remote.
- [ ] Update repository description.
- [ ] Add repository topics.
- [ ] Confirm old URL redirects.

## Documentation Migration

- [ ] Add `docs/` structure.
- [ ] Add root `README.md`.
- [ ] Add category README files.
- [ ] Move scripts into `scripts/`.
- [ ] Commit migration.
- [ ] Push to `main`.

## Wiki Cleanup

- [ ] Replace Wiki `Home.md` with a landing page.
- [ ] Link to `docs/README.md`.
- [ ] Avoid creating new wiki pages.
- [ ] Keep wiki only as navigation.

## After Migration

- [ ] Open root README on GitHub.
- [ ] Check every relative documentation link.
- [ ] Validate script paths.
- [ ] Review security-sensitive documents.
- [ ] Create first release/tag if desired.
