#!/bin/bash
# Complete setup guide for Kinic Memory Agent on Monad

echo "🚀 Kinic Memory Agent on Monad - Complete Setup Guide"
echo "======================================================"
echo ""
echo "This script will guide you through the complete setup process."
echo ""

# Step 1: Check dependencies
echo "📋 Step 1: Checking dependencies..."
echo ""

dependencies=("python3" "pip" "cargo" "dfx" "git" "curl")
missing_deps=()

for dep in "${dependencies[@]}"; do
    if command -v $dep &> /dev/null; then
        echo "  ✅ $dep"
    else
        echo "  ❌ $dep (missing)"
        missing_deps+=("$dep")
    fi
done

if [ ${#missing_deps[@]} -ne 0 ]; then
    echo ""
    echo "❌ Missing dependencies: ${missing_deps[*]}"
    echo ""
    echo "Install instructions:"
    echo "  - Python: https://www.python.org/downloads/"
    echo "  - Rust/Cargo: https://rustup.rs/"
    echo "  - DFX: https://internetcomputer.org/docs/current/developer-docs/setup/install"
    echo "  - Git: https://git-scm.com/downloads"
    exit 1
fi

echo ""
echo "✅ All dependencies installed!"
echo ""

# Step 2: Python setup
echo "📦 Step 2: Installing Python dependencies..."
pip install -r requirements.txt
echo "✅ Python dependencies installed"
echo ""

# Step 3: Build kinic-cli
echo "🔨 Step 3: Building kinic-cli..."
if [ -d "kinic-cli" ]; then
    echo "⚠️  kinic-cli directory already exists, skipping clone"
else
    git clone -b poc https://github.com/ICME-Lab/kinic-cli.git
fi

cd kinic-cli
cargo build --release
cd ..

if [ -f "kinic-cli/target/release/kinic-cli" ]; then
    echo "✅ kinic-cli built successfully"
else
    echo "❌ Failed to build kinic-cli"
    exit 1
fi
echo ""

# Step 4: IC identity setup
echo "🔑 Step 4: IC Identity Setup"
echo ""
echo "Do you have a DFX identity configured? [y/N]"
read -r has_identity

if [[ ! "$has_identity" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo ""
    echo "Creating new IC identity 'kinic-agent'..."
    dfx identity new kinic-agent || true
    dfx identity use kinic-agent
    echo "✅ Identity created!"
else
    echo ""
    echo "Available identities:"
    dfx identity list
    echo ""
    echo "Enter identity name to use (or press Enter for 'default'):"
    read -r identity_name
    identity_name=${identity_name:-default}
    dfx identity use "$identity_name"
fi

echo ""
echo "Current identity:"
dfx identity whoami
echo "Principal:"
dfx identity get-principal
echo ""

# Step 5: Deploy memory canister
echo "📡 Step 5: Deploy Kinic Memory Canister"
echo ""
echo "Have you already deployed a memory canister? [y/N]"
read -r has_canister

if [[ ! "$has_canister" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo ""
    echo "⚠️  You'll need ICP tokens in your identity to deploy a canister"
    echo "   Check balance and get tokens from: https://faucet.dfinity.org/"
    echo ""
    echo "Enter memory canister name (default: 'monad-agent'):"
    read -r canister_name
    canister_name=${canister_name:-monad-agent}

    echo ""
    echo "Creating memory canister '$canister_name'..."
    echo "This will cost tokens. Continue? [y/N]"
    read -r confirm

    if [[ "$confirm" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        ./kinic-cli/target/release/kinic-cli create \
          --identity "$(dfx identity whoami)" \
          --ic \
          --name "$canister_name" \
          --description "Monad memory agent"
        echo ""
        echo "✅ Memory canister created!"
        echo "   Copy the canister ID shown above for the next step"
    else
        echo "Skipping canister creation"
    fi
else
    echo "Skipping canister creation"
fi
echo ""

# Step 6: Monad setup
echo "⛓️  Step 6: Monad Blockchain Setup"
echo ""
echo "Do you have a Monad testnet wallet with tokens? [y/N]"
read -r has_monad

if [[ ! "$has_monad" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo ""
    echo "❌ You need a Monad testnet wallet to continue"
    echo ""
    echo "Steps:"
    echo "1. Create a wallet (MetaMask, etc.)"
    echo "2. Get testnet tokens from Monad faucet"
    echo "3. Export your private key"
    echo ""
    echo "Then run this script again"
    exit 1
fi

echo ""
echo "Have you deployed the KinicMemoryLog contract? [y/N]"
read -r has_contract

if [[ ! "$has_contract" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo ""
    echo "Let's deploy the contract now"
    echo "Enter your Monad private key (will not be displayed):"
    read -s monad_key
    export MONAD_PRIVATE_KEY="$monad_key"

    echo ""
    echo "Deploying contract..."
    python contracts/deploy.py

    echo ""
    echo "✅ Contract deployed!"
    echo "   Contract address saved to contracts/deployment.json"
else
    echo "Skipping contract deployment"
fi
echo ""

# Step 7: Configure .env
echo "⚙️  Step 7: Configure Environment Variables"
echo ""

if [ -f .env ]; then
    echo "⚠️  .env file already exists"
    echo "Overwrite? [y/N]"
    read -r overwrite
    if [[ ! "$overwrite" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo "Keeping existing .env"
        echo ""
        echo "✅ Setup complete!"
        exit 0
    fi
fi

cp .env.example .env

echo ""
echo "Please enter the following values:"
echo ""

echo -n "MONAD_CONTRACT_ADDRESS (from deployment above): "
read -r contract_addr

echo -n "KINIC_MEMORY_ID (canister principal): "
read -r memory_id

echo -n "MONAD_PRIVATE_KEY (0x...): "
read -s private_key
echo ""

# Update .env
sed -i.bak "s|MONAD_CONTRACT_ADDRESS=.*|MONAD_CONTRACT_ADDRESS=$contract_addr|" .env
sed -i.bak "s|KINIC_MEMORY_ID=.*|KINIC_MEMORY_ID=$memory_id|" .env
sed -i.bak "s|MONAD_PRIVATE_KEY=.*|MONAD_PRIVATE_KEY=$private_key|" .env

# Get IC identity PEM
identity_pem=$(cat ~/.config/dfx/identity/$(dfx identity whoami)/identity.pem | sed 's/$/\\n/' | tr -d '\n')
echo "IC_IDENTITY_PEM=\"$identity_pem\"" >> .env

rm .env.bak

echo "✅ .env file configured"
echo ""

# Step 8: Test
echo "🧪 Step 8: Testing Setup"
echo ""
echo "Run local tests? [Y/n]"
read -r run_tests

if [[ ! "$run_tests" =~ ^([nN][oO]|[nN])$ ]]; then
    echo ""
    echo "Running tests..."
    ./scripts/test_local.sh
else
    echo "Skipping tests"
fi

echo ""
echo "=========================================="
echo "✅ SETUP COMPLETE!"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Test locally:"
echo "   ./scripts/test_local.sh"
echo ""
echo "2. Deploy to Render:"
echo "   - Push to GitHub: git push origin main"
echo "   - Create web service on Render.com"
echo "   - Set environment variables from .env"
echo "   - Deploy!"
echo ""
echo "3. Read the docs:"
echo "   cat README.md"
echo ""
echo "Happy building! 🚀"
