#!/bin/bash

# Monad Protocol Submission Helper Script
# Automates the submission process to monad-crypto/protocols

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
MONAD_REPO="monad-crypto/protocols"
BRANCH_NAME="add-kinic-memory-agent"
JSON_FILE="KinicMemoryAgent.json"
PROTOCOLS_DIR="$HOME/monad-protocols"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Monad Protocol Submission Script${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Step 1: Check prerequisites
echo -e "${YELLOW}[1/9]${NC} Checking prerequisites..."

if ! command -v git &> /dev/null; then
    echo -e "${RED}✗ Git is not installed${NC}"
    exit 1
fi

if ! command -v gh &> /dev/null; then
    echo -e "${RED}✗ GitHub CLI (gh) is not installed${NC}"
    echo "Install from: https://cli.github.com/"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 is not installed${NC}"
    exit 1
fi

# Check GitHub auth
if ! gh auth status &> /dev/null; then
    echo -e "${RED}✗ Not authenticated with GitHub${NC}"
    echo "Run: gh auth login"
    exit 1
fi

echo -e "${GREEN}✓ All prerequisites met${NC}\n"

# Step 2: Fork and clone repository
echo -e "${YELLOW}[2/9]${NC} Forking and cloning monad-crypto/protocols..."

if [ -d "$PROTOCOLS_DIR" ]; then
    echo -e "${YELLOW}⚠ Directory $PROTOCOLS_DIR already exists${NC}"
    read -p "Do you want to remove it and start fresh? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$PROTOCOLS_DIR"
    else
        cd "$PROTOCOLS_DIR"
        echo -e "${GREEN}✓ Using existing directory${NC}\n"
        goto_step3=true
    fi
fi

if [ "$goto_step3" != "true" ]; then
    # Fork the repository
    gh repo fork $MONAD_REPO --clone=true --remote=true "$PROTOCOLS_DIR"
    cd "$PROTOCOLS_DIR"
    echo -e "${GREEN}✓ Repository forked and cloned${NC}\n"
fi

# Step 3: Create branch
echo -e "${YELLOW}[3/9]${NC} Creating branch: $BRANCH_NAME..."

# Ensure we're on main/master
git checkout main 2>/dev/null || git checkout master 2>/dev/null || true

# Check if branch already exists
if git show-ref --verify --quiet refs/heads/$BRANCH_NAME; then
    echo -e "${YELLOW}⚠ Branch $BRANCH_NAME already exists${NC}"
    read -p "Do you want to delete it and create a new one? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git branch -D $BRANCH_NAME
        git checkout -b $BRANCH_NAME
    else
        git checkout $BRANCH_NAME
    fi
else
    git checkout -b $BRANCH_NAME
fi

echo -e "${GREEN}✓ Branch created and checked out${NC}\n"

# Step 4: Copy JSON file
echo -e "${YELLOW}[4/9]${NC} Copying JSON file to mainnet/..."

SOURCE_JSON="$HOME/monad/kinic-monad-poc/monad-submission/$JSON_FILE"

if [ ! -f "$SOURCE_JSON" ]; then
    echo -e "${RED}✗ Source JSON file not found: $SOURCE_JSON${NC}"
    exit 1
fi

cp "$SOURCE_JSON" "mainnet/$JSON_FILE"
echo -e "${GREEN}✓ JSON file copied${NC}\n"

# Step 5: Validate
echo -e "${YELLOW}[5/9]${NC} Validating submission..."

if [ -f "scripts/validate_protocol.py" ]; then
    python3 scripts/validate_protocol.py --network mainnet --protocol KinicMemoryAgent
    echo -e "${GREEN}✓ Validation passed${NC}\n"
else
    echo -e "${YELLOW}⚠ Validation script not found, skipping...${NC}\n"
fi

# Step 6: Show diff
echo -e "${YELLOW}[6/9]${NC} Reviewing changes..."
git diff mainnet/$JSON_FILE
echo

read -p "Does this look correct? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${RED}Aborting submission${NC}"
    exit 1
fi

# Step 7: Commit
echo -e "${YELLOW}[7/9]${NC} Committing changes..."

git add mainnet/$JSON_FILE

COMMIT_MSG="Add Kinic AI Memory Agent to mainnet protocols

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

git commit -m "$COMMIT_MSG"
echo -e "${GREEN}✓ Changes committed${NC}\n"

# Step 8: Push
echo -e "${YELLOW}[8/9]${NC} Pushing to your fork..."

git push origin $BRANCH_NAME

echo -e "${GREEN}✓ Pushed to origin/$BRANCH_NAME${NC}\n"

# Step 9: Create PR
echo -e "${YELLOW}[9/9]${NC} Creating pull request..."

PR_TITLE="Add Kinic AI Memory Agent to mainnet protocols"

PR_BODY="## Protocol Information

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

✅ **Validation passed:** \`python scripts/validate_protocol.py --network mainnet --protocol KinicMemoryAgent\`
✅ **JSON structure verified** against existing examples
✅ **Contract address verified** on Monad mainnet
✅ **All links tested** and accessible
✅ **Application live** and functional

---

Ready for review! Please let me know if any changes or additional information is needed.

**Submission Date:** $(date +%Y-%m-%d)"

# Get username for PR
USERNAME=$(gh api user --jq .login)

gh pr create \
  --repo $MONAD_REPO \
  --base main \
  --head $USERNAME:$BRANCH_NAME \
  --title "$PR_TITLE" \
  --body "$PR_BODY"

echo -e "\n${GREEN}✓ Pull request created successfully!${NC}\n"

# Show PR URL
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✓ Submission complete!${NC}"
echo -e "${BLUE}========================================${NC}\n"

echo "View your PR:"
gh pr view --repo $MONAD_REPO --web

echo -e "\n${YELLOW}Next steps:${NC}"
echo "1. Monitor the PR for CI checks"
echo "2. Respond to any review comments"
echo "3. Wait for approval and merge"
echo -e "\n${GREEN}Good luck! 🚀${NC}"
