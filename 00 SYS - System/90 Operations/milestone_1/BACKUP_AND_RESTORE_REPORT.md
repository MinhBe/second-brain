# BACKUP AND RESTORE REPORT (MILESTONE 1)

## 1. Backup Location & Policy
- **External Backup Root**: `C:\Users\Admin\Documents\Hermes_Backups` (outside Second Brain vault)
- **Active Snapshot**: `C:\Users\Admin\Documents\Hermes_Backups\backup_20260920_193727`
- **Created At**: 20260920_193727

## 2. Protected Runtime Assets
| File Name | Source Path | Size (bytes) | SHA256 Integrity |
|---|---|---|---|
| `config.yaml` | `C:\Users\Admin\AppData\Local\hermes\config.yaml` | 8325 | Verified (85d3427cd6c4e320...) |
| `state.db` | `C:\Users\Admin\AppData\Local\hermes\state.db` | 11599872 | Verified (cb3a27269364d2d9...) |
| `SOUL.md` | `C:\Users\Admin\AppData\Local\hermes\SOUL.md` | 667 | Verified (36c1f5a2e92cd1d0...) |
| `jobs.json` | `C:\Users\Admin\AppData\Local\hermes\cron\jobs.json` | 3360 | Verified (1dc6d96aded7c23d...) |

## 3. Restore Verification Test
- **Restore Staging Directory**: `C:\Users\Admin\AppData\Local\Temp\hermes_restore_test`
- **Hash Verification**: All restored files matched original SHA256 hashes 100%.
- **SQLite Database Integrity Check**: `ok` (PRAGMA integrity_check)

## 4. Second Brain (20.45 GB) Migration Backup Plan
- Prior to migrating any folders in Second Brain, a point-in-time zip/snapshot archive will be created under `C:\Users\Admin\Documents\Hermes_Backups\vault_snapshot_20260920_193727.tar.gz` with file index validation.
- Rollback mechanism: Mapping file `path_mapping.json` will record every source to destination path for zero-loss reversal.
