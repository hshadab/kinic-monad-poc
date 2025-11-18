# Custom Domain Setup - kinicmemory.com

**Domain:** kinicmemory.com
**Render Service:** monad-ai-memory.onrender.com
**Goal:** Point both www.kinicmemory.com and kinicmemory.com to your Render app

---

## 📋 **Overview**

You need to configure DNS records at your domain registrar (where you bought kinicmemory.com) to point to Render.

**Two records needed:**
1. `www.kinicmemory.com` → CNAME record
2. `kinicmemory.com` → ANAME/ALIAS or A record

---

## 🔍 **Step 1: Find Your DNS Provider**

Where did you buy kinicmemory.com? Common providers:
- **Namecheap** (namecheap.com)
- **GoDaddy** (godaddy.com)
- **Google Domains** (domains.google.com) - Now Squarespace
- **Cloudflare** (cloudflare.com)
- **Porkbun** (porkbun.com)
- **Name.com** (name.com)

The DNS settings will be in your registrar's control panel.

---

## 🌐 **Step 2: Configure DNS Records**

### **For www.kinicmemory.com (Subdomain)**

**Record Type:** CNAME

| Type | Name | Value | TTL |
|------|------|-------|-----|
| CNAME | www | monad-ai-memory.onrender.com | Auto or 3600 |

**Instructions by Provider:**

#### **Namecheap:**
1. Log in to Namecheap
2. Go to **Domain List** → Select `kinicmemory.com`
3. Click **Manage** → **Advanced DNS**
4. Click **Add New Record**
5. Select **CNAME Record**
6. Host: `www`
7. Target: `monad-ai-memory.onrender.com`
8. TTL: Automatic
9. Click **Save All Changes**

#### **GoDaddy:**
1. Log in to GoDaddy
2. Go to **My Products** → **DNS**
3. Select `kinicmemory.com`
4. Click **Add** → Choose **CNAME**
5. Name: `www`
6. Value: `monad-ai-memory.onrender.com`
7. TTL: 1 Hour
8. Click **Save**

#### **Cloudflare:**
1. Log in to Cloudflare
2. Select `kinicmemory.com` domain
3. Go to **DNS** → **Records**
4. Click **Add record**
5. Type: `CNAME`
6. Name: `www`
7. Target: `monad-ai-memory.onrender.com`
8. Proxy status: **DNS only** (gray cloud, not orange)
9. Click **Save**

#### **Porkbun:**
1. Log in to Porkbun
2. Go to **Account** → **Domain Management**
3. Select `kinicmemory.com`
4. Scroll to **DNS Records**
5. Add New Record:
   - Type: `CNAME`
   - Host: `www`
   - Answer: `monad-ai-memory.onrender.com`
   - TTL: 600
6. Click **Add**

---

### **For kinicmemory.com (Root Domain)**

**Option A: ANAME/ALIAS Record (Preferred)**

If your DNS provider supports ANAME or ALIAS records:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| ANAME or ALIAS | @ | monad-ai-memory.onrender.com | Auto or 3600 |

**Providers that support ANAME/ALIAS:**
- ✅ Cloudflare (CNAME Flattening)
- ✅ DNS Made Easy (ANAME)
- ✅ DNSimple (ALIAS)
- ✅ Route53 (ALIAS)
- ✅ Namecheap (ALIAS)

**Option B: A Record (Fallback)**

If your DNS provider does NOT support ANAME/ALIAS:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | @ | 216.24.57.1 | Auto or 3600 |

**Instructions by Provider:**

#### **Namecheap (ALIAS Supported):**
1. Go to **Advanced DNS**
2. Click **Add New Record**
3. Select **ALIAS Record**
4. Host: `@`
5. Target: `monad-ai-memory.onrender.com`
6. TTL: Automatic
7. Click **Save All Changes**

**OR use A Record:**
1. Add New Record
2. Type: **A Record**
3. Host: `@`
4. Value: `216.24.57.1`
5. TTL: Automatic

#### **GoDaddy (A Record Only):**
1. Go to DNS settings
2. Click **Add** → Choose **A**
3. Name: `@`
4. Value: `216.24.57.1`
5. TTL: 1 Hour
6. Click **Save**

#### **Cloudflare (CNAME Flattening):**
1. Go to **DNS** → **Records**
2. Click **Add record**
3. Type: `CNAME`
4. Name: `@`
5. Target: `monad-ai-memory.onrender.com`
6. Proxy status: **DNS only** (gray cloud)
7. Click **Save**

Note: Cloudflare automatically flattens CNAME at root

---

## ⏱️ **Step 3: Wait for DNS Propagation**

**Time Required:** 5 minutes to 48 hours (usually 15-30 minutes)

### **Check DNS Propagation:**

```bash
# Check CNAME for www
dig www.kinicmemory.com CNAME +short
# Should show: monad-ai-memory.onrender.com

# Check A record for root
dig kinicmemory.com A +short
# Should show: 216.24.57.1 (or Render's IP)

# Check from multiple locations
# Use: https://www.whatsmydns.net/
```

**Online Tools:**
- https://www.whatsmydns.net/
- https://dnschecker.org/
- https://mxtoolbox.com/DNSLookup.aspx

---

## ✅ **Step 4: Verify Domain in Render**

Once DNS records are configured and propagating:

### **In Render Dashboard:**

1. Go to https://dashboard.render.com
2. Select your service: **monad-ai-memory**
3. Go to **Settings** → **Custom Domains**
4. You should see:
   ```
   www.kinicmemory.com - DNS update needed to verify
   kinicmemory.com - DNS update needed to verify
   ```
5. Click **Verify** for each domain
6. Wait for verification (may take a few minutes)

### **Verification Process:**

Render checks:
- ✅ DNS records are pointing correctly
- ✅ Domain ownership is confirmed
- ✅ SSL certificate can be issued

**When verified, you'll see:**
```
www.kinicmemory.com - ✓ Verified
kinicmemory.com - ✓ Verified
```

---

## 🔒 **Step 5: SSL Certificate (Automatic)**

Render automatically provisions SSL certificates from Let's Encrypt.

**After verification:**
- Render issues SSL certificate (1-5 minutes)
- Your site becomes accessible via HTTPS
- HTTP automatically redirects to HTTPS

**Check SSL:**
```bash
curl -I https://kinicmemory.com
# Should show: HTTP/2 200
```

---

## 🌍 **Step 6: Test Your Domain**

### **Test in Browser:**

1. **Root domain:**
   - http://kinicmemory.com → Should redirect to https://kinicmemory.com
   - https://kinicmemory.com → Should work ✅

2. **www subdomain:**
   - http://www.kinicmemory.com → Should redirect to https://www.kinicmemory.com
   - https://www.kinicmemory.com → Should redirect to https://kinicmemory.com (if configured)

### **Test API Endpoints:**

```bash
# Health check
curl https://kinicmemory.com/health

# Should return:
# {"status":"healthy","kinic":"connected","monad":"connected"...}

# Stats
curl https://kinicmemory.com/stats
```

---

## 🔧 **Step 7: Update CORS Settings**

Your CORS settings need to include the new domain!

### **Update in Render Environment Variables:**

1. Go to Render Dashboard → Your Service → **Environment**
2. Find or add `ALLOWED_ORIGINS`
3. Update to:
   ```
   https://kinicmemory.com,https://www.kinicmemory.com,http://localhost:3000,http://localhost:8000
   ```
4. Click **Save Changes**
5. Render will automatically redeploy

### **Or update in your code:**

Edit `src/main.py` and update the default:

```python
allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "https://kinicmemory.com,https://www.kinicmemory.com,http://localhost:3000,http://localhost:8000"
).split(",")
```

---

## 📝 **Complete DNS Configuration Example**

### **Final DNS Records:**

For `kinicmemory.com` at your registrar:

| Type | Name/Host | Value/Target | TTL |
|------|-----------|--------------|-----|
| A | @ | 216.24.57.1 | 3600 |
| CNAME | www | monad-ai-memory.onrender.com | 3600 |

**OR** (if ALIAS supported):

| Type | Name/Host | Value/Target | TTL |
|------|-----------|--------------|-----|
| ALIAS | @ | monad-ai-memory.onrender.com | 3600 |
| CNAME | www | monad-ai-memory.onrender.com | 3600 |

---

## 🆘 **Troubleshooting**

### **Issue: "DNS update needed" doesn't go away**

**Solutions:**

1. **Wait longer** - DNS can take up to 48 hours
2. **Check DNS propagation:**
   ```bash
   dig www.kinicmemory.com
   dig kinicmemory.com
   ```
3. **Verify records are correct:**
   - www → CNAME → monad-ai-memory.onrender.com
   - @ → A → 216.24.57.1
4. **Clear DNS cache:**
   ```bash
   # On Mac:
   sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder

   # On Windows:
   ipconfig /flushdns

   # On Linux:
   sudo systemd-resolve --flush-caches
   ```

### **Issue: "Too many redirects"**

**Solution:**
- If using Cloudflare, set Proxy Status to **DNS only** (gray cloud)
- Check that you don't have conflicting redirect rules

### **Issue: SSL certificate not provisioning**

**Solutions:**
1. Make sure domain is verified first
2. Wait 5-10 minutes after verification
3. Check that DNS records are correct
4. Contact Render support if it persists

### **Issue: www redirects incorrectly**

**Solution:**
- Configure redirect in Render:
  1. Settings → Custom Domains
  2. Set www.kinicmemory.com to redirect to kinicmemory.com
  3. Or vice versa (choose one as primary)

---

## 🎯 **Best Practices**

### **1. Choose Primary Domain**

Decide which is primary:
- Option A: `kinicmemory.com` (no www) ← **Recommended**
- Option B: `www.kinicmemory.com`

Then redirect the other to the primary.

### **2. Update All References**

After domain is working, update:

- ✅ Render environment variables (ALLOWED_ORIGINS)
- ✅ GitHub README.md
- ✅ Monad submission JSON (if not submitted yet)
- ✅ Social media links
- ✅ Documentation

### **3. Set Up Monitoring**

```bash
# Add to cron or monitoring service
*/5 * * * * curl -f https://kinicmemory.com/health || echo "Site down!"
```

---

## 📊 **Update Monad Submission**

If you haven't submitted to Monad yet, update your JSON:

```json
{
  "name": "Kinic AI Memory Agent",
  "description": "...",
  "live": true,
  "categories": ["Apps::AI", "Infra::Storage"],
  "addresses": {
    "KinicMemoryLog": "0xEB5B78Fa81cFEA1a46D46B3a42814F5A68038548"
  },
  "links": {
    "project": "https://kinicmemory.com",  ← Updated!
    "github": "https://github.com/hshadab/kinic-monad-poc",
    "docs": "https://github.com/hshadab/kinic-monad-poc/blob/master/README.md"
  }
}
```

---

## ✅ **Checklist**

Before considering setup complete:

- [ ] DNS records added (CNAME for www, A or ALIAS for root)
- [ ] DNS propagation complete (check with dig or online tools)
- [ ] Domains verified in Render
- [ ] SSL certificates issued and working
- [ ] Both http and https redirect correctly
- [ ] API endpoints work on new domain
- [ ] CORS updated to include new domain
- [ ] All documentation updated
- [ ] Monad submission updated (if applicable)
- [ ] Old render.com URLs still work (Render keeps them)

---

## 🎉 **Final Result**

After setup:

✅ https://kinicmemory.com → Your app
✅ https://www.kinicmemory.com → Redirects to kinicmemory.com
✅ https://monad-ai-memory.onrender.com → Still works (kept as backup)

**Your professional domain is live!** 🚀

---

## 📞 **Need Help?**

- **Render Docs:** https://render.com/docs/custom-domains
- **Render Support:** support@render.com
- **DNS Help:** Contact your registrar's support

**Common Registrar Support:**
- Namecheap: https://www.namecheap.com/support/
- GoDaddy: https://www.godaddy.com/help
- Cloudflare: https://support.cloudflare.com/

---

**Good luck with your domain setup!** 🌐
