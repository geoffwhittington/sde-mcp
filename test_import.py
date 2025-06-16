#!/usr/bin/env python3
"""Simple test to verify the package imports correctly."""

import sys
import os

# Add the src directory to Python path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported."""
    try:
        # Test package import
        import sde_mcp_server
        print(f"✓ Package imported successfully: {sde_mcp_server.__version__}")
        
        # Test individual modules
        from sde_mcp_server import api_client
        print("✓ API client module imported successfully")
        
        from sde_mcp_server import server
        print("✓ Server module imported successfully")
        
        # Test that main function exists
        from sde_mcp_server.server import main
        print("✓ Main function found")
        
        # Test entry point
        from sde_mcp_server.__main__ import main_entry
        print("✓ Entry point function found")
        
        print("\n🎉 All imports successful! Package structure is correct.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1) 