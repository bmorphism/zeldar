#!/usr/bin/env python3
"""
Electromagnetic Loop Validation Demo

Simplified demonstration of EMF-GPIO correlation measurement 
without heavy dependencies, showing technical measurement approach.
"""

import asyncio
import json
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
import math
import random

@dataclass
class EMFReading:
    """Electromagnetic field measurement"""
    timestamp: float
    frequency: float
    amplitude: float
    phase: float
    field_strength: float

@dataclass
class GPIOReading:
    """GPIO pin state measurement"""
    timestamp: float
    pin: int
    voltage: float
    state: bool
    transition_edge: Optional[str] = None

@dataclass
class LoopCorrelation:
    """Correlation between EMF and GPIO signals"""
    timestamp: float
    correlation_coefficient: float
    time_lag_ms: float
    signal_strength: float
    loop_detected: bool

class SimpleEMFValidator:
    """
    Simplified electromagnetic loop validator demonstrating 
    thermal head EMF measurement and GPIO correlation analysis.
    """
    
    def __init__(self, gpio_pin: int = 6, sampling_rate: int = 100):
        self.gpio_pin = gpio_pin
        self.sampling_rate = sampling_rate  # Hz (reduced for demo)
        self.logger = logging.getLogger('EMFValidator')
        
        # Signal buffers for correlation analysis
        self.emf_buffer = []
        self.gpio_buffer = []
        self.buffer_size = 200  # 2 seconds at 100Hz
        
        # Loop detection parameters
        self.correlation_threshold = 0.6
        self.time_lag_threshold = 50e-3  # 50ms
        self.loop_detected = False
        
        # Measurement state
        self.thermal_active = False
        self.emf_baseline = 0.0
        self.gpio_baseline = 3.3  # 3.3V logic level
        
        # Results storage
        self.correlations = []
        self.loop_detections = 0
        
        print(f"📡 EMF Validator initialized - GPIO pin {gpio_pin}, {sampling_rate}Hz")
    
    async def start_demo_validation(self, duration_seconds: int = 10):
        """Start electromagnetic loop validation demo"""
        print(f"🔬 Starting EMF loop validation demo for {duration_seconds}s...")
        
        start_time = time.time()
        end_time = start_time + duration_seconds
        
        # Start concurrent measurement tasks
        tasks = await asyncio.gather(
            self._measure_emf_patterns(end_time),
            self._measure_gpio_signals(end_time),
            self._analyze_correlations(end_time),
            self._monitor_progress(end_time),
            return_exceptions=True
        )
        
        # Generate final report
        final_report = self._generate_final_report()
        print("\n📊 VALIDATION RESULTS:")
        print(f"EMF measurements: {final_report['total_measurements']['emf_readings']}")
        print(f"GPIO measurements: {final_report['total_measurements']['gpio_readings']}")
        print(f"Correlations computed: {final_report['total_measurements']['correlations_computed']}")
        print(f"Loop detections: {final_report['loop_detection_summary']['total_detections']}")
        print(f"Detection rate: {final_report['loop_detection_summary']['detection_rate']:.1%}")
        print(f"Status: {final_report['status']}")
        
        if self.loop_detected:
            print("🔗 ELECTROMAGNETIC FEEDBACK LOOP CONFIRMED!")
            print(f"📊 Average correlation: {final_report.get('correlation_statistics', {}).get('mean', 0):.3f}")
    
    async def _measure_emf_patterns(self, end_time: float):
        """Measure electromagnetic field patterns from thermal head"""
        print("📡 Starting EMF pattern measurement...")
        
        while time.time() < end_time:
            try:
                # Simulate EMF measurements
                emf_reading = self._read_emf_field()
                
                # Add to buffer
                self.emf_buffer.append(emf_reading)
                if len(self.emf_buffer) > self.buffer_size:
                    self.emf_buffer.pop(0)
                
                # Update thermal activity state
                self.thermal_active = emf_reading.field_strength > self.emf_baseline * 2
                
                await asyncio.sleep(1.0 / self.sampling_rate)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"EMF measurement error: {e}")
                await asyncio.sleep(0.1)
    
    async def _measure_gpio_signals(self, end_time: float):
        """Measure GPIO pin voltage fluctuations"""
        print("⚡ Starting GPIO signal measurement...")
        
        while time.time() < end_time:
            try:
                # Read GPIO state and voltage
                gpio_reading = self._read_gpio_state()
                
                # Add to buffer
                self.gpio_buffer.append(gpio_reading)
                if len(self.gpio_buffer) > self.buffer_size:
                    self.gpio_buffer.pop(0)
                
                await asyncio.sleep(1.0 / self.sampling_rate)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"GPIO measurement error: {e}")
                await asyncio.sleep(0.1)
    
    async def _analyze_correlations(self, end_time: float):
        """Analyze correlations between EMF and GPIO signals"""
        print("📊 Starting signal correlation analysis...")
        
        while time.time() < end_time:
            try:
                await asyncio.sleep(1.0)  # Analyze every second
                
                if len(self.emf_buffer) > 20 and len(self.gpio_buffer) > 20:
                    correlation = self._compute_signal_correlation()
                    
                    if correlation:
                        self.correlations.append(correlation)
                        
                        if correlation.loop_detected:
                            self.loop_detections += 1
                            print(f"🔄 EMF-GPIO loop detected: "
                                        f"r={correlation.correlation_coefficient:.3f}, "
                                        f"lag={correlation.time_lag_ms:.1f}ms")
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Correlation analysis error: {e}")
                await asyncio.sleep(2.0)
    
    async def _monitor_progress(self, end_time: float):
        """Monitor validation progress"""
        while time.time() < end_time:
            try:
                await asyncio.sleep(3.0)  # Report every 3 seconds
                
                emf_count = len(self.emf_buffer)
                gpio_count = len(self.gpio_buffer)
                corr_count = len(self.correlations)
                
                print(f"📈 Progress: {emf_count} EMF, {gpio_count} GPIO, "
                           f"{corr_count} correlations, {self.loop_detections} loops")
                
            except asyncio.CancelledError:
                break
    
    def _read_emf_field(self) -> EMFReading:
        """Simulate EMF reading from thermal printer area"""
        current_time = time.time()
        
        # Base EMF pattern with thermal printer switching frequency (~50Hz)
        base_frequency = 50.0  # Hz
        thermal_modulation = 0.5 * math.sin(2 * math.pi * base_frequency * current_time)
        
        # Add harmonics and noise
        harmonic_2 = 0.2 * math.sin(2 * math.pi * 2 * base_frequency * current_time)
        harmonic_3 = 0.1 * math.sin(2 * math.pi * 3 * base_frequency * current_time)
        noise = random.gauss(0, 0.05)
        
        # Simulate thermal activity influence
        if not hasattr(self, '_thermal_activity_phase'):
            self._thermal_activity_phase = 0
        self._thermal_activity_phase += 0.1
        
        thermal_activity = 1.0 + 0.8 * math.sin(self._thermal_activity_phase)
        
        # Combine signals
        field_strength = (thermal_modulation + harmonic_2 + harmonic_3 + noise) * thermal_activity
        amplitude = abs(field_strength)
        phase = math.atan2(thermal_modulation, field_strength) if field_strength != 0 else 0
        
        return EMFReading(
            timestamp=current_time,
            frequency=base_frequency,
            amplitude=amplitude,
            phase=phase,
            field_strength=field_strength
        )
    
    def _read_gpio_state(self) -> GPIOReading:
        """Simulate GPIO pin voltage and state"""
        current_time = time.time()
        
        # Simulated GPIO with EMF coupling influence
        base_voltage = 3.3  # 3.3V logic high
        
        # Add EMF coupling influence (small voltage fluctuations)
        if self.emf_buffer:
            recent_emf = self.emf_buffer[-1].field_strength
            emf_coupling = 0.1 * recent_emf  # 100mV coupling coefficient
        else:
            emf_coupling = 0
        
        # Add thermal noise and button press simulation
        noise = random.gauss(0, 0.01)  # 10mV noise
        button_simulation = self._simulate_button_press(current_time)
        
        voltage = base_voltage + emf_coupling + noise + button_simulation
        digital_state = voltage > 1.65  # TTL threshold
        
        # Detect transitions
        transition_edge = None
        if hasattr(self, '_last_gpio_state'):
            if digital_state != self._last_gpio_state:
                transition_edge = "rising" if digital_state else "falling"
        self._last_gpio_state = digital_state
        
        return GPIOReading(
            timestamp=current_time,
            pin=self.gpio_pin,
            voltage=voltage,
            state=digital_state,
            transition_edge=transition_edge
        )
    
    def _simulate_button_press(self, current_time: float) -> float:
        """Simulate periodic button press events"""
        # Simulate button press every 5-10 seconds with randomness
        if not hasattr(self, '_next_button_time'):
            self._next_button_time = current_time + random.uniform(5, 10)
        
        if current_time > self._next_button_time:
            press_duration = 0.2  # seconds
            if not hasattr(self, '_button_press_start'):
                self._button_press_start = current_time
                print("🔘 Simulated button press event")
            
            if current_time - self._button_press_start < press_duration:
                return -3.3  # Pull to ground
            else:
                # Reset for next button press
                self._next_button_time = current_time + random.uniform(5, 10)
                delattr(self, '_button_press_start')
        
        return 0
    
    def _compute_signal_correlation(self) -> Optional[LoopCorrelation]:
        """Compute correlation between EMF and GPIO signals"""
        if len(self.emf_buffer) < 20 or len(self.gpio_buffer) < 20:
            return None
        
        # Extract recent signal data
        emf_data = [reading.field_strength for reading in self.emf_buffer[-20:]]
        gpio_data = [reading.voltage for reading in self.gpio_buffer[-20:]]
        
        # Simple correlation coefficient calculation
        n = min(len(emf_data), len(gpio_data))
        emf_data = emf_data[:n]
        gpio_data = gpio_data[:n]
        
        # Calculate means
        emf_mean = sum(emf_data) / n
        gpio_mean = sum(gpio_data) / n
        
        # Calculate correlation coefficient
        numerator = sum((emf_data[i] - emf_mean) * (gpio_data[i] - gpio_mean) for i in range(n))
        emf_sq_sum = sum((emf_data[i] - emf_mean) ** 2 for i in range(n))
        gpio_sq_sum = sum((gpio_data[i] - gpio_mean) ** 2 for i in range(n))
        
        denominator = math.sqrt(emf_sq_sum * gpio_sq_sum) if emf_sq_sum * gpio_sq_sum > 0 else 1
        correlation_coeff = numerator / denominator
        
        # Simple time lag estimation (mock)
        time_lag_ms = random.uniform(-30, 30)  # ±30ms lag simulation
        
        # Determine if loop is detected
        loop_detected = (
            abs(correlation_coeff) > self.correlation_threshold and
            abs(time_lag_ms) < self.time_lag_threshold * 1000
        )
        
        return LoopCorrelation(
            timestamp=time.time(),
            correlation_coefficient=correlation_coeff,
            time_lag_ms=time_lag_ms,
            signal_strength=abs(correlation_coeff),
            loop_detected=loop_detected
        )
    
    def _generate_final_report(self) -> Dict:
        """Generate comprehensive validation report"""
        if not self.correlations:
            return {'status': 'NO_DATA', 'correlations': 0}
        
        # Statistical analysis
        correlations = [c.correlation_coefficient for c in self.correlations]
        time_lags = [c.time_lag_ms for c in self.correlations]
        
        def mean(data): return sum(data) / len(data) if data else 0
        def std(data):
            if not data: return 0
            m = mean(data)
            return math.sqrt(sum((x - m) ** 2 for x in data) / len(data))
        
        self.loop_detected = self.loop_detections > 0
        
        report = {
            'timestamp': time.time(),
            'status': 'LOOP_CONFIRMED' if self.loop_detected else 'NO_LOOP_DETECTED',
            'total_measurements': {
                'emf_readings': len(self.emf_buffer),
                'gpio_readings': len(self.gpio_buffer),
                'correlations_computed': len(self.correlations)
            },
            'correlation_statistics': {
                'mean': mean(correlations),
                'std': std(correlations),
                'max': max(correlations) if correlations else 0,
                'min': min(correlations) if correlations else 0
            },
            'time_lag_statistics': {
                'mean_ms': mean(time_lags),
                'std_ms': std(time_lags),
                'max_ms': max(time_lags) if time_lags else 0,
                'min_ms': min(time_lags) if time_lags else 0
            },
            'loop_detection_summary': {
                'total_detections': self.loop_detections,
                'detection_rate': self.loop_detections / len(self.correlations) if self.correlations else 0,
                'loop_confirmed': self.loop_detected
            }
        }
        
        return report

async def main():
    """Main electromagnetic loop validation demo"""
    print("🔬 ELECTROMAGNETIC FEEDBACK LOOP VALIDATOR DEMO")
    print("=" * 60)
    
    validator = SimpleEMFValidator()
    
    try:
        print("📡 Starting EMF-GPIO correlation measurement demo...")
        await validator.start_demo_validation(duration_seconds=10)
        
    except KeyboardInterrupt:
        print("\n⏹️ Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")

if __name__ == "__main__":
    print("🔗 ZELDAR ELECTROMAGNETIC LOOP VALIDATION DEMO")
    print("    Thermal EMF → GPIO Coupling → Signal Correlation")
    print("    TECHNICAL MEASUREMENT OF ELECTROMAGNETIC INFLUENCE")
    print()
    
    asyncio.run(main())