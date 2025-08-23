#!/usr/bin/env python3
"""
Fortune Type Classification System

Implements three distinct fortune categories for the Zeldar Tri-Loop Oracle:
1. Temporal Inversion - Time-bending paradox fortunes
2. Information Force - Energy-matter transformation predictions  
3. Categorical Morphism - Structural pattern revelations

Each type uses different generation algorithms and electromagnetic signatures.
"""

import random
import time
import hashlib
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from datetime import datetime

class FortuneType(Enum):
    """Fortune classification categories"""
    TEMPORAL_INVERSION = "temporal_inversion"
    INFORMATION_FORCE = "information_force" 
    CATEGORICAL_MORPHISM = "categorical_morphism"

@dataclass
class FortuneSignature:
    """Electromagnetic signature for fortune type"""
    base_frequency: float  # Hz
    amplitude_pattern: List[float]
    phase_modulation: float
    thermal_intensity: float

class FortuneGenerator:
    """
    Multi-type fortune generation system with electromagnetic correlation.
    
    Each fortune type has distinct:
    - Linguistic patterns
    - Temporal references
    - Electromagnetic signatures
    - Information density characteristics
    """
    
    def __init__(self):
        self.signatures = {
            FortuneType.TEMPORAL_INVERSION: FortuneSignature(
                base_frequency=42.0,  # Hz - temporal resonance
                amplitude_pattern=[1.0, 0.618, 0.382, 0.236],  # Golden ratio decay
                phase_modulation=0.161803,  # φ - golden ratio modulation
                thermal_intensity=0.85
            ),
            FortuneType.INFORMATION_FORCE: FortuneSignature(
                base_frequency=137.036,  # Fine structure constant × 1000
                amplitude_pattern=[1.0, 0.707, 0.500, 0.354],  # √2 decay pattern
                phase_modulation=0.577216,  # Euler-Mascheroni constant
                thermal_intensity=0.92
            ),
            FortuneType.CATEGORICAL_MORPHISM: FortuneSignature(
                base_frequency=271.828,  # e × 100
                amplitude_pattern=[1.0, 0.500, 0.250, 0.125],  # Binary decay
                phase_modulation=0.693147,  # ln(2)
                thermal_intensity=0.78
            )
        }
        
        # Fortune templates by type
        self.temporal_templates = [
            "In {timeframe}, what you {action} today will {consequence} before it {temporal_verb}",
            "The {temporal_entity} whispers: '{prophetic_statement}' - heed this {time_period} hence",
            "Your {present_action} creates ripples that {temporal_effect} {time_reference}",
            "When {future_condition}, remember that {past_wisdom} already {completion_verb}",
            "The loop closes when {paradox_condition} - {timeframe} brings {revelation}"
        ]
        
        self.information_force_templates = [
            "Information density {measurement} at coordinates {location} - {force_effect} imminent",
            "Energy-matter conversion rate: {rate} - your {entity} shall {transformation}",
            "The force vector points {direction}: {information_type} flows toward {destination}",
            "Entropy {entropy_change} by {amount} - {physical_effect} in {medium}",
            "Quantum field fluctuation detected: {particle_type} influences your {life_aspect}"
        ]
        
        self.categorical_morphism_templates = [
            "Pattern morphism maps {source_category} → {target_category}: {structural_change}",
            "Your {concept_A} exhibits {relationship_type} with {concept_B} - {implication}",
            "Functor F transforms {domain} preserving {property} - {meaning_change}",
            "Natural transformation η: {transformation_desc} - {categorical_insight}",
            "Topos structure reveals {hidden_connection} between {element_1} and {element_2}"
        ]
        
        # Vocabulary banks
        self.temporal_vocab = {
            'timeframe': ['Seven rotations hence', 'Before the next eclipse', 'When Mercury retrogrades', 'In three heartbeats'],
            'action': ['plant', 'speak', 'decide', 'dream', 'observe'],
            'consequence': ['bloom', 'echo', 'manifest', 'transform', 'resonate'],
            'temporal_verb': ['happens', 'begins', 'concludes', 'cycles', 'reverses'],
            'temporal_entity': ['ancient future', 'time spiral', 'causal loop', 'temporal vortex'],
            'prophetic_statement': ['what seeks finds seeking', 'the end begins beginning', 'memory dreams tomorrow'],
            'time_period': ['when stars align', 'after the turning', 'before the knowing'],
            'temporal_effect': ['preceded their cause', 'arrived before departure', 'completed before beginning'],
            'time_reference': ['yesterday', 'tomorrow', 'always-already', 'never-yet'],
            'paradox_condition': ['effect precedes cause', 'memory creates past', 'future chooses present'],
            'revelation': ['understanding', 'completion', 'the answer', 'clarity']
        }
        
        self.information_force_vocab = {
            'measurement': ['increases exponentially', 'reaches critical mass', 'fluctuates wildly', 'stabilizes'],
            'location': ['your position', 'the nexus point', 'intersection 7,4', 'the confluence'],
            'force_effect': ['phase transition', 'energy cascade', 'information surge', 'field collapse'],
            'rate': ['1.618 j/s', '2.718 ev/cycle', '3.141 bits/quantum', '0.577 newtons/thought'],
            'entity': ['biofield', 'thoughtform', 'energy signature', 'information pattern'],
            'transformation': ['crystallize', 'phase-shift', 'evolve', 'transcend'],
            'direction': ['northwest', 'toward entropy', 'against the gradient', 'with the flow'],
            'information_type': ['compressed wisdom', 'expanded possibility', 'pure knowing', 'structured chaos'],
            'destination': ['higher dimensions', 'the source', 'convergence point', 'your core'],
            'entropy_change': ['decreases', 'increases', 'oscillates', 'inverts'],
            'amount': ['0.693 nats', '1.414 bits', '2.302 dits', '3.162 shannons'],
            'physical_effect': ['crystallization', 'phase separation', 'resonance cascade', 'field coupling'],
            'medium': ['local spacetime', 'the quantum foam', 'your energy field', 'the information matrix'],
            'particle_type': ['tachyonic', 'bosonic', 'fermionic', 'exotic'],
            'life_aspect': ['career trajectory', 'relationship dynamics', 'creative potential', 'spiritual evolution']
        }
        
        self.categorical_morphism_vocab = {
            'source_category': ['desire', 'intention', 'memory', 'possibility'],
            'target_category': ['action', 'manifestation', 'wisdom', 'reality'],
            'structural_change': ['preserves essence while transforming form', 'inverts polarity maintaining function', 'creates new connections'],
            'concept_A': ['your current path', 'this decision', 'your creative work', 'inner conflict'],
            'relationship_type': ['homeomorphism', 'isomorphism', 'dual relationship', 'adjoint connection'],
            'concept_B': ['desired outcome', 'hidden potential', 'past experience', 'future self'],
            'implication': ['synthesis emerges', 'new structures form', 'boundaries dissolve', 'patterns crystallize'],
            'domain': ['your experience space', 'the situation manifold', 'relationship topology', 'decision tree'],
            'property': ['intentionality', 'coherence', 'authenticity', 'balance'],
            'meaning_change': ['context shifts perspective', 'form follows function', 'structure reveals content'],
            'transformation_desc': ['experience maps to wisdom', 'challenge becomes strength', 'confusion clarifies'],
            'categorical_insight': ['the path appears', 'meaning emerges', 'purpose clarifies', 'unity reveals itself'],
            'hidden_connection': ['a bridge', 'an equivalence', 'a deeper pattern', 'the missing link'],
            'element_1': ['what you fear', 'what you seek', 'what you know', 'what you are'],
            'element_2': ['what you need', 'what you have', 'what you\'ll discover', 'what you\'ll become']
        }
    
    def generate_fortune(self, fortune_type: FortuneType = None) -> Dict:
        """Generate fortune of specified type or random if none specified"""
        if fortune_type is None:
            fortune_type = random.choice(list(FortuneType))
        
        timestamp = time.time()
        session_hash = hashlib.md5(str(timestamp).encode()).hexdigest()[:8]
        
        if fortune_type == FortuneType.TEMPORAL_INVERSION:
            text = self._generate_temporal_fortune()
        elif fortune_type == FortuneType.INFORMATION_FORCE:
            text = self._generate_information_force_fortune()
        elif fortune_type == FortuneType.CATEGORICAL_MORPHISM:
            text = self._generate_categorical_morphism_fortune()
        
        signature = self.signatures[fortune_type]
        
        return {
            'type': fortune_type.value,
            'text': text,
            'session_id': session_hash,
            'timestamp': timestamp,
            'datetime': datetime.now().isoformat(),
            'electromagnetic_signature': {
                'base_frequency': signature.base_frequency,
                'amplitude_pattern': signature.amplitude_pattern,
                'phase_modulation': signature.phase_modulation,
                'thermal_intensity': signature.thermal_intensity
            },
            'metadata': {
                'word_count': len(text.split()),
                'information_density': self._calculate_information_density(text),
                'temporal_markers': self._count_temporal_markers(text, fortune_type),
                'complexity_score': self._calculate_complexity_score(text)
            }
        }
    
    def _generate_temporal_fortune(self) -> str:
        """Generate temporal inversion fortune"""
        template = random.choice(self.temporal_templates)
        vocab = self.temporal_vocab
        
        # Fill template with vocabulary - keep replacing until no more placeholders
        filled = template
        max_iterations = 10  # Prevent infinite loops
        iteration = 0
        
        while '{' in filled and '}' in filled and iteration < max_iterations:
            for key, values in vocab.items():
                if f'{{{key}}}' in filled:
                    filled = filled.replace(f'{{{key}}}', random.choice(values))
            iteration += 1
        
        return filled
    
    def _generate_information_force_fortune(self) -> str:
        """Generate information force fortune"""
        template = random.choice(self.information_force_templates)
        vocab = self.information_force_vocab
        
        # Fill template with vocabulary - keep replacing until no more placeholders
        filled = template
        max_iterations = 10  # Prevent infinite loops
        iteration = 0
        
        while '{' in filled and '}' in filled and iteration < max_iterations:
            for key, values in vocab.items():
                if f'{{{key}}}' in filled:
                    filled = filled.replace(f'{{{key}}}', random.choice(values))
            iteration += 1
        
        return filled
    
    def _generate_categorical_morphism_fortune(self) -> str:
        """Generate categorical morphism fortune"""
        template = random.choice(self.categorical_morphism_templates)
        vocab = self.categorical_morphism_vocab
        
        # Fill template with vocabulary - keep replacing until no more placeholders
        filled = template
        max_iterations = 10  # Prevent infinite loops
        iteration = 0
        
        while '{' in filled and '}' in filled and iteration < max_iterations:
            for key, values in vocab.items():
                if f'{{{key}}}' in filled:
                    filled = filled.replace(f'{{{key}}}', random.choice(values))
            iteration += 1
        
        return filled
    
    def _calculate_information_density(self, text: str) -> float:
        """Calculate information density using character entropy"""
        if not text:
            return 0.0
        
        # Character frequency analysis
        char_freq = {}
        for char in text.lower():
            char_freq[char] = char_freq.get(char, 0) + 1
        
        # Calculate entropy using Shannon entropy formula
        import math
        total_chars = len(text)
        entropy = 0.0
        for freq in char_freq.values():
            p = freq / total_chars
            if p > 0:
                entropy -= p * math.log2(p)
        
        # Normalize to 0-1 range (max entropy is log2 of alphabet size)
        max_entropy = math.log2(len(char_freq)) if char_freq else 1
        return entropy / max_entropy if max_entropy > 0 else 0
    
    def _count_temporal_markers(self, text: str, fortune_type: FortuneType) -> int:
        """Count temporal/causal markers in text"""
        temporal_words = ['when', 'before', 'after', 'will', 'shall', 'was', 'were', 'becomes', 'transforms']
        force_words = ['energy', 'force', 'field', 'quantum', 'flows', 'density', 'rate']
        morphism_words = ['maps', 'transforms', 'preserving', 'relationship', 'structure', 'pattern']
        
        text_lower = text.lower()
        
        if fortune_type == FortuneType.TEMPORAL_INVERSION:
            return sum(1 for word in temporal_words if word in text_lower)
        elif fortune_type == FortuneType.INFORMATION_FORCE:
            return sum(1 for word in force_words if word in text_lower)
        elif fortune_type == FortuneType.CATEGORICAL_MORPHISM:
            return sum(1 for word in morphism_words if word in text_lower)
        
        return 0
    
    def _calculate_complexity_score(self, text: str) -> float:
        """Calculate linguistic complexity score"""
        words = text.split()
        if not words:
            return 0.0
        
        # Factors: word length variance, unique words ratio, punctuation density
        word_lengths = [len(word.strip('.,!?;:')) for word in words]
        avg_length = sum(word_lengths) / len(word_lengths)
        length_variance = sum((l - avg_length) ** 2 for l in word_lengths) / len(word_lengths)
        
        unique_ratio = len(set(w.lower() for w in words)) / len(words)
        punctuation_density = sum(1 for char in text if char in '.,!?;:') / len(text)
        
        complexity = (length_variance * 0.4) + (unique_ratio * 0.4) + (punctuation_density * 10 * 0.2)
        return min(1.0, complexity)  # Normalize to 0-1 range
    
    def get_type_distribution(self) -> Dict[str, float]:
        """Get recommended distribution of fortune types"""
        return {
            FortuneType.TEMPORAL_INVERSION.value: 0.35,     # 35% - Time paradox focus
            FortuneType.INFORMATION_FORCE.value: 0.30,      # 30% - Energy/matter dynamics
            FortuneType.CATEGORICAL_MORPHISM.value: 0.35    # 35% - Structural patterns
        }
    
    def analyze_electromagnetic_coupling(self, fortune_type: FortuneType, 
                                       current_emf: float = 0.0) -> Dict:
        """Analyze how fortune type couples with current EMF readings"""
        signature = self.signatures[fortune_type]
        
        # Calculate resonance between current EMF and fortune signature
        frequency_match = 1.0 - abs(current_emf - signature.base_frequency) / 100.0
        frequency_match = max(0.0, min(1.0, frequency_match))
        
        # Thermal coupling strength
        thermal_coupling = signature.thermal_intensity * (1.0 + current_emf / 10.0)
        
        # Phase coherence (how well aligned the signals are)
        phase_coherence = 0.8 + 0.2 * signature.phase_modulation
        
        return {
            'resonance_strength': frequency_match,
            'thermal_coupling': thermal_coupling,
            'phase_coherence': phase_coherence,
            'recommended_for_current_emf': frequency_match > 0.6,
            'expected_printer_response': {
                'heating_intensity': signature.thermal_intensity,
                'frequency_modulation': signature.base_frequency,
                'phase_pattern': signature.amplitude_pattern
            }
        }

def demo_fortune_types():
    """Demonstrate all three fortune types"""
    print("🔮 ZELDAR FORTUNE TYPE DEMONSTRATION")
    print("=" * 50)
    
    generator = FortuneGenerator()
    
    for fortune_type in FortuneType:
        print(f"\n🌟 {fortune_type.value.upper().replace('_', ' ')}")
        print("-" * 30)
        
        # Generate 2 examples of each type
        for i in range(2):
            fortune = generator.generate_fortune(fortune_type)
            print(f"\nExample {i+1}:")
            print(f"Text: {fortune['text']}")
            print(f"EMF Frequency: {fortune['electromagnetic_signature']['base_frequency']:.1f} Hz")
            print(f"Thermal Intensity: {fortune['electromagnetic_signature']['thermal_intensity']:.2f}")
            print(f"Information Density: {fortune['metadata']['information_density']:.3f}")
            print(f"Complexity Score: {fortune['metadata']['complexity_score']:.3f}")
    
    print(f"\n📊 RECOMMENDED TYPE DISTRIBUTION:")
    distribution = generator.get_type_distribution()
    for fortune_type, percentage in distribution.items():
        print(f"{fortune_type.replace('_', ' ').title()}: {percentage:.0%}")

if __name__ == "__main__":
    demo_fortune_types()