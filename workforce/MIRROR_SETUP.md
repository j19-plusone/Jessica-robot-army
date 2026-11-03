# QCF88888 mirror deployment checklist

Source: `j19-plusone/Jessica-robot-army`  
Mirror: `QCF88888/Jessica-robot-army`

This workflow is staged on the development branch. It **does not execute** until merged to `main`, and it **cannot push** until a cross-repository credential is configured.

1. Ensure the target organization repo exists and has no independent commits.
2. Create a fine-grained GitHub token or GitHub App installation token with **Contents: Read and write** scoped **only** to `QCF88888/Jessica-robot-army`. Store it as source repository Actions secret `QCF_MIRROR_TOKEN`. Never commit credentials.
3. Review and merge this workflow after tests pass.
4. Run **Mirror to QCF88888** using `workflow_dispatch`. Verify `main` SHA and tags match. The workflow does not force-push.
5. Development branches (including `feature/autonomous-workforce-v1`) are deliberately excluded from public automatic mirroring until reviewed and merged.
6. Require PR review and passing tests on source main. On mirror, avoid independent direct commits; send contributions upstream as PRs.
7. If mirror fails because histories diverged, STOP and investigate; do not use `--force` to bypass protections.
8. Check that no customer data, credentials, sensitive health/genetic information or confidential operations are in public history before first run.

GitHub Actions in one repository cannot automatically write to another repository using the default `GITHUB_TOKEN`; a separately scoped credential is required.
