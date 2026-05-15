---
name: gh-cli
description: Use GitHub CLI for repositories, issues, pull requests, Actions, releases, checks, and safe GitHub operations.
---

# GitHub CLI (gh)

Comprehensive reference for GitHub CLI (gh) - work seamlessly with GitHub from the command line.

**Version:** 2.85.0 (current as of January 2026)

## Prerequisites

### Installation

```bash
# macOS
brew install gh

# Linux
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# Windows
winget install --id GitHub.cli

# Verify installation
gh --version
```

### Authentication

```bash
# Interactive login (default: github.com)
gh auth login

# Login with specific hostname
gh auth login --hostname enterprise.internal

# Check authentication status
gh auth status

# Switch accounts
gh auth switch --hostname github.com --user username

# Logout
gh auth logout --hostname github.com --user username
```

### Setup Git Integration

```bash
# Configure git to use gh as credential helper
gh auth setup-git

# Refresh authentication scopes
gh auth refresh --scopes write:org,read:public_key
```

## CLI Structure

```
gh
├── auth          # Authentication
├── browse        # Open in browser
├── codespace     # GitHub Codespaces
├── gist          # Gists
├── issue         # Issues
├── org           # Organizations
├── pr            # Pull Requests
├── project       # Projects v2
├── release       # Releases
├── repo          # Repositories
├── cache         # Actions caches
├── run           # Workflow runs
├── workflow      # Workflows
├── secret        # Secrets
├── variable      # Variables
├── search        # Search
├── label         # Labels
├── ssh-key       # SSH keys
├── gpg-key       # GPG keys
├── status        # GitHub status
├── config        # Configuration
├── extension     # Extensions
├── alias         # Aliases
├── api           # API access
├── ruleset       # Rulesets
├── attestation   # Attestations
└── completion    # Shell completion
```

## gh auth

```bash
gh auth login                              # Interactive login
gh auth login --hostname enterprise.local  # Enterprise login
gh auth logout                             # Logout
gh auth status                             # Check status
gh auth switch --user username             # Switch account
gh auth refresh --scopes write:packages    # Add scopes
gh auth setup-git                          # Configure git credential helper
```

## gh browse

```bash
gh browse                    # Open repo in browser
gh browse --repo owner/repo  # Open specific repo
gh browse 123                # Open issue/PR #123
gh browse --branch main      # Open branch
gh browse --commit abc123    # Open specific commit
gh browse --projects         # Open projects tab
gh browse --releases         # Open releases tab
gh browse --settings         # Open settings
gh browse --wiki             # Open wiki
```

## gh repo

```bash
# Create
gh repo create myrepo --public
gh repo create myrepo --private --description "My repo"
gh repo create myrepo --clone
gh repo create --template owner/template-repo

# Clone
gh repo clone owner/repo
gh repo clone owner/repo -- --depth 1

# View
gh repo view
gh repo view owner/repo
gh repo view owner/repo --web

# Edit
gh repo edit --description "New description"
gh repo edit --visibility private
gh repo edit --default-branch main
gh repo edit --enable-issues --enable-wiki

# Fork
gh repo fork owner/repo
gh repo fork owner/repo --clone
gh repo fork owner/repo --remote

# Sync (fork with upstream)
gh repo sync                    # Sync current fork
gh repo sync owner/repo         # Sync specific fork
gh repo sync --branch main      # Sync specific branch

# List
gh repo list                    # Your repos
gh repo list org-name           # Org repos
gh repo list --limit 100        # More results
gh repo list --language go      # Filter by language
gh repo list --topic kubernetes # Filter by topic

# Other
gh repo set-default owner/repo  # Set default repo for gh commands
gh repo archive owner/repo      # Archive repo
gh repo delete owner/repo       # Delete repo (requires confirmation)
gh repo rename new-name         # Rename repo
```

## gh issue

```bash
# Create
gh issue create --title "Bug title" --body "Description"
gh issue create --title "Bug" --label bug --assignee @me
gh issue create --template bug_report.md

# List
gh issue list
gh issue list --state open
gh issue list --state closed
gh issue list --assignee @me
gh issue list --label "bug,enhancement"
gh issue list --milestone "v1.0"
gh issue list --limit 50

# View
gh issue view 123
gh issue view 123 --web
gh issue view 123 --comments

# Edit
gh issue edit 123 --title "New title"
gh issue edit 123 --add-label bug --remove-label enhancement
gh issue edit 123 --add-assignee @me --remove-assignee other
gh issue edit 123 --milestone "v2.0"

# Close/Reopen
gh issue close 123
gh issue close 123 --comment "Fixed in #456"
gh issue reopen 123

# Comment
gh issue comment 123 --body "My comment"
gh issue comment 123 --edit-last  # Edit last comment

# Status
gh issue status

# Other
gh issue pin 123
gh issue lock 123 --reason spam
gh issue transfer 123 owner/other-repo
gh issue delete 123
gh issue develop 123 --name feature-branch  # Create branch linked to issue
```

## gh pr

```bash
# Create
gh pr create --title "Feature" --body "Description"
gh pr create --base main --head feature-branch
gh pr create --draft
gh pr create --reviewer user1,user2
gh pr create --label enhancement
gh pr create --fill  # Use commit info for title/body
gh pr create --web   # Open browser to create

# List
gh pr list
gh pr list --state open
gh pr list --state closed
gh pr list --state merged
gh pr list --author @me
gh pr list --assignee @me
gh pr list --reviewer @me
gh pr list --label "needs-review"
gh pr list --base main

# View
gh pr view
gh pr view 123
gh pr view 123 --web
gh pr view 123 --comments

# Checkout
gh pr checkout 123
gh pr checkout 123 --branch local-name

# Diff
gh pr diff 123
gh pr diff 123 --name-only

# Merge
gh pr merge 123
gh pr merge 123 --merge      # Merge commit
gh pr merge 123 --squash     # Squash and merge
gh pr merge 123 --rebase     # Rebase and merge
gh pr merge 123 --auto       # Enable auto-merge
gh pr merge 123 --delete-branch

# Edit
gh pr edit 123 --title "New title"
gh pr edit 123 --add-reviewer user1
gh pr edit 123 --add-label bug
gh pr edit 123 --base main

# Review
gh pr review 123 --approve
gh pr review 123 --request-changes --body "Please fix X"
gh pr review 123 --comment --body "Looks good overall"

# Comment
gh pr comment 123 --body "LGTM"

# Status
gh pr status

# Other
gh pr checks 123          # Show CI checks
gh pr checks 123 --watch  # Wait for checks to complete
gh pr ready 123           # Mark as ready for review
gh pr close 123
gh pr reopen 123
gh pr update-branch 123   # Update with base branch
gh pr revert 123          # Revert merged PR
gh pr lock 123 --reason off-topic
```

## gh run (GitHub Actions)

```bash
# List
gh run list
gh run list --workflow ci.yml
gh run list --branch main
gh run list --status failure
gh run list --limit 20

# View
gh run view 12345678
gh run view 12345678 --log
gh run view 12345678 --log-failed  # Show only failed step logs

# Watch
gh run watch 12345678        # Watch run progress
gh run watch --exit-status   # Exit with run's exit code

# Rerun
gh run rerun 12345678
gh run rerun 12345678 --failed  # Rerun failed jobs only
gh run rerun 12345678 --job JOB_ID

# Cancel/Delete
gh run cancel 12345678
gh run delete 12345678

# Download artifacts
gh run download 12345678
gh run download 12345678 --name artifact-name --dir ./artifacts
```

## gh workflow

```bash
gh workflow list                          # List workflows
gh workflow view ci.yml                   # View workflow
gh workflow run ci.yml                    # Trigger workflow
gh workflow run ci.yml --ref feature      # Trigger on branch
gh workflow run ci.yml -f key=value       # With inputs
gh workflow enable ci.yml
gh workflow disable ci.yml
```

## gh secret / gh variable

```bash
# Secrets
gh secret list
gh secret set SECRET_NAME --body "value"
gh secret set SECRET_NAME < secret.txt
gh secret set SECRET_NAME --env production  # Environment secret
gh secret set SECRET_NAME --org myorg       # Org secret
gh secret delete SECRET_NAME

# Variables
gh variable list
gh variable set VAR_NAME --body "value"
gh variable set VAR_NAME --env production
gh variable delete VAR_NAME
```

## gh project (Projects v2)

```bash
gh project list
gh project list --owner @me
gh project list --owner org-name

gh project view 1
gh project view 1 --owner org-name

gh project create --title "My Project"
gh project edit 1 --title "New Title"
gh project close 1
gh project delete 1

# Items
gh project item-list 1
gh project item-add 1 --url https://github.com/owner/repo/issues/123
gh project item-create 1 --title "New item"
gh project item-edit --id ITEM_ID --field-id FIELD_ID --text "value"
gh project item-archive --id ITEM_ID
gh project item-delete --id ITEM_ID

# Fields
gh project field-list 1
gh project field-create 1 --name "Priority" --data-type SINGLE_SELECT
gh project field-delete --id FIELD_ID
```

## gh release

```bash
# Create
gh release create v1.0.0
gh release create v1.0.0 --title "Version 1.0"
gh release create v1.0.0 --notes "Release notes"
gh release create v1.0.0 --notes-file CHANGELOG.md
gh release create v1.0.0 --draft
gh release create v1.0.0 --prerelease
gh release create v1.0.0 ./dist/*.tar.gz  # Upload assets

# List/View
gh release list
gh release view v1.0.0

# Edit
gh release edit v1.0.0 --title "New title"
gh release edit v1.0.0 --draft=false

# Upload assets
gh release upload v1.0.0 ./dist/binary.tar.gz

# Download
gh release download v1.0.0
gh release download v1.0.0 --asset binary.tar.gz --dir ./downloads
gh release download --pattern "*.tar.gz"

# Delete
gh release delete v1.0.0
gh release delete-asset v1.0.0 binary.tar.gz
```

## gh gist

```bash
gh gist create file.txt
gh gist create file.txt --public
gh gist create file.txt --desc "Description"
gh gist create - <<< "content"  # From stdin

gh gist list
gh gist view GIST_ID
gh gist view GIST_ID --raw

gh gist edit GIST_ID
gh gist rename GIST_ID old-name.txt new-name.txt
gh gist delete GIST_ID
gh gist clone GIST_ID
```

## gh search

```bash
gh search repos "language:go topic:kubernetes"
gh search repos "owner:myorg stars:>100"

gh search issues "bug label:confirmed"
gh search issues "author:username state:open"
gh search issues "repo:owner/repo milestone:v1.0"

gh search prs "review:required"
gh search prs "author:@me draft:false"

gh search commits "message:fix bug repo:owner/repo"
gh search code "filename:main.go repo:owner/repo"
```

## gh api (REST + GraphQL)

```bash
# REST
gh api /repos/owner/repo
gh api /repos/owner/repo/issues --method POST --field title="Bug" --field body="Description"
gh api /user/repos --paginate
gh api --method PATCH /repos/owner/repo --field has_issues=true

# GraphQL
gh api graphql -f query='{ viewer { login } }'
gh api graphql --field query=@query.graphql

# Pagination
gh api /repos/owner/repo/issues --paginate
gh api /repos/owner/repo/issues --paginate --jq '.[].title'

# JSON output
gh api /repos/owner/repo --jq '.stargazers_count'
```

## Output Formatting

```bash
# JSON output for scripting
gh issue list --json number,title,state
gh pr list --json number,title,headRefName,state
gh repo list --json name,url,isPrivate

# jq filtering
gh issue list --json number,title --jq '.[] | select(.title | contains("bug"))'
gh pr list --json number,title,state --jq '.[] | [.number, .title] | @tsv'

# Template formatting
gh issue list --template '{{range .}}{{.number}}: {{.title}}{{"\\n"}}{{end}}'

# Table output
gh issue list --limit 20  # Default table format
```

## Common Workflows

### Create PR from issue

```bash
# Create branch linked to issue
gh issue develop 123 --name fix-bug-123

# Work on it, then create PR
gh pr create --title "Fix: bug description" --body "Closes #123"
```

### Bulk operations

```bash
# Close all issues with a label
gh issue list --label stale --json number --jq '.[].number' | \
  xargs -I {} gh issue close {} --comment "Closing stale issue"

# List all open PRs as TSV
gh pr list --json number,title,author --jq '.[] | [.number, .title, .author.login] | @tsv'
```

### Repository setup

```bash
# Create repo, clone, and set default
gh repo create myproject --public --clone
cd myproject
gh repo set-default

# Fork and clone
gh repo fork owner/repo --clone
```

### Monitor CI

```bash
# Create PR and wait for checks
gh pr create --fill
gh pr checks --watch

# Watch workflow run
gh run watch $(gh run list --limit 1 --json databaseId --jq '.[0].databaseId')
```

### Fork sync

```bash
# Keep fork up to date
gh repo sync --branch main
```

## Best Practices

- Prefer `gh` over browser for all GitHub operations — faster and scriptable
- Use `--json` for scripting, default table output for human reading
- Use `--web` to quickly open any resource in browser
- Set `GH_REPO=owner/repo` to avoid repeating `--repo` in scripts
- Use `gh api` for operations not covered by top-level commands
- Use `gh pr checks --watch` in CI workflows to block until checks complete

## Environment Variables

```bash
GH_HOST           # Default GitHub host
GH_REPO           # Default repo (owner/repo format)
NO_COLOR          # Disable color output
GH_NO_UPDATE_NOTIFIER  # Disable update notifications
```

## Configuration

```bash
gh config set editor vim
gh config set git_protocol ssh
gh config set browser firefox
gh config set prompt enabled
gh config list
gh config get editor
```

## Extensions

```bash
gh extension list                        # List installed
gh extension install owner/gh-extension  # Install
gh extension upgrade --all               # Update all
gh extension remove gh-extension         # Remove
gh extension search "keyword"            # Find extensions
```

## Aliases

```bash
gh alias set prc 'pr create --fill'
gh alias set prl 'pr list --author @me'
gh alias list
gh alias delete prc
```
