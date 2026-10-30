# Profile visuals maintenance

The README uses four SVGs committed in `assets/`. This keeps the initial profile and PR preview functional without an external statistics service or an uninitialized `output` branch.

`Update GitHub Visuals` generates and validates both 3D calendars and both snakes together. Pull requests and branch pushes validate and retain a downloadable artifact; only successful runs on the default branch can commit the four image files. A failed generator or validation step leaves the previous images intact. No force push is used, and unchanged images do not create a commit.

The daily schedule is **06:17 UTC / 03:17 São Paulo**. After merging, the default-branch push also generates a fresh set. To refresh manually, open **Actions → Update GitHub Visuals → Run workflow** on the default branch. GitHub may delay scheduled runs and disables schedules in public repositories after 60 days without repository activity.

No personal token or custom secret is required: the generators use the built-in `GITHUB_TOKEN`. Only the publishing job requests `contents: write`. If repository rules block direct bot commits to the default branch, allow that update through the repository's approved policy before expecting automatic refreshes; the committed images remain usable. Workflows from fork PRs may require a maintainer's approval before running.

The target username is explicitly `FilipeAndrade`, so fork validation does not accidentally substitute the fork owner's activity. Contributions reflect what GitHub exposes for that profile; the workflow does not request private-repository access.

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
