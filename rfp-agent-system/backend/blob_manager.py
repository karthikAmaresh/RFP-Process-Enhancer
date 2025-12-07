# Download files from Azure Blob Storage (works with private containers)
from azure.storage.blob import BlobServiceClient
import config
import sys
import os

def download_blob(blob_name: str, local_path: str = None):
    """
    Download a blob from Azure Storage to local file
    Works with private containers using connection string authentication
    
    Args:
        blob_name: Name of the blob in Azure Storage
        local_path: Local path to save file (optional, defaults to same name)
    """
    try:
        # Create BlobServiceClient using connection string (works with private access)
        blob_service_client = BlobServiceClient.from_connection_string(config.BLOB_CONN_STRING)
        
        # Get container and blob clients
        container_client = blob_service_client.get_container_client(config.BLOB_CONTAINER_NAME)
        blob_client = container_client.get_blob_client(blob_name)
        
        # Set local path
        if not local_path:
            local_path = os.path.join("data", "raw_text", blob_name)
        
        # Create directory if needed
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        print(f"Downloading '{blob_name}' from Azure Blob Storage...")
        
        # Download blob
        with open(local_path, "wb") as f:
            download_stream = blob_client.download_blob()
            f.write(download_stream.readall())
        
        file_size = os.path.getsize(local_path)
        print(f"✓ Downloaded successfully!")
        print(f"  Size: {file_size:,} bytes")
        print(f"  Saved to: {local_path}")
        
        return local_path
        
    except Exception as e:
        print(f"✗ Error downloading blob: {e}")
        return None


def list_blobs():
    """
    List all blobs in the container
    """
    try:
        blob_service_client = BlobServiceClient.from_connection_string(config.BLOB_CONN_STRING)
        container_client = blob_service_client.get_container_client(config.BLOB_CONTAINER_NAME)
        
        print(f"\nBlobs in container '{config.BLOB_CONTAINER_NAME}':")
        print("-" * 60)
        
        blobs = list(container_client.list_blobs())
        
        if not blobs:
            print("No blobs found in container.")
            return
        
        for i, blob in enumerate(blobs, 1):
            size_mb = blob.size / (1024 * 1024)
            print(f"{i}. {blob.name}")
            print(f"   Size: {size_mb:.2f} MB")
            print(f"   Last modified: {blob.last_modified}")
            print()
        
        return [blob.name for blob in blobs]
        
    except Exception as e:
        print(f"✗ Error listing blobs: {e}")
        return []


def upload_blob(local_file_path: str, blob_name: str = None):
    """
    Upload a local file to Azure Blob Storage
    
    Args:
        local_file_path: Path to local file
        blob_name: Name for blob (optional, defaults to filename)
    """
    try:
        if not os.path.exists(local_file_path):
            print(f"✗ File not found: {local_file_path}")
            return False
        
        if not blob_name:
            blob_name = os.path.basename(local_file_path)
        
        blob_service_client = BlobServiceClient.from_connection_string(config.BLOB_CONN_STRING)
        container_client = blob_service_client.get_container_client(config.BLOB_CONTAINER_NAME)
        blob_client = container_client.get_blob_client(blob_name)
        
        print(f"Uploading '{local_file_path}' to Azure Blob Storage...")
        
        with open(local_file_path, "rb") as f:
            blob_client.upload_blob(f, overwrite=True)
        
        print(f"✓ Uploaded successfully!")
        print(f"  Blob name: {blob_name}")
        print(f"  Container: {config.BLOB_CONTAINER_NAME}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error uploading blob: {e}")
        return False


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Manage Azure Blob Storage files')
    parser.add_argument('action', choices=['list', 'download', 'upload'], 
                       help='Action to perform')
    parser.add_argument('--blob', help='Blob name (for download/upload)')
    parser.add_argument('--file', help='Local file path (for download/upload)')
    
    args = parser.parse_args()
    
    if args.action == 'list':
        list_blobs()
    
    elif args.action == 'download':
        if not args.blob:
            print("Error: --blob required for download")
            print("Usage: python blob_manager.py download --blob my-file.pdf")
            return
        download_blob(args.blob, args.file)
    
    elif args.action == 'upload':
        if not args.file:
            print("Error: --file required for upload")
            print("Usage: python blob_manager.py upload --file my-file.pdf [--blob custom-name.pdf]")
            return
        upload_blob(args.file, args.blob)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Azure Blob Storage Manager")
        print("=" * 60)
        print("\nUsage:")
        print("  python blob_manager.py list")
        print("  python blob_manager.py download --blob my-file.pdf")
        print("  python blob_manager.py download --blob my-file.pdf --file ./local-copy.pdf")
        print("  python blob_manager.py upload --file my-file.pdf")
        print("  python blob_manager.py upload --file my-file.pdf --blob custom-name.pdf")
        print("\nExamples:")
        print("  # List all files in container")
        print("  python blob_manager.py list")
        print()
        print("  # Download a file")
        print("  python blob_manager.py download --blob rfp-document.pdf")
        print()
        print("  # Upload a file")
        print("  python blob_manager.py upload --file ./my-rfp.pdf")
        print("\n" + "=" * 60)
    else:
        main()
