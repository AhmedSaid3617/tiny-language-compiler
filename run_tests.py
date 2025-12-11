#!/usr/bin/env python3
"""
Run all tests for the TINY parser project.
"""

import sys
import os
import subprocess

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_command(description, command):
    """Run a command and report results."""
    print(f"\n{'=' * 70}")
    print(f"🔧 {description}")
    print('=' * 70)
    
    result = subprocess.run(
        command,
        shell=True,
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    
    return result.returncode == 0


def main():
    """Run all tests and checks."""
    print("=" * 70)
    print("TINY Parser - Running All Tests")
    print("=" * 70)
    
    results = []
    
    # Test 1: Integration tests
    success = run_command(
        "Integration Tests",
        "python test/integration_test.py"
    )
    results.append(("Integration Tests", success))
    
    # Test 2: Unit tests (if pytest is available)
    print(f"\n{'=' * 70}")
    print("🔧 Unit Tests (pytest)")
    print('=' * 70)
    try:
        result = subprocess.run(
            "pytest -v",
            shell=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        success = result.returncode == 0
    except:
        print("⚠️  pytest not found - skipping unit tests")
        success = None
    results.append(("Unit Tests (pytest)", success))
    
    # Test 3: Demo run
    success = run_command(
        "Demo Script",
        "python demo.py"
    )
    results.append(("Demo Script", success))
    
    # Summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    
    for test_name, success in results:
        if success is True:
            print(f"✓ {test_name}: PASSED")
        elif success is False:
            print(f"✗ {test_name}: FAILED")
        else:
            print(f"⊘ {test_name}: SKIPPED")
    
    print("=" * 70)
    
    # Overall result
    failed = [name for name, success in results if success is False]
    if failed:
        print(f"\n❌ {len(failed)} test(s) failed: {', '.join(failed)}")
        return 1
    else:
        print("\n✅ All tests passed!")
        print("\n🎉 The TINY parser is ready to use!")
        print("\nRun the GUI application with: python main.py")
        return 0


if __name__ == "__main__":
    sys.exit(main())
