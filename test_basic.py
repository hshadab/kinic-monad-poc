#!/usr/bin/env python3
"""
Basic unit tests for Kinic Memory Agent components
Tests components that don't require external services
"""
import sys
sys.path.insert(0, 'src')

from metadata import extract_metadata
from models import InsertRequest, SearchRequest, Metadata

def test_metadata_extraction():
    """Test metadata extraction"""
    print("\n🧪 Testing Metadata Extraction")
    print("="*50)

    # Test case 1: Markdown with heading
    content1 = """# ZKML Verification

Jolt Atlas is a framework that enables zero-knowledge proofs for machine learning inference.
This allows you to verify that ML models produce correct outputs without revealing the model itself.

Key features:
- Verifiable inference
- Privacy-preserving
- Efficient proof generation
"""

    meta1 = extract_metadata(content1, "zkml,research")

    assert len(meta1.title) > 0, "Title should not be empty"
    assert "ZKML" in meta1.title, "Title should contain 'ZKML'"
    assert len(meta1.summary) > 0, "Summary should not be empty"
    assert len(meta1.summary) <= 200, "Summary should be <= 200 chars"
    assert "zkml" in meta1.tags.lower(), "Tags should contain user tags"
    assert meta1.content_hash.startswith("0x"), "Hash should start with 0x"
    assert len(meta1.content_hash) == 66, "Hash should be 66 chars (0x + 64 hex)"

    print(f"✅ Title: {meta1.title}")
    print(f"✅ Summary: {meta1.summary[:80]}...")
    print(f"✅ Tags: {meta1.tags}")
    print(f"✅ Hash: {meta1.content_hash[:20]}...")

    # Test case 2: Plain text without heading
    content2 = "This is a simple note without any markdown formatting."
    meta2 = extract_metadata(content2, "")

    assert meta2.title == "This is a simple note without any markdown formatting.", "Should use first line as title"
    assert len(meta2.summary) > 0, "Summary should not be empty"

    print(f"✅ Plain text handling works")

    # Test case 3: Long content (truncation)
    content3 = "A" * 500
    meta3 = extract_metadata(content3, "")

    assert len(meta3.title) <= 100, "Title should be truncated to 100 chars"
    assert len(meta3.summary) <= 200, "Summary should be truncated to 200 chars"

    print(f"✅ Truncation works correctly")

    print("\n✅ All metadata extraction tests passed!")


def test_pydantic_models():
    """Test Pydantic models"""
    print("\n🧪 Testing Pydantic Models")
    print("="*50)

    # Test InsertRequest
    insert_req = InsertRequest(
        content="Test content",
        user_tags="test,example"
    )
    assert insert_req.content == "Test content"
    assert insert_req.user_tags == "test,example"
    print("✅ InsertRequest model works")

    # Test SearchRequest
    search_req = SearchRequest(
        query="test query",
        top_k=5
    )
    assert search_req.query == "test query"
    assert search_req.top_k == 5
    print("✅ SearchRequest model works")

    # Test Metadata
    meta = Metadata(
        title="Test Title",
        summary="Test summary",
        tags="test,tags",
        content_hash="0x" + "a" * 64
    )
    assert meta.title == "Test Title"
    assert len(meta.content_hash) == 66
    print("✅ Metadata model works")

    print("\n✅ All Pydantic model tests passed!")


def test_smart_contract_structure():
    """Verify smart contract exists and has correct structure"""
    print("\n🧪 Testing Smart Contract Structure")
    print("="*50)

    with open("contracts/KinicMemoryLog.sol", "r") as f:
        contract_code = f.read()

    # Check for key components
    assert "contract KinicMemoryLog" in contract_code, "Contract declaration exists"
    assert "struct Memory" in contract_code, "Memory struct exists"
    assert "function logMemory" in contract_code, "logMemory function exists"
    assert "string title" in contract_code, "Title field exists"
    assert "string summary" in contract_code, "Summary field exists"
    assert "string tags" in contract_code, "Tags field exists"
    assert "event MemoryLogged" in contract_code, "MemoryLogged event exists"

    print("✅ Contract has Memory struct")
    print("✅ Contract has logMemory function")
    print("✅ Contract has human-readable fields (title, summary, tags)")
    print("✅ Contract has events")

    print("\n✅ Smart contract structure is correct!")


def test_project_structure():
    """Verify all required files exist"""
    print("\n🧪 Testing Project Structure")
    print("="*50)

    import os

    required_files = [
        "src/main.py",
        "src/models.py",
        "src/metadata.py",
        "src/kinic_runner.py",
        "src/monad.py",
        "contracts/KinicMemoryLog.sol",
        "contracts/deploy.py",
        "requirements.txt",
        "Dockerfile",
        "render.yaml",
        ".env.example",
        "README.md",
        "QUICKSTART.md"
    ]

    for file_path in required_files:
        assert os.path.exists(file_path), f"{file_path} should exist"
        print(f"✅ {file_path}")

    print("\n✅ All required files exist!")


def test_hash_consistency():
    """Test that hash generation is consistent"""
    print("\n🧪 Testing Hash Consistency")
    print("="*50)

    content = "Test content for hashing"

    meta1 = extract_metadata(content, "")
    meta2 = extract_metadata(content, "")

    assert meta1.content_hash == meta2.content_hash, "Hash should be consistent"
    print(f"✅ Hash is consistent: {meta1.content_hash[:20]}...")

    # Different content should have different hash
    meta3 = extract_metadata(content + " different", "")
    assert meta1.content_hash != meta3.content_hash, "Different content should have different hash"
    print(f"✅ Different content has different hash")

    print("\n✅ Hash consistency tests passed!")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 KINIC MEMORY AGENT - BASIC TESTS")
    print("="*60)

    try:
        test_pydantic_models()
        test_metadata_extraction()
        test_hash_consistency()
        test_smart_contract_structure()
        test_project_structure()

        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\n📊 Test Summary:")
        print("  ✅ Pydantic models: Working")
        print("  ✅ Metadata extraction: Working")
        print("  ✅ Hash generation: Consistent")
        print("  ✅ Smart contract: Correctly structured")
        print("  ✅ Project structure: Complete")
        print("\n🎉 Your Kinic Memory Agent is ready to deploy!")
        print("\nNext steps:")
        print("  1. Set up environment: cp .env.example .env")
        print("  2. Deploy Monad contract: python contracts/deploy.py")
        print("  3. Create Kinic canister: ./kinic-cli/target/release/kinic-cli create")
        print("  4. Test locally: uvicorn src.main:app --reload")
        print("  5. Deploy to Render: Follow QUICKSTART.md")
        print("="*60 + "\n")

        sys.exit(0)

    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
