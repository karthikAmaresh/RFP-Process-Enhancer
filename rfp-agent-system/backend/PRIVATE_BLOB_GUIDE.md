# Working with Private Azure Blob Storage

## ✅ You're Already Set Up!

Your `.env` file has the **connection string with AccountKey**, which provides full access to private blobs. No changes needed!

## Understanding Access Types

### 🔒 Private Access (Your Current Setup - RECOMMENDED)
- **Most Secure**: Only authenticated requests work
- **Access Method**: Connection string with AccountKey
- **Your Status**: ✅ Configured and working

### 🌐 Public Access (You Disabled This - Good!)
- Less secure: Anyone with URL can access
- Not needed for your use case

## How to Use Your Private Blob Storage

### **1. List All Files in Container**

```cmd
python blob_manager.py list
```

**Output:**
```
Blobs in container 'rfpenhancer1':
------------------------------------------------------------
1. sample-rfp.pdf
   Size: 2.34 MB
   Last modified: 2025-12-07 10:30:00

2. requirements-doc.docx
   Size: 1.12 MB
   Last modified: 2025-12-07 09:15:00
```

### **2. Upload a File to Azure**

```cmd
python blob_manager.py upload --file my-local-file.pdf
```

Or with custom name:
```cmd
python blob_manager.py upload --file ./documents/rfp.pdf --blob project-a-rfp.pdf
```

### **3. Download a File from Azure**

```cmd
python blob_manager.py download --blob sample-rfp.pdf
```

Or specify local path:
```cmd
python blob_manager.py download --blob sample-rfp.pdf --file ./downloads/rfp.pdf
```

### **4. Process a File Directly from Azure**

```cmd
python pipeline.py --blob sample-rfp.pdf
```

This will:
1. ✅ Authenticate using your connection string
2. ✅ Access the private blob
3. ✅ Extract text using Document Intelligence
4. ✅ Run all agents
5. ✅ Save results to `kb.md`

---

## How It Works (Behind the Scenes)

### Connection String Components

Your connection string has:
```
DefaultEndpointsProtocol=https
AccountName=rfpenhancer1              ← Your storage account
AccountKey=cLNmTU4/...                ← Authentication key (like a password)
EndpointSuffix=core.windows.net
```

The **AccountKey** acts like a master password that gives your application full access to private containers.

### Authentication Flow

```
Your App
    ↓
Connection String (with AccountKey)
    ↓
Azure Blob Storage (validates key)
    ↓
Access Granted (even for private blobs)
    ↓
Download/Upload/List Operations
```

---

## Common Tasks

### Upload Multiple Files

```python
# Python script
from blob_manager import upload_blob
import os

folder = "./rfp-documents"
for filename in os.listdir(folder):
    if filename.endswith(('.pdf', '.docx', '.txt')):
        filepath = os.path.join(folder, filename)
        upload_blob(filepath)
```

### Process All Blobs in Container

```python
from blob_manager import list_blobs
import subprocess

blob_names = list_blobs()
for blob_name in blob_names:
    print(f"\nProcessing {blob_name}...")
    subprocess.run(["python", "pipeline.py", "--blob", blob_name])
```

### Download All Blobs

```cmd
python -c "from blob_manager import list_blobs, download_blob; [download_blob(b) for b in list_blobs()]"
```

---

## Troubleshooting Private Blob Access

### ❌ Error: "Blob not found"
**Cause**: Blob name doesn't exist or is misspelled

**Solution**:
```cmd
# List all blobs first
python blob_manager.py list

# Then use exact name
python blob_manager.py download --blob exact-name-from-list.pdf
```

### ❌ Error: "Authentication failed"
**Cause**: Connection string issue

**Solution**:
1. Check `.env` file has complete connection string
2. No spaces before/after the `=` sign
3. Connection string should be one long line
4. Regenerate key in Azure Portal if needed:
   - Go to Storage Account → Access Keys → Regenerate key1

### ❌ Error: "Container not found"
**Cause**: Container name mismatch

**Solution**:
```env
# In .env file, make sure container name matches Azure
BLOB_CONTAINER_NAME=rfpenhancer1  # Must match exactly (case-sensitive)
```

### ❌ Error: "This request is not authorized"
**Cause**: Account key expired or changed

**Solution**:
1. Go to Azure Portal → Storage Account → Access Keys
2. Copy new connection string
3. Update `.env` file
4. Restart your application

---

## Security Best Practices

### ✅ DO:
- Keep connection string in `.env` file (never commit to git)
- Use `.gitignore` to exclude `.env`
- Rotate keys periodically
- Use different keys for dev/prod
- Monitor access logs in Azure Portal

### ❌ DON'T:
- Share connection strings publicly
- Commit `.env` to version control
- Use public access unless absolutely necessary
- Hardcode credentials in code

---

## Alternative: Using SAS Tokens (Optional)

If you want temporary access instead of full AccountKey:

```python
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
import config

# Generate SAS token (valid for 1 hour)
sas_token = generate_blob_sas(
    account_name="rfpenhancer1",
    container_name=config.BLOB_CONTAINER_NAME,
    blob_name="sample-rfp.pdf",
    account_key="your-account-key",
    permission=BlobSasPermissions(read=True),
    expiry=datetime.utcnow() + timedelta(hours=1)
)

# Share this URL (expires in 1 hour)
sas_url = f"https://rfpenhancer1.blob.core.windows.net/{config.BLOB_CONTAINER_NAME}/sample-rfp.pdf?{sas_token}"
```

But for your internal use, the connection string method is simpler and more appropriate.

---

## Quick Reference

```cmd
# List files
python blob_manager.py list

# Upload file
python blob_manager.py upload --file my-file.pdf

# Download file
python blob_manager.py download --blob my-file.pdf

# Process from blob
python pipeline.py --blob my-file.pdf

# Verify setup
python verify_setup.py
```

---

## Your Setup Summary

✅ **Storage Account**: `rfpenhancer1`  
✅ **Container**: `rfpenhancer1`  
✅ **Access Level**: Private (Secure) ✓  
✅ **Authentication**: Connection String with AccountKey  
✅ **Status**: Fully configured and working  

You're all set to work with private blobs! 🎉
