# Google Drive storage organisation — 25 October 2026

## Reporting significance

The connected Google Drive now separates **pre-existing material** from **new investigative-journalism work**. The purpose is to prevent new large data collections and evidence packages from disappearing into an undifferentiated personal archive. This is an organisational boundary, not a claim that older files are personal rather than professional: earlier reporting work remains inside the `personal` archive by explicit instruction.

## Verified structure

```
My Drive/
  personal/                 Existing top-level files and folders, moved in place
  work/
    journalism/             Empty, reserved for new journalism work
```

After the operation, a fresh Google Drive root listing returned exactly two items: `personal` and `work`. The `work` listing contained exactly `journalism`, and `journalism` returned zero items. The `personal` listing reached the provider's 1,000-item display limit, so the exact total should not be inferred from that limited listing alone.

## What changed

- Created the three requested folders and moved all pre-existing root-level files and directories into `personal`.
- Used Google Drive's **parent update** operation: no copy-and-delete, rename, byte replacement, deletion, or deliberate sharing-permission edit.
- Kept pre-existing nested folders intact, rather than reorganising their contents.
- Every returned move response reported success with `personal` as the new parent; all subsequent root-level listings show no leftover unrelated items.
- Shared-file links retain their file identifiers. However, inherited folder permissions and external collaborators' practical access were not independently checked item by item.

## Future default

New research archives, source documents and derived datasets should go under `work/journalism`. Store prose reports, reproducible scripts and safe evidence manifests in GitHub. Avoid copying private Drive object links, confidential source identities or privileged materials into this public repository.

**Scope limits:** This was a top-level organisation operation, not a comprehensive data inventory, privacy audit, deduplication, quota evaluation or automated backup. Google Drive synchronisation does not substitute for an independent backup. Do not delete originals until recoverability and checksums have been verified.

For size and retention guidance, see [repository audit](repository-audit-2026-10-25.md).
