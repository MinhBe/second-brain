# SKILL AUDIT REPORT (MILESTONE 1)

## 1. Executive Summary
- **Skills in Second Brain (`Collection\SKILL`)**: 2374
- **Skills in Hermes Local (`AppData\Local\hermes\skills`)**: 1192
- **Total Catalog Entries Analyzed**: 3566
- **Unique Content Hashes (SHA256)**: 2371
- **Unique Skill Names**: 1958
- **Exact Duplicate Clusters**: 1192 groups (identical `SKILL.md` content in multiple locations)
- **Name Collision Clusters**: 376 groups (same name, differing implementations)

## 2. Collision & Overlap Findings
- **Overlap Ratio**: Second Brain contains 2,374 skills, while Hermes Local contains 1,192 skills. Nearly 1,000 skills in Hermes Local are exact duplicates of skills in Second Brain.
- **Top Name Collisions**:
- **`windows-chrome-automation`**: 2 variants across hermes_local, second_brain
- **`baoyu-infographic`**: 3 variants across hermes_local, second_brain
- **`humanizer`**: 4 variants across hermes_local, second_brain
- **`design-system`**: 3 variants across second_brain
- **`a11y-audit`**: 2 variants across second_brain
- **`ab-test-setup`**: 2 variants across second_brain
- **`ad-creative`**: 2 variants across second_brain
- **`adversarial-reviewer`**: 2 variants across second_brain
- **`aeo`**: 2 variants across second_brain
- **`agent-designer`**: 2 variants across second_brain
- **`agent-protocol`**: 2 variants across second_brain
- **`agent-workflow-designer`**: 2 variants across second_brain
- **`agenthub`**: 2 variants across second_brain
- **`agile-product-owner`**: 2 variants across second_brain
- **`ai-act-readiness`**: 2 variants across second_brain

## 3. Staging & Remediation Policy (Zero Deletion)
1. **Source of Truth**: Hermes runtime currently loads skills ONLY from `AppData\Local\hermes\skills`.
2. **External Dir Bridge**: In Milestone 2, `skills.external_dirs` can safely point to a staged/curated subset of `Second Brain\Collection\SKILL`.
3. **Registry Maintenance**: No skills will be deleted. Deduplicated aliases will be tracked via `skill_registry.json`.
