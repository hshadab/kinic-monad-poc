# 🚀 Detailed Monad Protocol Submission Steps

**Goal:** Submit your protocol metadata to https://github.com/monad-crypto/protocols

**Time Required:** ~15-20 minutes

**Repository:** monad-crypto/protocols
**Your File:** KinicMemoryAgent.json
**Target Directory:** mainnet/

---

## 📋 **Table of Contents**

1. [Authenticate with GitHub](#step-1-authenticate-with-github)
2. [Fork the Monad Repository](#step-2-fork-the-monad-repository)
3. [Clone Your Fork](#step-3-clone-your-fork)
4. [Add Your JSON File](#step-4-add-your-json-file)
5. [Validate Your Submission](#step-5-validate-your-submission)
6. [Commit Your Changes](#step-6-commit-your-changes)
7. [Push to Your Fork](#step-7-push-to-your-fork)
8. [Create Pull Request](#step-8-create-pull-request)
9. [Monitor and Respond](#step-9-monitor-and-respond)

---

## **Step 1: Authenticate with GitHub**

### 1.1 Check if you're logged in

```bash
gh auth status
```

**Expected Output:**
```
✓ Logged in to github.com as hshadab
✓ Git operations for github.com configured to use https protocol
✓ Token: *******************
```

### 1.2 If not logged in, authenticate

```bash
gh auth login
```

**Follow the prompts:**
- What account do you want to log into? → **GitHub.com**
- What is your preferred protocol for Git operations? → **HTTPS**
- Authenticate Git with your GitHub credentials? → **Yes**
- How would you like to authenticate? → **Login with a web browser**
- Copy the one-time code and press Enter to open browser

---

## **Step 2: Fork the Monad Repository**

### 2.1 Fork using GitHub CLI (Recommended)

```bash
# Fork the repository (creates a copy under your account)
gh repo fork monad-crypto/protocols --clone=true --remote=true

# This will:
# - Create a fork at https://github.com/YOUR_USERNAME/protocols
# - Clone it to your local machine
# - Set up remotes (origin = your fork, upstream = monad-crypto/protocols)
```

**Expected Output:**
```
✓ Created fork YOUR_USERNAME/protocols
Cloning into 'protocols'...
✓ Cloned fork
✓ Added remote upstream
```

### 2.2 Alternative: Fork manually via GitHub UI

If you prefer the web interface:

1. Go to https://github.com/monad-crypto/protocols
2. Click the **"Fork"** button in the top-right
3. Select your account
4. Wait for fork to complete
5. Clone your fork:

```bash
git clone https://github.com/YOUR_USERNAME/protocols.git
cd protocols
git remote add upstream https://github.com/monad-crypto/protocols.git
```

---

## **Step 3: Clone Your Fork**

### 3.1 Navigate to the cloned directory

```bash
# If you used gh repo fork, the repo is already cloned
cd protocols

# Verify you're in the right place
pwd
# Should show: /path/to/protocols
```

### 3.2 Check the repository structure

```bash
ls -la
```

**Expected Structure:**
```
.
├── .github/
├── mainnet/          ← Your JSON goes here
│   ├── Axelar.json
│   ├── LayerZero.json
│   ├── Circle_CCTP.json
│   └── ...
├── testnet/
├── scripts/
│   └── validate_protocol.py
├── README.md
└── ...
```

### 3.3 Verify remotes are set up correctly

```bash
git remote -v
```

**Expected Output:**
```
origin    https://github.com/YOUR_USERNAME/protocols.git (fetch)
origin    https://github.com/YOUR_USERNAME/protocols.git (push)
upstream  https://github.com/monad-crypto/protocols.git (fetch)
upstream  https://github.com/monad-crypto/protocols.git (push)
```

---

## **Step 4: Add Your JSON File**

### 4.1 Create a new branch (IMPORTANT!)

```bash
# Create and switch to a new branch
git checkout -b add-kinic-memory-agent

# Verify you're on the new branch
git branch
# Should show: * add-kinic-memory-agent
```

**Why a new branch?**
- Keeps your main branch clean
- Makes it easy to update your PR if needed
- Standard GitHub workflow

### 4.2 Copy your JSON file

**Option A: Copy from your kinic-monad-poc repo**

```bash
# Copy the JSON file to mainnet directory
cp ~/monad/kinic-monad-poc/monad-submission/KinicMemoryAgent.json mainnet/

# Verify it was copied
ls -lh mainnet/KinicMemoryAgent.json
```

**Option B: Create the file directly**

```bash
# Create the file in mainnet directory
cat > mainnet/KinicMemoryAgent.json << 'EOF'
{
  "name": "Kinic AI Memory Agent",
  "description": "AI-powered memory system combining Kinic/Internet Computer for semantic storage with Monad blockchain for transparent metadata logging and audit trails. Features Claude AI integration for intelligent context-aware responses.",
  "live": true,
  "categories": [
    "Apps::AI",
    "Infra::Storage"
  ],
  "addresses": {
    "KinicMemoryLog": "0xEB5B78Fa81cFEA1a46D46B3a42814F5A68038548"
  },
  "links": {
    "project": "https://kinicmemory.com",
    "github": "https://github.com/hshadab/kinic-monad-poc",
    "docs": "https://github.com/hshadab/kinic-monad-poc/blob/master/README.md"
  }
}
EOF
```

### 4.3 Verify the file content

```bash
# Display the file content
cat mainnet/KinicMemoryAgent.json

# Or use a pretty printer
python3 -m json.tool mainnet/KinicMemoryAgent.json
```

### 4.4 Check file status

```bash
git status
```

**Expected Output:**
```
On branch add-kinic-memory-agent
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        mainnet/KinicMemoryAgent.json

nothing added to commit but untracked files present (use "git add" to track)
```

---

## **Step 5: Validate Your Submission**

### 5.1 Check if Python is available

```bash
python3 --version
# Should show: Python 3.x.x
```

### 5.2 Install dependencies (if needed)

```bash
# Check if validation script has requirements
cat scripts/requirements.txt 2>/dev/null || echo "No requirements file"

# If there's a requirements file, install dependencies
pip3 install -r scripts/requirements.txt
```

### 5.3 Run the validation script

```bash
# Validate your JSON file
python3 scripts/validate_protocol.py --network mainnet --protocol KinicMemoryAgent
```

**Expected Output (Success):**
```
✓ Validating mainnet/KinicMemoryAgent.json
✓ JSON is valid
✓ Required fields present: name, description, live, categories, addresses, links
✓ Contract addresses are valid Ethereum addresses
✓ URLs are valid
✓ All checks passed!
```

**If Validation Fails:**

Common issues and fixes:

1. **Invalid JSON syntax:**
   ```bash
   # Check JSON syntax
   python3 -m json.tool mainnet/KinicMemoryAgent.json
   # Fix any syntax errors shown
   ```

2. **Invalid contract address:**
   ```bash
   # Verify contract address format (must start with 0x and be 42 characters)
   echo "0xEB5B78Fa81cFEA1a46D46B3a42814F5A68038548" | wc -c
   # Should output: 43 (42 chars + newline)
   ```

3. **Missing required fields:**
   - Check that all fields from the example above are present
   - Compare with other files: `cat mainnet/Axelar.json`

### 5.4 Compare with existing examples

```bash
# Look at a similar protocol
cat mainnet/Axelar.json

# List all mainnet protocols
ls -1 mainnet/*.json
```

---

## **Step 6: Commit Your Changes**

### 6.1 Stage your file

```bash
# Add the JSON file to staging area
git add mainnet/KinicMemoryAgent.json

# Verify it's staged
git status
```

**Expected Output:**
```
On branch add-kinic-memory-agent
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        new file:   mainnet/KinicMemoryAgent.json
```

### 6.2 Create a commit

```bash
# Commit with a descriptive message
git commit -m "Add Kinic AI Memory Agent to mainnet protocols

- AI-powered memory system with semantic search
- Integrates Kinic/Internet Computer and Monad blockchain
- Live deployment: https://kinicmemory.com
- Smart contract: 0xEB5B78Fa81cFEA1a46D46B3a42814F5A68038548
- Categories: Apps::AI, Infra::Storage

Features:
- Semantic memory storage and search
- Claude AI integration for intelligent responses
- Rich metadata logging on Monad
- Public audit trail
- Dual-blockchain architecture (IC + Monad)"
```

**Expected Output:**
```
[add-kinic-memory-agent 1a2b3c4] Add Kinic AI Memory Agent to mainnet protocols
 1 file changed, 17 insertions(+)
 create mode 100644 mainnet/KinicMemoryAgent.json
```

### 6.3 Verify the commit

```bash
# View commit details
git log -1 --stat

# View the changes
git show
```

---

## **Step 7: Push to Your Fork**

### 7.1 Push the branch

```bash
# Push your branch to your fork (origin)
git push origin add-kinic-memory-agent
```

**Expected Output:**
```
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 8 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (4/4), 1.2 KiB | 1.2 MiB/s, done.
Total 4 (delta 1), reused 0 (delta 0)
remote: Resolving deltas: 100% (1/1), completed with 1 local object.
remote:
remote: Create a pull request for 'add-kinic-memory-agent' on GitHub by visiting:
remote:      https://github.com/YOUR_USERNAME/protocols/pull/new/add-kinic-memory-agent
remote:
To https://github.com/YOUR_USERNAME/protocols.git
 * [new branch]      add-kinic-memory-agent -> add-kinic-memory-agent
```

**Note:** Copy the URL from the output - you'll use it next!

### 7.2 Verify on GitHub

```bash
# Open your fork in the browser
gh repo view --web
```

You should see a yellow banner at the top:
> **add-kinic-memory-agent had recent pushes** [Compare & pull request]

---

## **Step 8: Create Pull Request**

### 8.1 Create PR using GitHub CLI (Easiest)

```bash
# Create a PR with title and body
gh pr create \
  --repo monad-crypto/protocols \
  --base main \
  --head YOUR_USERNAME:add-kinic-memory-agent \
  --title "Add Kinic AI Memory Agent to mainnet protocols" \
  --body "## Protocol Information

**Name:** Kinic AI Memory Agent
**Category:** Apps::AI, Infra::Storage
**Status:** ✅ Live on Monad Mainnet

---

## Description

AI-powered memory system that combines:
- **Kinic/Internet Computer** for semantic storage with vector embeddings
- **Monad blockchain** for transparent metadata logging and audit trails
- **Claude AI** for intelligent, context-aware responses

---

## Deployment Details

- **Live Application:** https://kinicmemory.com
- **Smart Contract:** \`0xEB5B78Fa81cFEA1a46D46B3a42814F5A68038548\`
- **Deployer Address:** \`0xDA9f4e4C9596a1dA338164FD22895D8C167C6Bd6\`
- **Deployment TX:** \`0xf694177f5f0c2d90674a4167d99b09350ba106cfea316dfee7c38d05ff53a716\`
- **Block Number:** 35971599
- **Network:** Monad Private Mainnet (Chain ID: 143)
- **GitHub Repository:** https://github.com/hshadab/kinic-monad-poc

---

## Features

✅ **Semantic Memory Storage** - Vector-based search using Kinic embedding API
✅ **AI Chat** - Claude Haiku integration with memory context
✅ **Blockchain Logging** - Rich metadata stored on Monad for transparency
✅ **Public Audit Trail** - Human-readable on-chain data
✅ **Dual Architecture** - Internet Computer for data, Monad for metadata

---

## Technical Stack

**Backend:**
- FastAPI (Python)
- ic-py for Internet Computer integration
- web3.py for Monad blockchain
- Anthropic Claude AI

**Storage:**
- Kinic Canister: \`2x5sz-ciaaa-aaaak-apgta-cai\`
- Vector embeddings via Kinic API

**Smart Contract:**
- Solidity (KinicMemoryLog)
- Stores: titles, summaries, tags, content hashes, timestamps

---

## Validation

✅ **Validation passed:**
\`\`\`bash
python scripts/validate_protocol.py --network mainnet --protocol KinicMemoryAgent
\`\`\`

✅ **JSON structure verified** against Axelar.json and LayerZero.json examples
✅ **Contract address verified** on Monad mainnet
✅ **All links tested** and accessible
✅ **Application live** and functional

---

## Additional Information

**Documentation:** Full architecture and deployment guides available in the GitHub repository
**API Endpoints:** /insert, /search, /chat, /stats, /health
**Security:** CORS hardening, API key authentication available

Ready for review! Please let me know if any changes or additional information is needed.

---

**Submission Date:** $(date +%Y-%m-%d)
**Contact:** Available via GitHub (@hshadab)"
```

### 8.2 Alternative: Create PR via Web UI

If you prefer the web interface:

1. **Go to the URL from the push output** (or click the banner on your fork page)

2. **Fill in the PR form:**

   **Title:**
   ```
   Add Kinic AI Memory Agent to mainnet protocols
   ```

   **Description:** (Use the markdown from above in section 8.1)

3. **Create the PR:**
   - Click **"Create pull request"**
   - DO NOT click "Create draft pull request"

### 8.3 Verify PR was created

```bash
# List your PRs
gh pr list --repo monad-crypto/protocols --author @me

# View your PR in the browser
gh pr view --repo monad-crypto/protocols --web
```

**Expected Output:**
```
Opening github.com/monad-crypto/protocols/pull/XXX in your browser.
```

---

## **Step 9: Monitor and Respond**

### 9.1 Watch for CI/CD checks

After creating the PR, automated checks may run:

```bash
# Check PR status
gh pr status --repo monad-crypto/protocols

# View PR checks
gh pr checks --repo monad-crypto/protocols PR_NUMBER
```

**Common CI Checks:**
- ✅ JSON validation
- ✅ Contract address verification
- ✅ Link validation
- ✅ File naming conventions

### 9.2 Respond to review comments

If maintainers request changes:

```bash
# Make changes to your file
nano mainnet/KinicMemoryAgent.json

# Commit the changes
git add mainnet/KinicMemoryAgent.json
git commit -m "Address review feedback: update description"

# Push to update the PR
git push origin add-kinic-memory-agent
```

The PR will automatically update!

### 9.3 Enable notifications

```bash
# Watch the repository for updates
gh repo set-default monad-crypto/protocols
gh repo watch

# Or enable GitHub notifications in your settings
```

### 9.4 After PR is merged

Once your PR is approved and merged:

```bash
# Sync your fork with upstream
cd protocols
git checkout main
git pull upstream main
git push origin main

# Delete your feature branch (optional cleanup)
git branch -d add-kinic-memory-agent
git push origin --delete add-kinic-memory-agent

# Celebrate! 🎉
echo "✅ Successfully submitted to Monad protocols repo!"
```

---

## 🆘 **Troubleshooting**

### Issue: "Permission denied" when pushing

**Solution:**
```bash
# Verify you're pushing to your fork
git remote -v
# origin should point to YOUR_USERNAME/protocols

# If not, fix it:
git remote set-url origin https://github.com/YOUR_USERNAME/protocols.git
```

### Issue: "Validation script not found"

**Solution:**
```bash
# Make sure you're in the protocols directory
pwd
# Should show: /path/to/protocols

# Check if script exists
ls -la scripts/validate_protocol.py

# If not, you may need to pull latest changes
git pull upstream main
```

### Issue: "Merge conflicts"

**Solution:**
```bash
# Update your branch with latest changes
git checkout add-kinic-memory-agent
git pull upstream main
# Resolve any conflicts
git commit -m "Merge upstream changes"
git push origin add-kinic-memory-agent
```

### Issue: "Invalid JSON"

**Solution:**
```bash
# Validate JSON syntax
python3 -m json.tool mainnet/KinicMemoryAgent.json

# Common issues:
# - Missing comma between fields
# - Extra comma after last field
# - Unescaped quotes in strings
# - Wrong bracket types
```

### Issue: "PR shows files from other branches"

**Solution:**
```bash
# Make sure you created a branch from latest main
git checkout main
git pull upstream main
git checkout -b add-kinic-memory-agent-v2
git cherry-pick YOUR_COMMIT_HASH
git push origin add-kinic-memory-agent-v2
```

---

## 📞 **Getting Help**

If you encounter issues:

1. **Check existing PRs** for examples:
   ```bash
   gh pr list --repo monad-crypto/protocols --state all --limit 10
   ```

2. **Ask in PR comments** - Tag maintainers if needed

3. **Review closed PRs** for similar submissions

4. **Check Monad Discord/Telegram** for community support

---

## ✅ **Checklist**

Before submitting, verify:

- [ ] GitHub CLI installed and authenticated
- [ ] Repository forked to your account
- [ ] New branch created (not submitting from main)
- [ ] JSON file in correct location (mainnet/KinicMemoryAgent.json)
- [ ] Validation script passes
- [ ] Contract address is correct (0xEB5B78Fa81cFEA1a46D46B3a42814F5A68038548)
- [ ] All links work (test in browser)
- [ ] Application is live and accessible
- [ ] Commit message is descriptive
- [ ] PR title follows convention
- [ ] PR description is complete
- [ ] Ready to respond to review comments

---

## 🎯 **Success Criteria**

Your submission is successful when:

✅ PR is created on monad-crypto/protocols
✅ All CI checks pass (green checkmarks)
✅ Maintainers approve the PR
✅ PR is merged into main branch
✅ Your protocol appears in mainnet/ directory

**After merge:** Your protocol will be listed in the official Monad ecosystem!

---

## 🚀 **Next Steps After Submission**

1. **Monad Momentum Program** - Eligible for Wave 2 (Q4 2025)
2. **Ecosystem Visibility** - Listed in official Monad documentation
3. **Community Engagement** - Connect with other Monad builders
4. **Updates** - Submit PRs to update your protocol info as needed

---

**Good luck with your submission!** 🎉

If you have questions, feel free to ask in the PR or reach out to the Monad team.
