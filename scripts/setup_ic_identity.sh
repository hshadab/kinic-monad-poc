#!/bin/bash
# Helper script to prepare IC identity for Render deployment

set -e

echo "🔑 IC Identity Setup for Render Deployment"
echo "==========================================="
echo ""

# Check if dfx is installed
if ! command -v dfx &> /dev/null; then
    echo "❌ Error: dfx not found"
    echo "Install from: https://internetcomputer.org/docs/current/developer-docs/setup/install"
    exit 1
fi

# Get identity name (default to "default")
IDENTITY_NAME=${1:-default}
echo "📝 Using identity: $IDENTITY_NAME"

# Check if identity exists
if ! dfx identity list | grep -q "^$IDENTITY_NAME$"; then
    echo "❌ Error: Identity '$IDENTITY_NAME' not found"
    echo ""
    echo "Available identities:"
    dfx identity list
    echo ""
    echo "Create a new identity with: dfx identity new $IDENTITY_NAME"
    exit 1
fi

# Get identity path
IDENTITY_PATH="$HOME/.config/dfx/identity/$IDENTITY_NAME/identity.pem"

if [ ! -f "$IDENTITY_PATH" ]; then
    echo "❌ Error: Identity file not found at $IDENTITY_PATH"
    exit 1
fi

echo "✅ Found identity file"
echo ""

# Display PEM content
echo "📄 PEM File Content (add to .env as IC_IDENTITY_PEM):"
echo "=================================================="
cat "$IDENTITY_PATH"
echo "=================================================="
echo ""

# Offer base64 encoding option
echo "Would you like to base64 encode it? (useful for single-line env var) [y/N]"
read -r response

if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo ""
    echo "📦 Base64 Encoded (single line):"
    echo "=================================================="
    base64 -w 0 "$IDENTITY_PATH" 2>/dev/null || base64 "$IDENTITY_PATH" | tr -d '\n'
    echo ""
    echo "=================================================="
    echo ""
    echo "⚠️  Note: You'll need to decode this in your app if using base64"
fi

# Get principal
echo ""
echo "🆔 Principal for this identity:"
echo "=================================================="
dfx identity use "$IDENTITY_NAME" &>/dev/null
dfx identity get-principal
echo "=================================================="
echo ""

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Copy the PEM content above to your .env file as IC_IDENTITY_PEM"
echo "2. Or set it as an environment variable in Render dashboard"
echo "3. Make sure your identity has ICP tokens for canister operations"
