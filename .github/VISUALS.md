# Profile visuals maintenance

The README uses four SVGs committed in `assets/`. This keeps the initial profile and PR preview functional without an external statistics service or an uninitialized `output` branch.

`Update GitHub Visuals` generates and validates both 3D calendars and both snakes together. Pull requests and branch pushes validate and retain a downloadable artifact; only successful runs on the default branch can commit the four image files. A failed generator or validation step leaves the previous images intact. No force push is used, and unchanged images do not create a commit.

The daily schedule is **06:17 UTC / 03:17 São Paulo**. After merging, the default-branch push also generates a fresh set. To refresh manually, open **Actions → Update GitHub Visuals → Run workflow** on the default branch. GitHub may delay scheduled runs and disables schedules in public repositories after 60 days without repository activity.

Without an optional secret, the generators use the built-in `GITHUB_TOKEN` and continue to work with public activity. Only the publishing job requests `contents: write`, and it always uses the built-in token. If repository rules block direct bot commits to the default branch, allow that update through the repository's approved policy before expecting automatic refreshes; the committed images remain usable. Workflows from fork PRs may require a maintainer's approval before running.

The target username is explicitly `FilipeAndrade`, so fork validation does not accidentally substitute the fork owner's activity. Activity from `FilipeDsAndrade` is not combined with this profile.

## Include private contributions (optional)

1. While signed in as **FilipeAndrade**, create a fine-grained personal access token with an expiration. Choose the owner of the private repositories and **Only select repositories** for the repositories you want to include. Grant read-only access to **Contents**, **Issues**, and **Pull requests**; **Metadata** read access is included. No write or administration permissions are needed for generation.
2. If an organization owns those repositories, follow its token policy and obtain any required approval. A fine-grained token is limited to one resource owner; it does not automatically include private repositories from every organization or another GitHub account. Only data accessible to the token can be counted.
3. In **FilipeAndrade/FilipeAndrade → Settings → Secrets and variables → Actions**, create a repository secret named **`PROFILE_READ_TOKEN`** containing that token. Do not paste it into the README, a PR, or chat.
4. Merge the workflow change, then run **Actions → Update GitHub Visuals → Run workflow** on **main**. Check that generation and publishing both pass. Private-data coverage can only be verified after the secret is configured and the organization has approved access, if required.

The private token is supplied only to the two pinned generators, only in the original repository, and only for non-PR runs on the default branch. Forks, PRs, and other branches always use the built-in token. Checkout and publication never use the personal token. If the secret is missing, public generation remains available. If a configured token expires or an API call is denied, generation fails and preserves the last published images; renew or remove the secret before retrying.

The generated SVGs are public: opting in exposes aggregate contribution counts and activity dates, including the radar's totals, but these four images do not display private repository names or source code. For calendar counts without granting repository access, GitHub also offers **Profile → Contribution settings → Private contributions**; that does not provide the same private detail to the radar.

The workflow still runs in this **public** profile repository on the standard **ubuntu-latest** runner. Its execution is free and does not draw from paid/included Actions compute merely because the token reads private repositories. Profile page views only load committed SVGs and do not trigger a workflow.

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
- [Create and scope a personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
- [GraphQL authentication and permissions](https://docs.github.com/en/graphql/guides/forming-calls-with-graphql)
- [Private contribution visibility](https://docs.github.com/en/account-and-profile/how-tos/contribution-settings/manage-visibility-settings-for-private-contributions-and-achievements)
- [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions)
