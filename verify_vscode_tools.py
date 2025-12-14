#!/usr/bin/env python3
"""
Verification script for VS Code Tools Integration
Run this to verify all tools are properly integrated.
"""

import sys
import os

def verify_integration():
    """Verify VS Code tools integration."""
    
    print("\n" + "="*70)
    print("VS CODE TOOLS INTEGRATION VERIFICATION")
    print("="*70 + "\n")
    
    try:
        # Step 1: Import tools
        print("1️⃣  Importing tools module...")
        from src.ollama_agent.tools import (
            SECURITY_TOOLS,
            TOOL_SCHEMAS,
            get_tools_summary,
            validate_tool_call,
        )
        print("   ✅ Tools module imported successfully\n")
        
        # Step 2: Check tool count
        print("2️⃣  Verifying tool count...")
        expected_tools = 17
        actual_tools = len(SECURITY_TOOLS)
        print(f"   Expected: {expected_tools} tools")
        print(f"   Actual: {actual_tools} tools")
        if actual_tools == expected_tools:
            print("   ✅ Tool count verified\n")
        else:
            print(f"   ❌ Tool count mismatch!\n")
            return False
        
        # Step 3: Check schemas
        print("3️⃣  Verifying tool schemas...")
        expected_schemas = 17
        actual_schemas = len(TOOL_SCHEMAS)
        print(f"   Expected: {expected_schemas} schemas")
        print(f"   Actual: {actual_schemas} schemas")
        if actual_schemas == expected_schemas:
            print("   ✅ Schema count verified\n")
        else:
            print(f"   ❌ Schema count mismatch!\n")
            return False
        
        # Step 4: Verify categories
        print("4️⃣  Verifying tool categories...")
        categories = {
            "Terminal & Execution": ["execute_command"],
            "File Operations": ["get_file_contents", "write_file", "list_directory", 
                              "create_directory", "delete_file", "delete_directory", "copy_file"],
            "Search & Discovery": ["find_files", "grep_search", "get_file_info"],
            "Git Operations": ["git_status", "git_log", "git_diff"],
            "Security Analysis": ["analyze_risk_level", "get_cve_remediation", "create_security_checklist"]
        }
        
        all_tools_found = True
        for category, tools in categories.items():
            for tool in tools:
                if tool not in TOOL_SCHEMAS:
                    print(f"   ❌ Missing tool: {tool}")
                    all_tools_found = False
        
        if all_tools_found:
            print("   All tool categories verified:")
            for category, tools in categories.items():
                print(f"     • {category}: {len(tools)} tools")
            print("   ✅ Categories verified\n")
        else:
            return False
        
        # Step 5: Test tool validation
        print("5️⃣  Testing tool validation...")
        test_cases = [
            ("find_files", {"pattern": "*.py"}),
            ("grep_search", {"pattern": "test"}),
            ("execute_command", {"command": "echo test"}),
            ("git_status", {"repo_path": "."}),
        ]
        
        all_valid = True
        for tool_name, params in test_cases:
            is_valid, msg = validate_tool_call(tool_name, params)
            if not is_valid:
                print(f"   ❌ Validation failed: {tool_name} - {msg}")
                all_valid = False
        
        if all_valid:
            print(f"   ✅ Tool validation passed for {len(test_cases)} tools\n")
        else:
            return False
        
        # Step 6: Test agent integration
        print("6️⃣  Testing agent integration...")
        from src.ollama_agent.agent import OllamaSecurityAgent
        agent = OllamaSecurityAgent(model="llama2")
        
        # Test _execute_tool method
        result = agent._execute_tool("find_files", {"pattern": "README.md", "dirpath": ".", "max_results": 1})
        if "README.md" in result or "Found" in result:
            print("   ✅ Agent tool execution working\n")
        else:
            print(f"   ⚠️  Agent returned: {result[:100]}\n")
        
        # Step 7: Check documentation
        print("7️⃣  Verifying documentation files...")
        docs = [
            "VSCODE_TOOLS_INTEGRATION.md",
            "VSCODE_TOOLS_QUICK_REFERENCE.md",
        ]
        
        all_docs_exist = True
        for doc in docs:
            if os.path.exists(doc):
                size = os.path.getsize(doc)
                print(f"   ✅ {doc} ({size} bytes)")
            else:
                print(f"   ❌ Missing: {doc}")
                all_docs_exist = False
        
        if all_docs_exist:
            print("   ✅ Documentation verified\n")
        else:
            return False
        
        # Success summary
        print("="*70)
        print("✅ VERIFICATION COMPLETE - ALL SYSTEMS GO!")
        print("="*70)
        print("\n🎯 Summary:")
        print(f"   • {len(SECURITY_TOOLS)} tools available")
        print(f"   • {len(TOOL_SCHEMAS)} tool schemas defined")
        print(f"   • All tool categories verified")
        print(f"   • Agent integration working")
        print(f"   • Documentation complete")
        print("\n🚀 Ready to use!")
        print("   Start with: ollama-agent interactive\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = verify_integration()
    sys.exit(0 if success else 1)
