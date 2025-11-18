#!/bin/bash

# DNS Propagation Checker for kinicmemory.com

echo "========================================"
echo "  DNS Propagation Status Check"
echo "========================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "Checking kinicmemory.com..."
echo ""

# Check root domain
echo -n "Root domain (kinicmemory.com): "
RESULT=$(nslookup kinicmemory.com 8.8.8.8 2>/dev/null | grep -A1 "Name:" | grep "Address:" | awk '{print $2}' | head -1)
if [ "$RESULT" == "216.24.57.1" ]; then
    echo -e "${GREEN}✓ Propagated${NC} ($RESULT)"
elif [ -n "$RESULT" ]; then
    echo -e "${YELLOW}⚠ Partial${NC} ($RESULT - should be 216.24.57.1)"
else
    echo -e "${RED}✗ Not propagated yet${NC}"
fi

# Check www subdomain
echo -n "WWW subdomain (www.kinicmemory.com): "
RESULT=$(nslookup www.kinicmemory.com 8.8.8.8 2>/dev/null | grep "canonical name" | awk '{print $5}')
if [ "$RESULT" == "monad-ai-memory.onrender.com." ]; then
    echo -e "${GREEN}✓ Propagated${NC} (CNAME: monad-ai-memory.onrender.com)"
elif [ -n "$RESULT" ]; then
    echo -e "${YELLOW}⚠ Partial${NC} (CNAME: $RESULT)"
else
    echo -e "${RED}✗ Not propagated yet${NC}"
fi

echo ""
echo "========================================"
echo "Next Steps:"
echo "========================================"
echo "1. Wait 15-30 minutes if not propagated"
echo "2. Run this script again: ./check_dns.sh"
echo "3. Once propagated, verify in Render dashboard"
echo "4. Update CORS settings"
echo ""
echo "Online check: https://www.whatsmydns.net/"
echo "========================================"
