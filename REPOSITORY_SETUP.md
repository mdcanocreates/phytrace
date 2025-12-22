# Repository Setup Completion Guide

**Repository:** `mdcanocreates/phytrace`  
**Version:** v0.1.0  
**Status:** Pre-release setup

---

## ✅ Automated Steps (Already Complete)

- ✅ Community files created locally:
  - `.github/ISSUE_TEMPLATE/config.yml`
  - `.github/ISSUE_TEMPLATE/bug_report.yml`
  - `.github/ISSUE_TEMPLATE/feature_request.yml`
  - `.github/ISSUE_TEMPLATE/question.yml`
  - `CODE_OF_CONDUCT.md`
  - `SECURITY.md`
  - `CONTRIBUTING.md` (updated)
- ✅ All tests passing (28/28)
- ✅ Package builds successfully
- ✅ Files ready to commit

---

## 📋 Manual GitHub UI Steps Required

### Step 1: Push Community Files to GitHub

**Option A: Via Git (Recommended)**
```bash
cd /Users/michael.cano/Desktop/sof.dev/PhySim
git add .github/ISSUE_TEMPLATE/ CODE_OF_CONDUCT.md SECURITY.md CONTRIBUTING.md
git commit -m "chore: add GitHub issue templates and community files"
git push origin main
```

**Option B: Via GitHub Web UI**
1. Navigate to: `https://github.com/mdcanocreates/phytrace`
2. Click "Add file" → "Create new file"
3. For each file:
   - Path: `.github/ISSUE_TEMPLATE/config.yml` (etc.)
   - Paste content from local file
   - Commit directly to `main` branch

---

### Step 2: Update Repository Settings

**URL:** `https://github.com/mdcanocreates/phytrace/settings`

#### 2.1 About Section
1. Scroll to **"About"** section (right sidebar)
2. Click the gear icon (⚙️) to edit
3. Fill in:
   - **Description:** `Audit-ready tracing and evidence generation for scientific simulations in Python`
   - **Website:** (leave empty for now)
   - **Topics:** Add each topic (press Enter after each):
     - `scientific-computing`
     - `reproducibility`
     - `provenance`
     - `scipy`
     - `simulation`
     - `ode`
     - `research`
     - `python`
   - **Uncheck "Releases"** (until v0.1.0 is published)
4. Click **"Save changes"**

#### 2.2 Enable Discussions
1. Scroll to **"Features"** section
2. Find **"Discussions"**
3. Check the box to **"Enable Discussions"**
4. Click **"Set up Discussions"**
5. Use default categories (or customize):
   - **Q&A** - Questions and answers
   - **Ideas** - Feature ideas and suggestions
   - **Show and tell** - Share your work
   - **Announcements** - Project announcements
6. Click **"Start discussions"**

#### 2.3 Branch Protection (Optional but Recommended)
1. Navigate to: `https://github.com/mdcanocreates/phytrace/settings/branches`
2. Click **"Add rule"**
3. Configure:
   - **Branch name pattern:** `main`
   - **Protect matching branches**
   - Check: **"Require status checks to pass before merging"**
   - Check: **"Require branches to be up to date before merging"**
   - Under "Status checks that are required":
     - Select: `test` (if available after first workflow run)
   - Check: **"Require conversation resolution before merging"**
   - Check: **"Include administrators"**
4. Click **"Create"**

---

### Step 3: Create v0.1.0 Release Draft

**URL:** `https://github.com/mdcanocreates/phytrace/releases/new`

#### 3.1 Release Information
1. **Choose a tag:** 
   - Type: `v0.1.0`
   - Select: **"Create new tag: v0.1.0 on publish"**
2. **Target:** Select `main` branch
3. **Release title:** `v0.1.0: Audit-Ready Simulation Tracking`
4. **Description:** Paste the content below (from "Release Notes" section)

#### 3.2 Attach Release Assets
1. Scroll to **"Attach binaries"** section
2. Upload files from `dist/` directory:
   - `phytrace-0.1.0-py3-none-any.whl`
   - `phytrace-0.1.0.tar.gz`
3. Drag and drop or click to browse

#### 3.3 Release Options
1. Check: **"Set as a pre-release"** (for initial feedback period)
2. **DO NOT** click "Publish release" yet
3. Click **"Save draft"**

---

### Step 4: Release Notes Content

Copy and paste this into the release description:

```markdown
## v0.1.0: Audit-Ready Simulation Tracking

**phytrace** is a Python library that adds provenance tracking, invariant checking, and evidence generation to scientific simulations. It's a minimal wrapper around `scipy.integrate.solve_ivp` that makes your simulations audit-ready and reproducible by default.

### What phytrace Does

✅ **Automatic Environment Capture**
- Python version and implementation
- Installed package versions (numpy, scipy, etc.)
- System information (OS, architecture, hostname)
- Git repository state (commit, branch, dirty flag)
- Timestamp of execution

✅ **Runtime Invariant Checking**
- Built-in invariants: `finite()`, `bounded()`, `monotonic()`
- Custom invariants via decorator
- Severity levels: warning, error, critical
- Automatic violation tracking

✅ **Structured Evidence Packs**
- Complete metadata in `manifest.json`
- Trajectory data (CSV, HDF5)
- Publication-ready plots (time series, phase space, solver stats)
- Human-readable markdown report
- Invariant check results

✅ **Deterministic Reproducibility**
- Automatic seed management
- Environment documentation
- Complete parameter capture

### What phytrace Is NOT

❌ **Not a certification tool** - Does not guarantee correctness or compliance  
❌ **Not a real-time system** - Designed for batch simulations  
❌ **Not a formal verification tool** - Runtime checks, not proofs  
❌ **Not a replacement for testing** - Complements, doesn't replace unit tests  
❌ **Not a solver** - Wraps existing solvers, doesn't implement new ones

### Key Features

- **Zero refactoring required** - Wrap your existing ODE functions
- **Minimal overhead** - Lightweight wrapper around scipy
- **Publication-ready** - Evidence packs satisfy audit requirements
- **Reproducible by default** - Seeds and environment captured automatically

### Installation

```bash
pip install phytrace
```

For optional dependencies (pandas, h5py, gitpython):

```bash
pip install phytrace[full]
```

### Quick Start

```python
from phytrace import trace_run
from phytrace.invariants import bounded, finite
import numpy as np

def damped_oscillator(t, y, k, c, m):
    x, v = y
    return [v, -(k/m)*x - (c/m)*v]

result = trace_run(
    simulate=damped_oscillator,
    params={'k': 1.0, 'c': 0.1, 'm': 1.0},
    t_span=(0, 10),
    y0=[1.0, 0.0],
    invariants=[finite(), bounded(-10, 10)],
    evidence_dir='./evidence/run_001'
)
```

### Documentation

- **README:** https://github.com/mdcanocreates/phytrace#readme
- **Examples:** See `examples/` directory
- **API Docs:** Coming soon

### Testing

All tests passing: **28/28** ✅  
Code coverage: **39%** (core modules: 84-96%)

### What's Next (v0.2.0)

- Multi-solver comparison
- Assumption ledger
- Enhanced golden test framework
- Performance optimizations

### Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### License

MIT License - see [LICENSE](LICENSE) file.

---

**Full Changelog:** See [CHANGELOG.md](CHANGELOG.md)
```

---

### Step 5: Verify GitHub Actions

After pushing community files:

1. Navigate to: `https://github.com/mdcanocreates/phytrace/actions`
2. Verify workflows:
   - **test.yml** should run on push
   - **docs.yml** should run on push (if configured)
   - **release.yml** should run on tag push
3. Check for any failures
4. If workflows fail, review logs and fix issues

---

### Step 6: Final Pre-Release Checklist

Before publishing the release, verify:

- [ ] All GitHub Actions workflows passing
- [ ] README renders correctly on GitHub (check main page)
- [ ] Issue templates appear properly:
  - Go to: `https://github.com/mdcanocreates/phytrace/issues/new/choose`
  - Should show: Bug Report, Feature Request, Question
- [ ] Discussions enabled and accessible:
  - Go to: `https://github.com/mdcanocreates/phytrace/discussions`
  - Should show categories
- [ ] Release draft saved:
  - Go to: `https://github.com/mdcanocreates/phytrace/releases`
  - Should see "v0.1.0" as draft
- [ ] Repository About section updated (topics visible on main page)
- [ ] PyPI credentials configured (if publishing to PyPI):
  - Go to: `https://pypi.org/manage/account/`
  - Create API token if needed
  - Add to GitHub Secrets: `https://github.com/mdcanocreates/phytrace/settings/secrets/actions`

---

### Step 7: Publish Release

When ready to publish:

1. Navigate to: `https://github.com/mdcanocreates/phytrace/releases`
2. Click on **"v0.1.0"** draft
3. Click **"Edit"**
4. Review release notes and assets
5. **Uncheck** "Set as a pre-release" (if you're confident)
6. Click **"Publish release"**
7. GitHub will:
   - Create the `v0.1.0` tag automatically
   - Trigger the `release.yml` workflow (if configured)
   - Make the release public

---

### Step 8: Post-Release Verification

After publishing:

1. **Verify tag created:**
   - Go to: `https://github.com/mdcanocreates/phytrace/tags`
   - Should see `v0.1.0` tag

2. **Verify release visible:**
   - Go to: `https://github.com/mdcanocreates/phytrace/releases`
   - Should see v0.1.0 as latest release

3. **Verify workflows:**
   - Check Actions tab for release workflow
   - Verify PyPI upload (if configured)

4. **Update repository About:**
   - Go to Settings → About
   - **Check** "Releases" box (now that v0.1.0 is published)

---

## 🚨 Troubleshooting

### Issue Templates Not Appearing
- Verify files are in `.github/ISSUE_TEMPLATE/` directory
- Check file extensions are `.yml` (not `.yaml`)
- Ensure files are on `main` branch

### Discussions Not Enabled
- Check repository settings → Features
- Ensure you have admin access
- Try refreshing the page

### Release Workflow Fails
- Check PyPI credentials in GitHub Secrets
- Verify `release.yml` workflow file is correct
- Check workflow logs for specific errors

### Tag Not Created
- Ensure you selected "Create new tag on publish"
- Check that you have permission to create tags
- Verify branch protection rules allow tag creation

---

## 📝 Notes

- **Pre-release period:** Keep release as "pre-release" for 1-2 weeks to gather feedback
- **PyPI publishing:** Can be done manually or via GitHub Actions workflow
- **Documentation:** Consider setting up ReadTheDocs after v0.1.0 release
- **Community:** Monitor Discussions and Issues for user feedback

---

## ✅ Completion Checklist

- [ ] Community files pushed to GitHub
- [ ] Repository About section updated
- [ ] Discussions enabled
- [ ] Branch protection configured (optional)
- [ ] Release draft created
- [ ] Release assets attached
- [ ] GitHub Actions verified
- [ ] Pre-release checklist completed
- [ ] Release published
- [ ] Post-release verification done

---

**Last Updated:** 2025-12-20  
**Status:** Ready for manual execution

