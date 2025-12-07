# How to Get Azure Credentials - Visual Guide

## 📋 Document Intelligence Credentials

### Step-by-Step:

1. **Login to Azure Portal**
   - Go to: https://portal.azure.com
   - Sign in with your account

2. **Find Your Document Intelligence Resource**
   - Search for "Document Intelligence" or "Form Recognizer" in the top search bar
   - OR click "All resources" and find your resource

3. **Get Endpoint and Key**
   - Click on your Document Intelligence resource name
   - In the left menu, click **"Keys and Endpoint"**
   - You'll see:
     ```
     ENDPOINT: https://your-resource-name.cognitiveservices.azure.com/
     KEY 1: abc123...xyz789
     KEY 2: xyz789...abc123
     ```
   - Copy **ENDPOINT** and **KEY 1**

4. **Paste in .env file**
   ```env
   FORM_RECOGNIZER_ENDPOINT=https://your-resource-name.cognitiveservices.azure.com/
   FORM_RECOGNIZER_KEY=abc123...xyz789
   ```

---

## 💾 Blob Storage Credentials

### Step-by-Step:

1. **Find Your Storage Account**
   - In Azure Portal, search for "Storage accounts"
   - Click on your storage account name

2. **Get Connection String**
   - In the left menu, click **"Access keys"** (under Security + networking)
   - You'll see:
     ```
     key1
     ├─ Key: [Show] button
     └─ Connection string: [Show] button  ← Click this!
     ```
   - Click **"Show"** next to Connection string under key1
   - Copy the entire string (it's long!)
     ```
     DefaultEndpointsProtocol=https;AccountName=yourstorage;
     AccountKey=longkeyhere;EndpointSuffix=core.windows.net
     ```

3. **Get Container Name**
   - In the left menu, click **"Containers"** (under Data storage)
   - Find your container name (e.g., `rfp-documents`)
   - If you don't have one, click **"+ Container"** to create

4. **Paste in .env file**
   ```env
   BLOB_CONN_STRING=DefaultEndpointsProtocol=https;AccountName=yourstorage;AccountKey=longkey;EndpointSuffix=core.windows.net
   BLOB_CONTAINER_NAME=rfp-documents
   ```

---

## ✅ Verification

### Test Document Intelligence:
```python
# Run this in Python to test
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import config

client = DocumentAnalysisClient(
    endpoint=config.FORM_RECOGNIZER_ENDPOINT,
    credential=AzureKeyCredential(config.FORM_RECOGNIZER_KEY)
)
print("✓ Document Intelligence connected!")
```

### Test Blob Storage:
```python
# Run this in Python to test
from azure.storage.blob import BlobServiceClient
import config

client = BlobServiceClient.from_connection_string(config.BLOB_CONN_STRING)
container = client.get_container_client(config.BLOB_CONTAINER_NAME)
print(f"✓ Blob Storage connected! Container: {config.BLOB_CONTAINER_NAME}")
```

---

## 🔍 Quick Commands to Find Info

### Using Azure CLI (if installed):

```bash
# Get Document Intelligence endpoint
az cognitiveservices account show --name YOUR_RESOURCE_NAME --resource-group YOUR_RG --query "properties.endpoint"

# Get Document Intelligence key
az cognitiveservices account keys list --name YOUR_RESOURCE_NAME --resource-group YOUR_RG

# Get Storage connection string
az storage account show-connection-string --name YOUR_STORAGE_NAME --resource-group YOUR_RG
```

---

## 🎯 Common Issues

### Issue: "Endpoint not found"
**Solution:** 
- Make sure endpoint ends with `/`
- Example: `https://your-resource.cognitiveservices.azure.com/`

### Issue: "Invalid key"
**Solution:**
- Copy the entire key (no spaces before/after)
- Use KEY 1 or KEY 2 (both work)
- Regenerate key if needed

### Issue: "Container not found"
**Solution:**
- Container name is case-sensitive
- Check spelling matches exactly
- Create container if it doesn't exist

### Issue: "Connection string invalid"
**Solution:**
- Copy the ENTIRE connection string (it's one long line)
- Should start with: `DefaultEndpointsProtocol=https;...`
- No spaces or line breaks

---

## 📝 Complete .env Template

```env
# ========================================
# REQUIRED: Azure Document Intelligence
# ========================================
FORM_RECOGNIZER_ENDPOINT=https://YOUR-RESOURCE.cognitiveservices.azure.com/
FORM_RECOGNIZER_KEY=your_32_character_key_here

# ========================================
# REQUIRED: Azure Blob Storage
# ========================================
BLOB_CONN_STRING=DefaultEndpointsProtocol=https;AccountName=youraccount;AccountKey=yourkey;EndpointSuffix=core.windows.net
BLOB_CONTAINER_NAME=rfp-documents

# ========================================
# OPTIONAL: Not needed for local LLM setup
# ========================================
MONGO_CONN_STR=
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_DEPLOYMENT=
SEARCH_ENDPOINT=
SEARCH_API_KEY=
SEARCH_INDEX_NAME=
```

---

## 🚀 After Setting Up Credentials

1. **Save** the `.env` file
2. **Test** the connection:
   ```cmd
   python -c "import config; print('Endpoint:', config.FORM_RECOGNIZER_ENDPOINT)"
   ```
3. **Run** the pipeline:
   ```cmd
   python pipeline.py --file sample_rfp.txt
   ```

---

## 💡 Pro Tips

1. **Keep keys secure** - Don't commit `.env` to git
2. **Use key rotation** - Regenerate keys periodically
3. **Test incrementally** - Test each service separately first
4. **Check pricing** - Document Intelligence charges per page analyzed
5. **Monitor usage** - Check Azure Portal > Cost Management

---

## Need More Help?

- Azure Document Intelligence Docs: https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/
- Azure Blob Storage Docs: https://learn.microsoft.com/en-us/azure/storage/blobs/
- Contact: Check the main README.md for support options
