# Profile visuals maintenance

The README uses four SVGs committed in `assets/`. This keeps the initial profile and PR preview functional without an external statistics service or an uninitialized `output` branch.

`Update GitHub Visuals` generates and validates both 3D calendars and both snakes together. Pull requests and branch pushes validate and retain a downloadable artifact; only successful runs on the default branch can commit the four image files. A failed generator or validation step leaves the previous images intact. No force push is used, and unchanged images do not create a commit.

The daily schedule is **06:17 UTC / 03:17 São Paulo**. After merging, the default-branch push also generates a fresh set. To refresh manually, open **Actions → Update GitHub Visuals → Run workflow** on the default branch. GitHub may delay scheduled runs and disables schedules in public repositories after 60 days without repository activity.

The generators use only the built-in `GITHUB_TOKEN`. No personal access token or custom secret is used. Only the publishing job requests `contents: write`, and it also uses the built-in token. If repository rules block direct bot commits to the default branch, allow that update through the repository's approved policy before expecting automatic refreshes; the committed images remain usable. Workflows from fork PRs may require a maintainer's approval before running.

The target username is explicitly `FilipeAndrade`, so fork validation does not accidentally substitute the fork owner's activity. Activity from `FilipeDsAndrade` is not combined with this profile.

## Access and security boundaries

The dashboard reads activity GitHub exposes for the profile. It does not request access to other private repositories. If the account owner already shares anonymized private contribution counts through GitHub's profile settings, the calendar can reflect those published counts without accessing the private repositories themselves. This workflow does not change that setting.

GitHub creates a separate short-lived token for each job, scoped to this repository. The generators run with read-only repository permissions, and checkout does not persist credentials in that job. Publication runs in a separate job on the default branch, never for PR events. Its write permission covers this profile repository; the commit step stages only the four expected SVGs.

The two generators remain third-party code running inside GitHub Actions. Full commit pins and limited permissions reduce supply-chain risk but do not prove that a dependency is free of vulnerabilities. The SVG validator checks output correctness and some unsafe elements; it is not a security sandbox or a comprehensive SVG sanitizer. Review changes to action pins, workflow code, and repository access before merging.

The workflow runs in this **public** profile repository on the standard **ubuntu-latest** runner. Its execution is free and does not draw from paid/included Actions compute. Profile page views only load committed SVGs and do not trigger a workflow.

The light 3D calendar uses Southern Hemisphere seasons. Dark-mode images are selected with `<picture>`. SVGs contain native animation and need no JavaScript in the README.

Local validation (Python 3):

```sh
python scripts/validate_visuals.py
```

Action versions are pinned to complete commit hashes. When upgrading, check the corresponding release and validate the generated images again.

## Upstream references

- [3D calendar generator](https://github.com/yoshi389111/github-profile-3d-contrib/tree/v0.9.3)
- [Snake generator](https://github.com/Platane/snk/tree/v3.5.0)
- [GitHub workflow events and schedule behavior](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)
- [GitHub token permissions](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token)
- [Automatic token scope and lifetime](https://docs.github.com/en/actions/concepts/security/github_token)
- [GitHub Actions security guidance](https://docs.github.com/en/actions/reference/security/secure-use)
- [Private contribution visibility](https://docs.github.com/en/account-and-profile/how-tos/contribution-settings/manage-visibility-settings-for-private-contributions-and-achievements)
- [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions)
