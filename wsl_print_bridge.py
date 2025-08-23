#!/usr/bin/env python3
"""
WSL-Windows Printing Bridge
Allows Linux applications in WSL to trigger Windows print events
Works on both Windows 10 and Windows 11 WSL
"""

import subprocess
import os
import tempfile
import json
from pathlib import Path
from typing import Dict, List, Optional, Union

class WSLPrintBridge:
    """Bridge for printing from WSL Linux to Windows printers"""
    
    def __init__(self):
        self.temp_dir = Path("/tmp/wsl_print_bridge")
        self.temp_dir.mkdir(exist_ok=True)
        self.windows_temp = "/mnt/c/temp/wsl_prints"
        self._ensure_windows_temp()
    
    def _ensure_windows_temp(self):
        """Ensure Windows temp directory exists"""
        try:
            subprocess.run([
                "powershell.exe", "-Command", 
                f"New-Item -ItemType Directory -Force -Path C:\\temp\\wsl_prints"
            ], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            print("Warning: Could not create Windows temp directory")
    
    def get_windows_printers(self) -> List[Dict[str, str]]:
        """Get list of available Windows printers"""
        try:
            result = subprocess.run([
                "powershell.exe", "-Command",
                "Get-Printer | Select-Object Name, Type, DriverName, PortName | ConvertTo-Json"
            ], capture_output=True, text=True, check=True)
            
            printers_data = json.loads(result.stdout)
            if isinstance(printers_data, dict):
                printers_data = [printers_data]  # Single printer case
                
            return printers_data
        except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
            print(f"Error getting printers: {e}")
            return []
    
    def print_text_file(self, file_path: Union[str, Path], printer_name: Optional[str] = None) -> bool:
        """Print a text file to Windows printer"""
        file_path = Path(file_path)
        if not file_path.exists():
            print(f"File not found: {file_path}")
            return False
        
        # Copy file to Windows accessible location
        windows_file_path = f"C:\\temp\\wsl_prints\\{file_path.name}"
        subprocess.run([
            "cp", str(file_path), f"/mnt/c/temp/wsl_prints/{file_path.name}"
        ], check=True)
        
        # Build PowerShell print command
        ps_command = f"Get-Content '{windows_file_path}' | Out-Printer"
        if printer_name:
            ps_command = f"Get-Content '{windows_file_path}' | Out-Printer -Name '{printer_name}'"
        
        try:
            result = subprocess.run([
                "powershell.exe", "-Command", ps_command
            ], capture_output=True, text=True, check=True)
            
            print(f"Successfully printed {file_path.name}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"Print failed: {e.stderr}")
            return False
    
    def print_pdf(self, pdf_path: Union[str, Path], printer_name: Optional[str] = None) -> bool:
        """Print PDF using Windows default PDF handler"""
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            print(f"PDF file not found: {pdf_path}")
            return False
        
        # Copy PDF to Windows location
        windows_pdf_path = f"C:\\temp\\wsl_prints\\{pdf_path.name}"
        subprocess.run([
            "cp", str(pdf_path), f"/mnt/c/temp/wsl_prints/{pdf_path.name}"
        ], check=True)
        
        # Use Windows shell to print PDF
        print_command = f"Start-Process -FilePath '{windows_pdf_path}' -Verb Print"
        if printer_name:
            # More complex PDF printing with specific printer
            print_command = f"""
$pdf = '{windows_pdf_path}'
$printer = '{printer_name}'
$reader = (Get-ItemProperty 'HKLM:\\SOFTWARE\\Classes\\.pdf' -Name '(default)' -ErrorAction SilentlyContinue).'(default)'
if ($reader) {{
    $app = (Get-ItemProperty "HKLM:\\SOFTWARE\\Classes\\$reader\\shell\\print\\command" -Name '(default)' -ErrorAction SilentlyContinue).'(default)'
    if ($app) {{
        $app = $app.Replace('%1', $pdf)
        Invoke-Expression $app
    }}
}}
"""
        
        try:
            result = subprocess.run([
                "powershell.exe", "-Command", print_command
            ], capture_output=True, text=True, check=True)
            
            print(f"Successfully sent PDF {pdf_path.name} to printer")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"PDF print failed: {e.stderr}")
            return False
    
    def print_command_output(self, command: List[str], printer_name: Optional[str] = None) -> bool:
        """Execute Linux command and print its output"""
        try:
            # Execute command and capture output
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            
            # Create temporary file with output
            temp_file = self.temp_dir / f"command_output_{os.getpid()}.txt"
            temp_file.write_text(result.stdout)
            
            # Print the output
            success = self.print_text_file(temp_file, printer_name)
            
            # Cleanup
            temp_file.unlink(missing_ok=True)
            
            return success
            
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {e}")
            return False
    
    def create_cups_to_windows_bridge(self, cups_printer_name: str, windows_printer_name: str):
        """Create a CUPS printer that bridges to Windows printer"""
        
        # Create CUPS backend script
        backend_script = f"""#!/bin/bash
# WSL-Windows Print Bridge Backend
# Usage: {cups_printer_name}-backend job-id user title copies options [file]

# Get print job details
JOB_ID="$1"
USER="$2" 
TITLE="$3"
COPIES="$4"
OPTIONS="$5"
FILE="$6"

# If no file provided, read from stdin
if [ -z "$FILE" ]; then
    FILE="/tmp/print_job_$JOB_ID.txt"
    cat > "$FILE"
fi

# Use Python bridge to print
python3 -c "
import sys
sys.path.append('/tmp/wsl_print_bridge')
from wsl_print_bridge import WSLPrintBridge
bridge = WSLPrintBridge()
bridge.print_text_file('$FILE', '{windows_printer_name}')
"

# Cleanup temp file if we created it
if [ "$FILE" == "/tmp/print_job_$JOB_ID.txt" ]; then
    rm -f "$FILE"
fi

exit 0
"""
        
        # Write backend script
        backend_path = Path("/usr/lib/cups/backend") / f"{cups_printer_name}-bridge"
        
        try:
            subprocess.run(["sudo", "mkdir", "-p", "/usr/lib/cups/backend"], check=True)
            
            with open("/tmp/bridge_backend.sh", "w") as f:
                f.write(backend_script)
            
            subprocess.run([
                "sudo", "cp", "/tmp/bridge_backend.sh", str(backend_path)
            ], check=True)
            
            subprocess.run([
                "sudo", "chmod", "+x", str(backend_path)
            ], check=True)
            
            # Add CUPS printer
            subprocess.run([
                "sudo", "lpadmin", "-p", cups_printer_name,
                "-v", f"{cups_printer_name}-bridge://localhost",
                "-m", "raw", "-E"
            ], check=True)
            
            print(f"Created CUPS printer '{cups_printer_name}' bridged to Windows printer '{windows_printer_name}'")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"Failed to create CUPS bridge: {e}")
            return False

class LinuxPrintController:
    """High-level controller for Linux applications to print via Windows"""
    
    def __init__(self):
        self.bridge = WSLPrintBridge()
        
    def setup_environment(self):
        """Setup printing environment"""
        print("🖨️  Setting up WSL-Windows printing bridge...")
        
        # Install required packages
        packages = ["cups", "cups-client", "python3", "python3-pip"]
        for package in packages:
            try:
                subprocess.run(["sudo", "apt", "install", "-y", package], 
                             check=True, capture_output=True)
            except subprocess.CalledProcessError:
                print(f"Warning: Could not install {package}")
        
        # Start CUPS service
        try:
            subprocess.run(["sudo", "service", "cups", "start"], check=True)
        except subprocess.CalledProcessError:
            print("Warning: Could not start CUPS service")
        
        print("✅ Environment setup complete")
    
    def list_available_printers(self):
        """List all available Windows printers"""
        print("\n🖨️  Available Windows Printers:")
        print("-" * 50)
        
        printers = self.bridge.get_windows_printers()
        for i, printer in enumerate(printers, 1):
            print(f"{i}. Name: {printer.get('Name', 'Unknown')}")
            print(f"   Type: {printer.get('Type', 'Unknown')}")
            print(f"   Driver: {printer.get('DriverName', 'Unknown')}")
            print(f"   Port: {printer.get('PortName', 'Unknown')}")
            print()
        
        return printers
    
    def print_from_linux(self, content: str, printer_name: Optional[str] = None, 
                        content_type: str = "text") -> bool:
        """Print content from Linux applications"""
        
        # Create temporary file
        temp_file = self.bridge.temp_dir / f"linux_print_{os.getpid()}.{content_type}"
        
        if content_type == "text":
            temp_file.write_text(content)
            return self.bridge.print_text_file(temp_file, printer_name)
        else:
            print(f"Unsupported content type: {content_type}")
            return False
    
    def demo_print_scenarios(self):
        """Demonstrate various printing scenarios"""
        print("\n🎯 Demonstrating WSL-Windows printing scenarios...")
        
        # Scenario 1: Print system information
        print("\n1. Printing system information...")
        success = self.bridge.print_command_output(["uname", "-a"])
        print(f"   Result: {'✅ Success' if success else '❌ Failed'}")
        
        # Scenario 2: Print directory listing
        print("\n2. Printing directory listing...")
        success = self.bridge.print_command_output(["ls", "-la", "/home"])
        print(f"   Result: {'✅ Success' if success else '❌ Failed'}")
        
        # Scenario 3: Print custom content
        print("\n3. Printing custom content...")
        custom_content = """
WSL-Windows Print Bridge Demo
============================

This document was generated from Linux WSL and printed to a Windows printer.

System Details:
- Generated at: $(date)
- From: $(hostname)
- User: $(whoami)
- WSL Version: $(wsl.exe --version 2>/dev/null || echo "WSL 1")

This demonstrates the successful bridging between Linux control and Windows printing.
        """
        success = self.print_from_linux(custom_content)
        print(f"   Result: {'✅ Success' if success else '❌ Failed'}")

# CLI Interface
def main():
    """Main CLI interface for the WSL printing bridge"""
    import argparse
    
    parser = argparse.ArgumentParser(description="WSL-Windows Printing Bridge")
    parser.add_argument("--setup", action="store_true", help="Setup printing environment")
    parser.add_argument("--list-printers", action="store_true", help="List Windows printers")
    parser.add_argument("--print-file", help="Print a text file")
    parser.add_argument("--print-pdf", help="Print a PDF file")
    parser.add_argument("--printer", help="Specific printer name to use")
    parser.add_argument("--demo", action="store_true", help="Run demo scenarios")
    parser.add_argument("--create-bridge", nargs=2, metavar=('CUPS_NAME', 'WIN_NAME'),
                       help="Create CUPS-to-Windows printer bridge")
    
    args = parser.parse_args()
    
    controller = LinuxPrintController()
    
    if args.setup:
        controller.setup_environment()
    
    if args.list_printers:
        controller.list_available_printers()
    
    if args.print_file:
        success = controller.bridge.print_text_file(args.print_file, args.printer)
        exit(0 if success else 1)
    
    if args.print_pdf:
        success = controller.bridge.print_pdf(args.print_pdf, args.printer)
        exit(0 if success else 1)
    
    if args.demo:
        controller.demo_print_scenarios()
    
    if args.create_bridge:
        cups_name, win_name = args.create_bridge
        success = controller.bridge.create_cups_to_windows_bridge(cups_name, win_name)
        exit(0 if success else 1)
    
    if not any(vars(args).values()):
        parser.print_help()

if __name__ == "__main__":
    main()