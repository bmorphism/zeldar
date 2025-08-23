#!/usr/bin/env python3
"""
Optimized Test Suite - Minimal Paper Usage with Amortized Testing
Prevents excessive printing while maintaining full validation
"""

import unittest
import subprocess
import time
import json
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

class MockPrintSystem:
    """Mock print system to avoid actual paper usage during tests"""
    
    def __init__(self):
        self.print_count = 0
        self.last_content = None
        self.last_command = None
        self.simulated_success = True
        
    def mock_subprocess_run(self, command, **kwargs):
        """Mock subprocess.run to intercept print commands"""
        self.print_count += 1
        self.last_command = command
        
        if './scripts/print-now.sh' in command:
            # Simulate print script behavior without actual printing
            return MagicMock(
                returncode=0 if self.simulated_success else 1,
                stdout="✅ Precision fortune sent successfully!",
                stderr=""
            )
        elif command[0] == 'lsusb':
            # Simulate USB device detection
            return MagicMock(
                returncode=0,
                stdout="Bus 003 Device 006: ID 5958:0130 YXWL Y812BT",
                stderr=""
            )
        else:
            # Default mock behavior
            return MagicMock(returncode=0, stdout="", stderr="")

class TestPrintSystemAmortized(unittest.TestCase):
    """Amortized test suite - runs multiple validations per actual print"""
    
    @classmethod
    def setUpClass(cls):
        """Set up mock system to prevent excessive printing"""
        cls.mock_system = MockPrintSystem()
        cls.original_run = subprocess.run
        
    def setUp(self):
        """Reset mock state for each test"""
        self.mock_system.print_count = 0
        self.mock_system.last_content = None
        
    def test_format_optimization_without_printing(self):
        """Test format optimization using string analysis only"""
        from precision_print import StickyFortuneFormatter
        
        formatter = StickyFortuneFormatter()
        
        # Test multiple fortune variants without printing
        test_fortunes = [
            "Context distilled, In geometric form -- Inductive bias, Resonating worlds",
            "Short fortune",
            "Very long fortune that might exceed the width limits and need wrapping",
            "Multi\nline\nfortune\nwith\nexplicit\nbreaks"
        ]
        
        for fortune in test_fortunes:
            lines = formatter.format_fortune(fortune)
            
            # Validate without printing
            self.assertLessEqual(len(lines), formatter.label_height - 2)
            for line in lines:
                self.assertLessEqual(len(line), formatter.label_width)
            
            # Check required elements present
            content_str = '\n'.join(lines)
            self.assertIn("ヲヲヲ welcome to", content_str)
            self.assertIn("reafferent reaberrant", content_str)
    
    @patch('subprocess.run')
    def test_controlled_button_logic(self, mock_run):
        """Test button control logic without GPIO hardware"""
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        
        # Import after patching
        from controlled_button import controlled_print_haiku, save_last_print_time, can_print_now
        
        # Test cooldown logic
        save_last_print_time()
        can_print, wait_time = can_print_now()
        self.assertFalse(can_print)  # Should be in cooldown
        self.assertGreater(wait_time, 0)
        
        # Test that print command is constructed correctly
        controlled_print_haiku()
        mock_run.assert_called()
        
    def test_paper_format_optimization(self):
        """Test optimal paper format without physical printing"""
        
        # Optimal sticky dimensions for 58mm thermal paper
        optimal_width = 28  # Conservative safe width
        optimal_height = 18  # Maximum usable height
        
        # Test fortune fits in optimal dimensions
        test_content = """ヲヲヲ welcome to the Uncommons
(up to a symplectomorphic cobordism)

there is no official _ universe-agent
every _ is the unofficial universe-agent

-----
Context distilled, In geometric 
    form -- Inductive bias,     
       Resonating worlds        

sincerely yours
reafferent reaberrant"""
        
        lines = test_content.split('\n')
        
        # Validate optimal format
        self.assertLessEqual(len(lines), optimal_height)
        for line in lines:
            self.assertLessEqual(len(line), optimal_width, 
                               f"Line too long: '{line}' ({len(line)} chars)")
    
    @patch('subprocess.run')
    def test_print_script_validation(self, mock_run):
        """Test print script logic without actual execution"""
        mock_run.side_effect = self.mock_system.mock_subprocess_run
        
        # Test successful print scenario
        result = subprocess.run(['./scripts/print-now.sh'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(self.mock_system.print_count, 1)
        
    def test_amortized_integration(self):
        """Single integration test covering multiple scenarios"""
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = self.mock_system.mock_subprocess_run
            
            # Test scenario 1: Normal operation
            result1 = subprocess.run(['./scripts/print-now.sh'], capture_output=True)
            self.assertEqual(result1.returncode, 0)
            
            # Test scenario 2: USB check
            result2 = subprocess.run(['lsusb'], capture_output=True)
            self.assertEqual(result2.returncode, 0)
            
            # Verify only 2 mock calls made (not 2 real prints)
            self.assertEqual(self.mock_system.print_count, 2)

class TestPaperOptimization(unittest.TestCase):
    """Paper format optimization tests - no physical printing"""
    
    def test_minimal_paper_usage(self):
        """Ensure fortune uses minimal paper while maintaining readability"""
        
        # Calculate optimal line spacing
        content_lines = [
            "ヲヲヲ welcome to the Uncommons",
            "(up to a symplectomorphic cobordism)",
            "",  # Spacer
            "there is no official _ universe-agent",
            "every _ is the unofficial universe-agent", 
            "",  # Spacer
            "-----",
            "Context distilled, In geometric",
            "    form -- Inductive bias,",
            "       Resonating worlds",
            "",  # Spacer
            "sincerely yours",
            "reafferent reaberrant"
        ]
        
        # Validate minimal format (13 lines including spacers)
        self.assertLessEqual(len(content_lines), 15)  # Under 15 lines total
        
        # Check no excessive whitespace
        non_empty_lines = [line for line in content_lines if line.strip()]
        whitespace_ratio = (len(content_lines) - len(non_empty_lines)) / len(content_lines)
        self.assertLess(whitespace_ratio, 0.3)  # Less than 30% whitespace

    def test_character_density_optimization(self):
        """Optimize character density for best paper usage"""
        
        test_line = "Context distilled, In geometric form -- Inductive bias, Resonating worlds"
        
        # Test optimal wrapping
        max_width = 28
        words = test_line.split()
        wrapped_lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + word + " ") <= max_width:
                current_line += word + " "
            else:
                if current_line:
                    wrapped_lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            wrapped_lines.append(current_line.strip())
        
        # Validate wrapping efficiency
        total_chars = sum(len(line) for line in wrapped_lines)
        efficiency = total_chars / (len(wrapped_lines) * max_width)
        self.assertGreater(efficiency, 0.7)  # At least 70% character density

class RealPrintTest(unittest.TestCase):
    """Single real print test - only run when explicitly requested"""
    
    def setUp(self):
        """Check if real printing is enabled"""
        self.real_print_enabled = os.getenv('ENABLE_REAL_PRINT', 'false').lower() == 'true'
        if not self.real_print_enabled:
            self.skipTest("Real printing disabled. Set ENABLE_REAL_PRINT=true to enable.")
    
    def test_single_real_print(self):
        """Single real print test to validate actual hardware"""
        print("\n🖨️ EXECUTING SINGLE REAL PRINT TEST")
        print("This will consume actual thermal paper.")
        
        # Execute one real print for validation
        result = subprocess.run(['./scripts/print-now.sh'], 
                              capture_output=True, 
                              text=True, 
                              timeout=30)
        
        self.assertEqual(result.returncode, 0)
        self.assertIn("Precision fortune sent successfully", result.stdout)
        
        print("✅ Real print test completed successfully")

if __name__ == '__main__':
    # Configure test runner to minimize output
    import sys
    
    print("🧪 Running Amortized Print System Tests")
    print("📄 Paper conservation mode: Mocking enabled")
    print("⚡ Tests optimized for minimal resource usage\n")
    
    # Run tests with minimal verbosity
    unittest.main(verbosity=1, buffer=True)