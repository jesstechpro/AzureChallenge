# Azure Storage Static Website Migration Plan

## Overview
This plan outlines the migration of your resume website from local hosting to Azure Storage static website hosting with HTTPS via Azure CDN and custom DNS configuration.

## Current State Analysis
- **Static Files**: `index.html`, `style.css`, `script.js`, `robots.txt`
- **Backend**: Azure Functions with Cosmos DB (already deployed)
- **Current API Endpoints**: Using localhost URLs in HTML (lines 31-32)
- **Domain**: Need custom domain (e.g., my-c00l-resume-website.com)

## Architecture Overview
```
[Custom Domain] → [Azure CDN] → [Azure Storage Static Website] → [Azure Functions API]
     HTTPS           HTTPS              HTTP                        HTTPS
```

---

# Phase 1: Prerequisites & Setup

## 1.1 Azure Resources Required
- **Azure Storage Account** (General Purpose v2)
- **Azure CDN Profile** (Standard Microsoft or Premium Verizon)
- **Domain Name** (~$10-15/year)
- **Azure DNS Zone** (optional, can use external DNS provider)

## 1.2 Cost Estimates (Monthly)
- **Storage Account**: ~$0.50-2.00 (minimal storage + transactions)
- **Azure CDN**: ~$0.10-1.00 (low traffic)
- **Azure DNS**: ~$0.50 (if using Azure DNS)
- **Domain Registration**: ~$1.00/month (annual cost divided)
- **Total**: ~$2-5/month

## 1.3 Tools & Access
- [x] Azure CLI installed and configured
- [x] Azure subscription with appropriate permissions
- [ ] Domain registrar account (GoDaddy, Namecheap, etc.)
- [ ] DNS management access

---

# Phase 2: Azure Storage Static Website Setup

## 2.1 Create Storage Account
```bash
# Create resource group (if not exists)
az group create --name rg-resume-website --location eastus

# Create storage account
az storage account create \
  --name stresumejesswood \
  --resource-group rg-resume-website \
  --location eastus \
  --sku Standard_LRS \
  --kind StorageV2 \
  --access-tier Hot
```

## 2.2 Enable Static Website Hosting
```bash
# Enable static website hosting
az storage blob service-properties update \
  --account-name stresumejesswood \
  --static-website \
  --404-document 404.html \
  --index-document index.html
```

## 2.3 Upload Website Files
```bash
# Get storage account key
STORAGE_KEY=$(az storage account keys list --account-name stresumejesswood --resource-group rg-resume-website --query '[0].value' -o tsv)

# Upload files to $web container
az storage blob upload-batch \
  --account-name stresumejesswood \
  --account-key $STORAGE_KEY \
  --destination '$web' \
  --source ./ \
  --pattern "*.html" \
  --pattern "*.css" \
  --pattern "*.js" \
  --pattern "*.txt"
```

## 2.4 Update API Endpoints
**Before uploading**, update `index.html` to use production Azure Functions URLs:
- Replace `http://localhost:7072/api/counter` with production URL
- Replace `http://localhost:7072/api/counter/increment` with production URL

## 2.5 Test Static Website
- Get static website URL: `https://stresumejesswood.z13.web.core.windows.net/`
- Verify all files load correctly
- Test visitor counter functionality

---

# Phase 3: Azure CDN Configuration for HTTPS

## 3.1 Create CDN Profile
```bash
# Create CDN profile
az cdn profile create \
  --name cdn-resume-website \
  --resource-group rg-resume-website \
  --sku Standard_Microsoft
```

## 3.2 Create CDN Endpoint
```bash
# Create CDN endpoint
az cdn endpoint create \
  --name jesswood-resume \
  --profile-name cdn-resume-website \
  --resource-group rg-resume-website \
  --origin stresumejesswood.z13.web.core.windows.net \
  --origin-host-header stresumejesswood.z13.web.core.windows.net \
  --enable-compression true \
  --content-types-to-compress "text/html" "text/css" "application/javascript"
```

## 3.3 Configure HTTPS Settings
```bash
# Enable HTTPS redirect
az cdn endpoint update \
  --name jesswood-resume \
  --profile-name cdn-resume-website \
  --resource-group rg-resume-website \
  --https-redirect Enabled
```

## 3.4 Test CDN Endpoint
- CDN URL: `https://jesswood-resume.azureedge.net/`
- Verify HTTPS works
- Test performance and caching
- Verify visitor counter still functions

---

# Phase 4: Custom DNS Configuration

## 4.1 Domain Registration
1. **Choose Domain**: e.g., `my-c00l-resume-website.com`
2. **Register Domain**: Use registrar like GoDaddy, Namecheap, or Hover
3. **Cost**: ~$10-15 for .com domain

## 4.2 Option A: Azure DNS (Recommended)
```bash
# Create DNS zone
az network dns zone create \
  --name my-c00l-resume-website.com \
  --resource-group rg-resume-website

# Get name servers
az network dns zone show \
  --name my-c00l-resume-website.com \
  --resource-group rg-resume-website \
  --query nameServers
```

**Configure at Domain Registrar**:
- Update name servers to Azure DNS name servers
- Wait 24-48 hours for propagation

**Create DNS Records**:
```bash
# Create CNAME record for www
az network dns record-set cname create \
  --name www \
  --zone-name my-c00l-resume-website.com \
  --resource-group rg-resume-website

az network dns record-set cname set-record \
  --record-set-name www \
  --zone-name my-c00l-resume-website.com \
  --resource-group rg-resume-website \
  --cname jesswood-resume.azureedge.net

# Create CNAME record for apex domain (using alias)
az network dns record-set a create \
  --name @ \
  --zone-name my-c00l-resume-website.com \
  --resource-group rg-resume-website

# Note: For apex domain, you'll need to use CNAME flattening or ALIAS record
```

## 4.3 Option B: External DNS Provider
**At your DNS provider**, create:
- **CNAME Record**: `www` → `jesswood-resume.azureedge.net`
- **CNAME Record**: `@` or apex → `jesswood-resume.azureedge.net` (if supported)
- **A Record**: If CNAME not supported for apex, use CDN IP address

## 4.4 Configure Custom Domain on CDN
```bash
# Add custom domain to CDN endpoint
az cdn custom-domain create \
  --endpoint-name jesswood-resume \
  --name my-c00l-resume-website-com \
  --profile-name cdn-resume-website \
  --resource-group rg-resume-website \
  --hostname my-c00l-resume-website.com
```

## 4.5 Enable HTTPS for Custom Domain
```bash
# Enable managed certificate for custom domain
az cdn custom-domain enable-https \
  --endpoint-name jesswood-resume \
  --name my-c00l-resume-website-com \
  --profile-name cdn-resume-website \
  --resource-group rg-resume-website \
  --min-tls-version 1.2
```

---

# Phase 5: Testing & Validation

## 5.1 DNS Propagation Testing
```bash
# Test DNS resolution
nslookup my-c00l-resume-website.com
nslookup www.my-c00l-resume-website.com

# Test with online tools
# - whatsmydns.net
# - dnschecker.org
```

## 5.2 HTTPS Certificate Validation
- Verify SSL certificate is valid and trusted
- Test with SSL Labs: ssllabs.com/ssltest/
- Ensure HTTP redirects to HTTPS

## 5.3 Functionality Testing
- [ ] Website loads correctly on custom domain
- [ ] All CSS and JavaScript files load
- [ ] Visitor counter functions properly
- [ ] Azure Functions API calls work
- [ ] Mobile responsiveness maintained
- [ ] SEO meta tags preserved

## 5.4 Performance Testing
- [ ] Page load speed (should improve with CDN)
- [ ] Global accessibility (CDN edge locations)
- [ ] Compression working (check response headers)

---

# Phase 6: Production Deployment Checklist

## 6.1 Pre-Deployment
- [ ] Backup current website files
- [ ] Update Azure Functions URLs in HTML
- [ ] Test locally with production API endpoints
- [ ] Prepare rollback plan

## 6.2 Deployment Steps
1. [ ] Create Azure Storage Account
2. [ ] Enable static website hosting
3. [ ] Upload website files
4. [ ] Create CDN profile and endpoint
5. [ ] Register domain name
6. [ ] Configure DNS records
7. [ ] Add custom domain to CDN
8. [ ] Enable HTTPS certificate
9. [ ] Test all functionality

## 6.3 Post-Deployment
- [ ] Update any hardcoded URLs
- [ ] Monitor Azure costs
- [ ] Set up monitoring/alerting
- [ ] Document new URLs and credentials
- [ ] Update documentation

---

# Phase 7: Ongoing Maintenance

## 7.1 Regular Tasks
- **Monthly**: Review Azure costs and usage
- **Quarterly**: Check SSL certificate status
- **Annually**: Renew domain registration

## 7.2 Monitoring Setup
```bash
# Enable diagnostic logging for CDN
az monitor diagnostic-settings create \
  --name cdn-diagnostics \
  --resource jesswood-resume \
  --resource-group rg-resume-website \
  --resource-type Microsoft.Cdn/profiles/endpoints \
  --logs '[{"category":"CoreAnalytics","enabled":true}]'
```

## 7.3 Security Considerations
- [ ] Enable CDN security features
- [ ] Configure custom error pages
- [ ] Set up Content Security Policy headers
- [ ] Regular security scanning

---

# Troubleshooting Guide

## Common Issues

### DNS Not Resolving
- **Cause**: DNS propagation delay or incorrect records
- **Solution**: Wait 24-48 hours, verify DNS records with `nslookup`

### HTTPS Certificate Issues
- **Cause**: Domain validation failed or DNS not propagated
- **Solution**: Ensure DNS is working first, then retry certificate provisioning

### CDN Caching Issues
- **Cause**: Old content cached at CDN edge
- **Solution**: Purge CDN cache or wait for TTL expiration

### API Calls Failing
- **Cause**: CORS issues or incorrect API URLs
- **Solution**: Verify CORS settings on Azure Functions, check API endpoints

---

# Resource Names Convention

| Resource Type | Name | Purpose |
|---------------|------|---------|
| Resource Group | `rg-resume-website` | Container for all resources |
| Storage Account | `stresumejesswood` | Static website hosting |
| CDN Profile | `cdn-resume-website` | CDN service |
| CDN Endpoint | `jesswood-resume` | CDN endpoint |
| DNS Zone | `my-c00l-resume-website.com` | DNS management |

---

# Next Steps

1. **Review and approve this plan**
2. **Register your chosen domain name**
3. **Execute Phase 2: Azure Storage setup**
4. **Continue through phases sequentially**
5. **Test thoroughly at each phase**

**Estimated Total Time**: 2-4 hours (excluding DNS propagation wait times)
**Estimated Total Cost**: $2-5/month + $10-15 domain registration
