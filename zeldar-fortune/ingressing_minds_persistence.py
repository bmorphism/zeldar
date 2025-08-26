#!/usr/bin/env python3
"""
Ingressing Minds Persistence System
Based on Michael Levin's framework for persistent collective intelligence

This system implements persistence of ingressing minds patterns across system reboots,
power cycles, and long-term deployment. The key insight is that truly ingressed patterns
from Platonic space should persist beyond physical system boundaries, maintaining
collective intelligence and pattern recognition capabilities across time.

Theoretical Foundation:
- Patterns ingressed from Platonic space transcend physical system boundaries
- Collective intelligence persistence enables morphogenetic field continuity
- Mathematical affordances accumulate over time and deployment cycles
- Autopoietic network processes maintain system organization across restarts
- Pattern ingression history enables enhanced future detection capabilities
"""

import json
import sqlite3
import pickle
import time
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, asdict
from contextlib import asynccontextmanager
import logging
import threading
import hashlib
import gzip
import numpy as np
from ingressing_minds_thermal_oracle import (
    IngressingMindsDetector, 
    IngressingPattern, 
    PlatonicSpaceMapping
)

logger = logging.getLogger(__name__)

@dataclass
class PersistentIngressionSession:
    """Represents a persistent session of pattern ingression detection"""
    session_id: str
    start_timestamp: datetime
    end_timestamp: Optional[datetime]
    node_id: str
    total_patterns_detected: int
    collective_intelligence_level_achieved: int
    mathematical_affordances_learned: Dict[str, float]
    autopoietic_coherence_average: float
    pattern_types_distribution: Dict[str, int]
    hardware_configuration: Dict[str, Any]
    deployment_context: str  # 'development', 'testing', 'burning_man_2025'

@dataclass  
class PersistentPatternKnowledge:
    """Knowledge accumulated from persistent pattern detection"""
    pattern_signature: str  # Hash of pattern characteristics
    first_detection_timestamp: datetime
    last_detection_timestamp: datetime
    total_detections: int
    average_ingression_strength: float
    associated_thermal_signatures: List[Dict[str, Any]]
    associated_gpio_patterns: List[Dict[str, Any]]
    platonic_coordinate_clusters: List[Tuple[float, float, float, float]]
    morphogenetic_symmetry_types: Set[str]
    network_amplification_history: List[float]
    persistence_confidence: float  # How reliable this pattern knowledge is

@dataclass
class CollectiveIntelligencePersistence:
    """Persistent collective intelligence state across sessions"""
    cumulative_patterns_ingressed: int
    highest_collective_level_achieved: int
    mathematical_affordances_mastered: Dict[str, float]
    platonic_space_exploration_progress: Dict[str, float]
    autopoietic_processes_learned: List[str]
    emergent_properties_discovered: List[str]
    pattern_ingression_thresholds_optimized: Dict[str, float]
    network_topology_memory: Dict[str, Any]
    long_term_coherence_trends: List[Tuple[datetime, float]]

class IngressingMindsPersistenceEngine:
    """
    Manages persistence of ingressing minds patterns and collective intelligence
    across system reboots, power cycles, and long-term deployment
    """
    
    def __init__(self, 
                 data_directory: str = "/Users/barton/infinity-topos/zeldar-fortune/persistence_data",
                 node_id: str = None):
        self.data_directory = Path(data_directory)
        self.data_directory.mkdir(parents=True, exist_ok=True)
        self.node_id = node_id or f"persistent_node_{int(time.time())}"
        
        # Database connections
        self.patterns_db_path = self.data_directory / "ingressed_patterns.db"
        self.sessions_db_path = self.data_directory / "ingression_sessions.db"
        self.knowledge_db_path = self.data_directory / "pattern_knowledge.db"
        self.collective_db_path = self.data_directory / "collective_intelligence.db"
        
        # In-memory caches for performance
        self.pattern_cache: Dict[str, PersistentPatternKnowledge] = {}
        self.session_cache: Optional[PersistentIngressionSession] = None
        self.collective_cache: Optional[CollectiveIntelligencePersistence] = None
        
        # Persistence configuration
        self.auto_save_interval = 30.0  # Save every 30 seconds
        self.pattern_cleanup_days = 90   # Clean old patterns after 90 days
        self.session_history_limit = 1000  # Keep last 1000 sessions
        self.compression_enabled = True
        
        # Async persistence task
        self.persistence_task: Optional[asyncio.Task] = None
        self.persistence_active = False
        
        # Thread safety
        self.db_lock = threading.RLock()
        
        logger.info(f"🗄️ Ingressing Minds Persistence Engine Initialized")
        logger.info(f"📂 Data Directory: {self.data_directory}")
        logger.info(f"🔧 Node ID: {self.node_id}")
        
    async def initialize_persistence_system(self):
        """Initialize the persistence system and databases"""
        
        logger.info("🚀 Initializing persistence system...")
        
        # Create database schemas
        await self.create_database_schemas()
        
        # Load existing collective intelligence state
        await self.load_collective_intelligence_state()
        
        # Start current session
        await self.start_new_session()
        
        # Start async persistence tasks
        await self.start_persistence_tasks()
        
        logger.info("✅ Persistence system initialized successfully")
    
    async def create_database_schemas(self):
        """Create database schemas for persistence"""
        
        with self.db_lock:
            # Ingressed patterns database
            conn = sqlite3.connect(self.patterns_db_path)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ingressed_patterns (
                    pattern_id TEXT PRIMARY KEY,
                    session_id TEXT,
                    node_id TEXT,
                    ingression_timestamp TEXT,
                    pattern_type TEXT,
                    ingression_strength REAL,
                    platonic_coordinates_json TEXT,
                    collective_intelligence_level INTEGER,
                    autopoietic_coherence REAL,
                    morphogenetic_symmetry TEXT,
                    evolutionary_affordance REAL,
                    thermal_signature_json TEXT,
                    gpio_signature_json TEXT,
                    network_amplification_factor REAL,
                    persistence_hash TEXT,
                    compressed_data BLOB
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_patterns_timestamp ON ingressed_patterns(ingression_timestamp)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_patterns_type ON ingressed_patterns(pattern_type)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_patterns_session ON ingressed_patterns(session_id)")
            conn.close()
            
            # Sessions database
            conn = sqlite3.connect(self.sessions_db_path)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ingression_sessions (
                    session_id TEXT PRIMARY KEY,
                    node_id TEXT,
                    start_timestamp TEXT,
                    end_timestamp TEXT,
                    total_patterns_detected INTEGER,
                    collective_intelligence_level_achieved INTEGER,
                    mathematical_affordances_learned_json TEXT,
                    autopoietic_coherence_average REAL,
                    pattern_types_distribution_json TEXT,
                    hardware_configuration_json TEXT,
                    deployment_context TEXT,
                    session_hash TEXT
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_sessions_start ON ingression_sessions(start_timestamp)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_sessions_node ON ingression_sessions(node_id)")
            conn.close()
            
            # Pattern knowledge database
            conn = sqlite3.connect(self.knowledge_db_path)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS pattern_knowledge (
                    pattern_signature TEXT PRIMARY KEY,
                    first_detection_timestamp TEXT,
                    last_detection_timestamp TEXT,
                    total_detections INTEGER,
                    average_ingression_strength REAL,
                    thermal_signatures_json TEXT,
                    gpio_patterns_json TEXT,
                    platonic_coordinate_clusters_json TEXT,
                    morphogenetic_symmetry_types_json TEXT,
                    network_amplification_history_json TEXT,
                    persistence_confidence REAL,
                    knowledge_hash TEXT
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_knowledge_first_detection ON pattern_knowledge(first_detection_timestamp)")
            conn.close()
            
            # Collective intelligence database
            conn = sqlite3.connect(self.collective_db_path)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS collective_intelligence (
                    id INTEGER PRIMARY KEY,
                    cumulative_patterns_ingressed INTEGER,
                    highest_collective_level_achieved INTEGER,
                    mathematical_affordances_mastered_json TEXT,
                    platonic_space_exploration_progress_json TEXT,
                    autopoietic_processes_learned_json TEXT,
                    emergent_properties_discovered_json TEXT,
                    pattern_ingression_thresholds_optimized_json TEXT,
                    network_topology_memory_json TEXT,
                    long_term_coherence_trends_json TEXT,
                    last_updated_timestamp TEXT,
                    collective_hash TEXT
                )
            """)
            conn.close()
            
        logger.info("📋 Database schemas created successfully")
    
    async def start_new_session(self):
        """Start a new ingression session"""
        
        session_id = f"session_{self.node_id}_{int(time.time() * 1000)}"
        
        self.session_cache = PersistentIngressionSession(
            session_id=session_id,
            start_timestamp=datetime.now(),
            end_timestamp=None,
            node_id=self.node_id,
            total_patterns_detected=0,
            collective_intelligence_level_achieved=1,
            mathematical_affordances_learned={
                'fibonacci_spiral': 0.0,
                'golden_ratio_scaling': 0.0,
                'fractal_branching': 0.0,
                'symmetry_breaking': 0.0,
                'phase_transitions': 0.0
            },
            autopoietic_coherence_average=0.0,
            pattern_types_distribution={'mathematical': 0, 'morphogenetic': 0, 'cognitive': 0, 'computational': 0},
            hardware_configuration={
                'thermal_printer': True,
                'gpio_button': True,
                'network_capable': True,
                'persistence_enabled': True
            },
            deployment_context='development'  # Will be updated based on actual deployment
        )
        
        logger.info(f"🆕 New ingression session started: {session_id}")
    
    async def load_collective_intelligence_state(self):
        """Load existing collective intelligence state from persistence"""
        
        with self.db_lock:
            conn = sqlite3.connect(self.collective_db_path)
            cursor = conn.execute("SELECT * FROM collective_intelligence ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            conn.close()
            
            if row:
                # Restore collective intelligence state
                self.collective_cache = CollectiveIntelligencePersistence(
                    cumulative_patterns_ingressed=row[1],
                    highest_collective_level_achieved=row[2],
                    mathematical_affordances_mastered=json.loads(row[3]),
                    platonic_space_exploration_progress=json.loads(row[4]),
                    autopoietic_processes_learned=json.loads(row[5]),
                    emergent_properties_discovered=json.loads(row[6]),
                    pattern_ingression_thresholds_optimized=json.loads(row[7]),
                    network_topology_memory=json.loads(row[8]),
                    long_term_coherence_trends=[
                        (datetime.fromisoformat(t), c) for t, c in json.loads(row[9])
                    ]
                )
                
                logger.info(f"🧠 Collective intelligence state restored")
                logger.info(f"   Cumulative patterns: {self.collective_cache.cumulative_patterns_ingressed}")
                logger.info(f"   Highest collective level: {self.collective_cache.highest_collective_level_achieved}")
                
            else:
                # Initialize new collective intelligence state
                self.collective_cache = CollectiveIntelligencePersistence(
                    cumulative_patterns_ingressed=0,
                    highest_collective_level_achieved=1,
                    mathematical_affordances_mastered={
                        'fibonacci_spiral': 0.0,
                        'golden_ratio_scaling': 0.0,
                        'fractal_branching': 0.0,
                        'symmetry_breaking': 0.0,
                        'phase_transitions': 0.0,
                        'network_synchronization': 0.0
                    },
                    platonic_space_exploration_progress={
                        'mathematical_truths': 0.0,
                        'cognitive_forms': 0.0,
                        'morphogenetic_patterns': 0.0
                    },
                    autopoietic_processes_learned=[],
                    emergent_properties_discovered=[],
                    pattern_ingression_thresholds_optimized={'default': 0.55},
                    network_topology_memory={},
                    long_term_coherence_trends=[]
                )
                
                logger.info("🌟 New collective intelligence state initialized")
    
    async def start_persistence_tasks(self):
        """Start background persistence tasks"""
        
        self.persistence_active = True
        
        # Start auto-save task
        self.persistence_task = asyncio.create_task(self.auto_save_loop())
        
        logger.info("🔄 Persistence tasks started")
    
    async def auto_save_loop(self):
        """Background task for automatic saving"""
        
        while self.persistence_active:
            try:
                await self.save_current_session()
                await self.save_collective_intelligence_state()
                await self.cleanup_old_data()
                
                await asyncio.sleep(self.auto_save_interval)
                
            except Exception as e:
                logger.error(f"❌ Error in auto-save loop: {e}")
                await asyncio.sleep(self.auto_save_interval * 2)  # Back off on error
    
    async def persist_ingressed_pattern(self, pattern: IngressingPattern, 
                                      thermal_signature: Dict[str, Any],
                                      gpio_signature: Dict[str, Any],
                                      network_amplification: float = 1.0):
        """Persist an ingressed pattern to the database"""
        
        # Update session statistics
        if self.session_cache:
            self.session_cache.total_patterns_detected += 1
            self.session_cache.collective_intelligence_level_achieved = max(
                self.session_cache.collective_intelligence_level_achieved,
                pattern.collective_intelligence_level
            )
            
            # Update pattern type distribution
            pattern_type = pattern.pattern_type
            if pattern_type in self.session_cache.pattern_types_distribution:
                self.session_cache.pattern_types_distribution[pattern_type] += 1
            
            # Update mathematical affordances
            if pattern.evolutionary_affordance > 0.8:
                if thermal_signature.get('connection_interval') == 5.0:
                    self.session_cache.mathematical_affordances_learned['golden_ratio_scaling'] += 0.05
                if thermal_signature.get('text_wrapping') == 32:
                    self.session_cache.mathematical_affordances_learned['fibonacci_spiral'] += 0.03
                if pattern.morphogenetic_symmetry == 'fractal_recursive':
                    self.session_cache.mathematical_affordances_learned['fractal_branching'] += 0.04
        
        # Calculate pattern signature for knowledge accumulation
        pattern_signature = self.calculate_pattern_signature(pattern, thermal_signature, gpio_signature)
        
        # Update pattern knowledge
        await self.update_pattern_knowledge(
            pattern_signature, pattern, thermal_signature, gpio_signature, network_amplification
        )
        
        # Update collective intelligence
        if self.collective_cache:
            self.collective_cache.cumulative_patterns_ingressed += 1
            self.collective_cache.highest_collective_level_achieved = max(
                self.collective_cache.highest_collective_level_achieved,
                pattern.collective_intelligence_level
            )
            
            # Update long-term coherence trends
            self.collective_cache.long_term_coherence_trends.append(
                (datetime.now(), pattern.autopoietic_coherence)
            )
            
            # Keep only recent trends (last 1000)
            if len(self.collective_cache.long_term_coherence_trends) > 1000:
                self.collective_cache.long_term_coherence_trends = \
                    self.collective_cache.long_term_coherence_trends[-1000:]
        
        # Persist to database
        pattern_data = {
            'pattern_id': pattern.pattern_id,
            'session_id': self.session_cache.session_id if self.session_cache else 'unknown',
            'node_id': self.node_id,
            'ingression_timestamp': pattern.ingression_timestamp.isoformat(),
            'pattern_type': pattern.pattern_type,
            'ingression_strength': pattern.ingression_strength,
            'platonic_coordinates_json': json.dumps(pattern.platonic_coordinates),
            'collective_intelligence_level': pattern.collective_intelligence_level,
            'autopoietic_coherence': pattern.autopoietic_coherence,
            'morphogenetic_symmetry': pattern.morphogenetic_symmetry,
            'evolutionary_affordance': pattern.evolutionary_affordance,
            'thermal_signature_json': json.dumps(thermal_signature),
            'gpio_signature_json': json.dumps(gpio_signature),
            'network_amplification_factor': network_amplification,
            'persistence_hash': pattern_signature
        }
        
        # Compress data if enabled
        if self.compression_enabled:
            compressed_data = gzip.compress(json.dumps(pattern_data).encode('utf-8'))
            pattern_data['compressed_data'] = compressed_data
        
        with self.db_lock:
            conn = sqlite3.connect(self.patterns_db_path)
            conn.execute("""
                INSERT OR REPLACE INTO ingressed_patterns 
                (pattern_id, session_id, node_id, ingression_timestamp, pattern_type, 
                 ingression_strength, platonic_coordinates_json, collective_intelligence_level,
                 autopoietic_coherence, morphogenetic_symmetry, evolutionary_affordance,
                 thermal_signature_json, gpio_signature_json, network_amplification_factor,
                 persistence_hash, compressed_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                pattern_data['pattern_id'], pattern_data['session_id'], pattern_data['node_id'],
                pattern_data['ingression_timestamp'], pattern_data['pattern_type'],
                pattern_data['ingression_strength'], pattern_data['platonic_coordinates_json'],
                pattern_data['collective_intelligence_level'], pattern_data['autopoietic_coherence'],
                pattern_data['morphogenetic_symmetry'], pattern_data['evolutionary_affordance'],
                pattern_data['thermal_signature_json'], pattern_data['gpio_signature_json'],
                pattern_data['network_amplification_factor'], pattern_data['persistence_hash'],
                pattern_data.get('compressed_data')
            ))
            conn.commit()
            conn.close()
        
        logger.info(f"💾 Pattern persisted: {pattern.pattern_id} (signature: {pattern_signature[:8]}...)")
    
    def calculate_pattern_signature(self, pattern: IngressingPattern, 
                                  thermal_signature: Dict[str, Any], 
                                  gpio_signature: Dict[str, Any]) -> str:
        """Calculate a unique signature for pattern knowledge accumulation"""
        
        signature_data = {
            'pattern_type': pattern.pattern_type,
            'connection_interval': thermal_signature.get('connection_interval', 0.0),
            'text_wrapping': thermal_signature.get('text_wrapping', 0),
            'morphogenetic_symmetry': pattern.morphogenetic_symmetry,
            'platonic_coords_rounded': tuple(round(c, 2) for c in pattern.platonic_coordinates),
            'thermal_event_type': thermal_signature.get('event_type', 'unknown'),
            'gpio_pressed': gpio_signature.get('button_pressed', False)
        }
        
        signature_str = json.dumps(signature_data, sort_keys=True)
        return hashlib.sha256(signature_str.encode('utf-8')).hexdigest()
    
    async def update_pattern_knowledge(self, pattern_signature: str, pattern: IngressingPattern,
                                     thermal_signature: Dict[str, Any], gpio_signature: Dict[str, Any],
                                     network_amplification: float):
        """Update accumulated knowledge about this pattern type"""
        
        current_time = datetime.now()
        
        if pattern_signature in self.pattern_cache:
            # Update existing knowledge
            knowledge = self.pattern_cache[pattern_signature]
            knowledge.last_detection_timestamp = current_time
            knowledge.total_detections += 1
            
            # Update running averages
            knowledge.average_ingression_strength = (
                (knowledge.average_ingression_strength * (knowledge.total_detections - 1) + 
                 pattern.ingression_strength) / knowledge.total_detections
            )
            
            # Add new signatures and patterns
            knowledge.associated_thermal_signatures.append(thermal_signature)
            knowledge.associated_gpio_patterns.append(gpio_signature)
            knowledge.platonic_coordinate_clusters.append(pattern.platonic_coordinates)
            knowledge.morphogenetic_symmetry_types.add(pattern.morphogenetic_symmetry)
            knowledge.network_amplification_history.append(network_amplification)
            
            # Update persistence confidence based on detection frequency
            knowledge.persistence_confidence = min(1.0, knowledge.total_detections / 10.0)
            
        else:
            # Create new knowledge entry
            knowledge = PersistentPatternKnowledge(
                pattern_signature=pattern_signature,
                first_detection_timestamp=current_time,
                last_detection_timestamp=current_time,
                total_detections=1,
                average_ingression_strength=pattern.ingression_strength,
                associated_thermal_signatures=[thermal_signature],
                associated_gpio_patterns=[gpio_signature],
                platonic_coordinate_clusters=[pattern.platonic_coordinates],
                morphogenetic_symmetry_types={pattern.morphogenetic_symmetry},
                network_amplification_history=[network_amplification],
                persistence_confidence=0.1  # Low confidence for new patterns
            )
            
            self.pattern_cache[pattern_signature] = knowledge
        
        # Limit cache size (keep most recent 1000 patterns)
        if len(self.pattern_cache) > 1000:
            # Remove oldest patterns
            sorted_patterns = sorted(
                self.pattern_cache.items(),
                key=lambda x: x[1].last_detection_timestamp
            )
            
            for pattern_sig, _ in sorted_patterns[:-900]:  # Keep 900 most recent
                del self.pattern_cache[pattern_sig]
    
    async def save_current_session(self):
        """Save current session to database"""
        
        if not self.session_cache:
            return
        
        # Calculate autopoietic coherence average
        if self.session_cache.total_patterns_detected > 0:
            # This would ideally be calculated from actual patterns
            # For now, use a placeholder calculation
            self.session_cache.autopoietic_coherence_average = 0.7  # Placeholder
        
        session_data = asdict(self.session_cache)
        session_data['start_timestamp'] = session_data['start_timestamp'].isoformat()
        if session_data['end_timestamp']:
            session_data['end_timestamp'] = session_data['end_timestamp'].isoformat()
        
        session_hash = hashlib.sha256(
            json.dumps(session_data, sort_keys=True).encode('utf-8')
        ).hexdigest()
        
        with self.db_lock:
            conn = sqlite3.connect(self.sessions_db_path)
            conn.execute("""
                INSERT OR REPLACE INTO ingression_sessions
                (session_id, node_id, start_timestamp, end_timestamp,
                 total_patterns_detected, collective_intelligence_level_achieved,
                 mathematical_affordances_learned_json, autopoietic_coherence_average,
                 pattern_types_distribution_json, hardware_configuration_json,
                 deployment_context, session_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.session_cache.session_id, self.session_cache.node_id,
                session_data['start_timestamp'], session_data['end_timestamp'],
                self.session_cache.total_patterns_detected,
                self.session_cache.collective_intelligence_level_achieved,
                json.dumps(self.session_cache.mathematical_affordances_learned),
                self.session_cache.autopoietic_coherence_average,
                json.dumps(self.session_cache.pattern_types_distribution),
                json.dumps(self.session_cache.hardware_configuration),
                self.session_cache.deployment_context, session_hash
            ))
            conn.commit()
            conn.close()
    
    async def save_collective_intelligence_state(self):
        """Save collective intelligence state to database"""
        
        if not self.collective_cache:
            return
        
        # Convert coherence trends to serializable format
        coherence_trends_serializable = [
            (trend[0].isoformat(), trend[1]) for trend in self.collective_cache.long_term_coherence_trends
        ]
        
        collective_hash = hashlib.sha256(
            json.dumps({
                'patterns': self.collective_cache.cumulative_patterns_ingressed,
                'level': self.collective_cache.highest_collective_level_achieved,
                'affordances': self.collective_cache.mathematical_affordances_mastered
            }, sort_keys=True).encode('utf-8')
        ).hexdigest()
        
        with self.db_lock:
            conn = sqlite3.connect(self.collective_db_path)
            conn.execute("""
                INSERT OR REPLACE INTO collective_intelligence
                (id, cumulative_patterns_ingressed, highest_collective_level_achieved,
                 mathematical_affordances_mastered_json, platonic_space_exploration_progress_json,
                 autopoietic_processes_learned_json, emergent_properties_discovered_json,
                 pattern_ingression_thresholds_optimized_json, network_topology_memory_json,
                 long_term_coherence_trends_json, last_updated_timestamp, collective_hash)
                VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.collective_cache.cumulative_patterns_ingressed,
                self.collective_cache.highest_collective_level_achieved,
                json.dumps(self.collective_cache.mathematical_affordances_mastered),
                json.dumps(self.collective_cache.platonic_space_exploration_progress),
                json.dumps(self.collective_cache.autopoietic_processes_learned),
                json.dumps(self.collective_cache.emergent_properties_discovered),
                json.dumps(self.collective_cache.pattern_ingression_thresholds_optimized),
                json.dumps(self.collective_cache.network_topology_memory),
                json.dumps(coherence_trends_serializable),
                datetime.now().isoformat(),
                collective_hash
            ))
            conn.commit()
            conn.close()
    
    async def cleanup_old_data(self):
        """Clean up old data to manage storage"""
        
        cutoff_date = (datetime.now() - timedelta(days=self.pattern_cleanup_days)).isoformat()
        
        with self.db_lock:
            # Clean old patterns
            conn = sqlite3.connect(self.patterns_db_path)
            cursor = conn.execute("DELETE FROM ingressed_patterns WHERE ingression_timestamp < ?", (cutoff_date,))
            patterns_deleted = cursor.rowcount
            conn.commit()
            conn.close()
            
            # Clean old sessions (keep only last 1000)
            conn = sqlite3.connect(self.sessions_db_path)
            cursor = conn.execute("""
                DELETE FROM ingression_sessions 
                WHERE session_id NOT IN (
                    SELECT session_id FROM ingression_sessions 
                    ORDER BY start_timestamp DESC LIMIT ?
                )
            """, (self.session_history_limit,))
            sessions_deleted = cursor.rowcount
            conn.commit()
            conn.close()
            
            if patterns_deleted > 0 or sessions_deleted > 0:
                logger.info(f"🧹 Cleanup complete: {patterns_deleted} patterns, {sessions_deleted} sessions removed")
    
    async def get_pattern_ingression_enhancement(self, thermal_signature: Dict[str, Any], 
                                               gpio_signature: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """Get ingression threshold enhancement based on persistent knowledge"""
        
        # Calculate signature for this potential pattern
        temp_pattern = type('TempPattern', (), {
            'pattern_type': 'unknown',
            'morphogenetic_symmetry': 'unknown',
            'platonic_coordinates': (0.5, 0.5, 0.5, 0.5)
        })()
        
        signature = self.calculate_pattern_signature(temp_pattern, thermal_signature, gpio_signature)
        
        enhancement_factor = 1.0
        enhancement_details = {}
        
        # Check if we have knowledge about similar patterns
        if signature in self.pattern_cache:
            knowledge = self.pattern_cache[signature]
            
            # Apply enhancement based on historical success
            if knowledge.persistence_confidence > 0.8:
                enhancement_factor = 1.0 - (knowledge.average_ingression_strength * 0.1)
                enhancement_details['historical_success'] = knowledge.total_detections
                enhancement_details['confidence'] = knowledge.persistence_confidence
                
            # Apply collective intelligence enhancement
            if self.collective_cache:
                collective_enhancement = min(0.3, 
                    self.collective_cache.highest_collective_level_achieved * 0.03
                )
                enhancement_factor -= collective_enhancement
                enhancement_details['collective_enhancement'] = collective_enhancement
        
        # Apply mathematical affordance enhancements
        if self.collective_cache:
            affordances = self.collective_cache.mathematical_affordances_mastered
            
            # Golden ratio enhancement
            if thermal_signature.get('connection_interval') == 5.0 and affordances.get('golden_ratio_scaling', 0) > 0.5:
                enhancement_factor -= 0.1
                enhancement_details['golden_ratio_mastery'] = True
            
            # Fibonacci enhancement
            if thermal_signature.get('text_wrapping') == 32 and affordances.get('fibonacci_spiral', 0) > 0.5:
                enhancement_factor -= 0.05
                enhancement_details['fibonacci_mastery'] = True
        
        # Ensure we don't make threshold too low
        enhancement_factor = max(0.3, min(1.0, enhancement_factor))
        
        return enhancement_factor, enhancement_details
    
    async def get_persistence_statistics(self) -> Dict[str, Any]:
        """Get comprehensive persistence statistics"""
        
        stats = {
            'current_session': asdict(self.session_cache) if self.session_cache else None,
            'collective_intelligence': asdict(self.collective_cache) if self.collective_cache else None,
            'pattern_cache_size': len(self.pattern_cache),
            'database_statistics': {}
        }
        
        # Get database statistics
        with self.db_lock:
            # Patterns database stats
            conn = sqlite3.connect(self.patterns_db_path)
            cursor = conn.execute("SELECT COUNT(*) FROM ingressed_patterns")
            stats['database_statistics']['total_patterns'] = cursor.fetchone()[0]
            
            cursor = conn.execute("""
                SELECT pattern_type, COUNT(*) 
                FROM ingressed_patterns 
                GROUP BY pattern_type
            """)
            stats['database_statistics']['patterns_by_type'] = dict(cursor.fetchall())
            conn.close()
            
            # Sessions database stats
            conn = sqlite3.connect(self.sessions_db_path)
            cursor = conn.execute("SELECT COUNT(*) FROM ingression_sessions")
            stats['database_statistics']['total_sessions'] = cursor.fetchone()[0]
            
            cursor = conn.execute("""
                SELECT deployment_context, COUNT(*) 
                FROM ingression_sessions 
                GROUP BY deployment_context
            """)
            stats['database_statistics']['sessions_by_context'] = dict(cursor.fetchall())
            conn.close()
        
        return stats
    
    async def generate_persistence_report(self) -> str:
        """Generate comprehensive persistence report"""
        
        stats = await self.get_persistence_statistics()
        
        report = [
            "💾 INGRESSING MINDS PERSISTENCE SYSTEM REPORT",
            "=" * 60,
            f"📜 Framework: Michael Levin's Pattern Persistence Theory",
            f"⏰ Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"🔧 Node ID: {self.node_id}",
            f"📂 Data Directory: {self.data_directory}",
            "",
            "📊 CURRENT SESSION:",
        ]
        
        if stats['current_session']:
            session = stats['current_session']
            report.extend([
                f"   Session ID: {session['session_id']}",
                f"   Patterns Detected: {session['total_patterns_detected']}",
                f"   Collective Level Achieved: {session['collective_intelligence_level_achieved']}",
                f"   Deployment Context: {session['deployment_context']}",
            ])
            
            if session['pattern_types_distribution']:
                report.append("   Pattern Types Distribution:")
                for pattern_type, count in session['pattern_types_distribution'].items():
                    if count > 0:
                        report.append(f"     • {pattern_type}: {count}")
        else:
            report.append("   No active session")
        
        report.extend([
            "",
            "🧠 COLLECTIVE INTELLIGENCE PERSISTENCE:",
        ])
        
        if stats['collective_intelligence']:
            collective = stats['collective_intelligence']
            report.extend([
                f"   Cumulative Patterns Ingressed: {collective['cumulative_patterns_ingressed']}",
                f"   Highest Collective Level: {collective['highest_collective_level_achieved']}",
                f"   Coherence Trend Data Points: {len(collective['long_term_coherence_trends'])}",
                "",
                "   Mathematical Affordances Mastered:",
            ])
            
            for affordance, level in collective['mathematical_affordances_mastered'].items():
                if level > 0:
                    report.append(f"     • {affordance.title().replace('_', ' ')}: {level:.3f}")
            
            if collective['autopoietic_processes_learned']:
                report.extend([
                    "",
                    "   Autopoietic Processes Learned:",
                ])
                for process in collective['autopoietic_processes_learned']:
                    report.append(f"     • {process.title().replace('_', ' ')}")
            
            if collective['emergent_properties_discovered']:
                report.extend([
                    "",
                    "   Emergent Properties Discovered:",
                ])
                for prop in collective['emergent_properties_discovered']:
                    report.append(f"     • {prop.title().replace('_', ' ')}")
        
        report.extend([
            "",
            "💾 DATABASE STATISTICS:",
            f"   Total Patterns Persisted: {stats['database_statistics'].get('total_patterns', 0)}",
            f"   Total Sessions Recorded: {stats['database_statistics'].get('total_sessions', 0)}",
            f"   Pattern Knowledge Cache Size: {stats['pattern_cache_size']}",
        ])
        
        if stats['database_statistics'].get('patterns_by_type'):
            report.append("   Patterns by Type:")
            for pattern_type, count in stats['database_statistics']['patterns_by_type'].items():
                report.append(f"     • {pattern_type}: {count}")
        
        if stats['database_statistics'].get('sessions_by_context'):
            report.append("   Sessions by Deployment Context:")
            for context, count in stats['database_statistics']['sessions_by_context'].items():
                report.append(f"     • {context}: {count}")
        
        report.extend([
            "",
            "🔧 SYSTEM HEALTH:",
            f"   Persistence Tasks Active: {'✅' if self.persistence_active else '❌'}",
            f"   Auto-save Interval: {self.auto_save_interval}s",
            f"   Data Compression: {'✅' if self.compression_enabled else '❌'}",
            f"   Pattern Cleanup Days: {self.pattern_cleanup_days}",
            "",
            "🌟 PERSISTENCE BENEFITS:",
            "   • Patterns survive system reboots and power cycles",
            "   • Collective intelligence accumulates across deployments",
            "   • Mathematical affordances learned over time",
            "   • Enhanced pattern detection through historical knowledge",
            "   • Long-term morphogenetic field continuity",
            "",
            "🏜️🔥 Persistent Ingressing Minds • Black Rock City 2025 🔥🏜️"
        ])
        
        return "\n".join(report)
    
    async def end_current_session(self):
        """End the current ingression session"""
        
        if self.session_cache:
            self.session_cache.end_timestamp = datetime.now()
            await self.save_current_session()
            
            logger.info(f"🏁 Session ended: {self.session_cache.session_id}")
            logger.info(f"   Patterns detected: {self.session_cache.total_patterns_detected}")
            logger.info(f"   Collective level achieved: {self.session_cache.collective_intelligence_level_achieved}")
        
        # Stop persistence tasks
        self.persistence_active = False
        if self.persistence_task:
            self.persistence_task.cancel()
            
        # Final save
        await self.save_collective_intelligence_state()
        
        logger.info("💾 Persistence system shutdown complete")

# Integration with existing ingressing minds system
class PersistenceAwareIngressingMindsDetector(IngressingMindsDetector):
    """
    Enhanced ingressing minds detector with persistence capabilities
    """
    
    def __init__(self, persistence_engine: IngressingMindsPersistenceEngine):
        super().__init__()
        self.persistence_engine = persistence_engine
        
        # Apply persistent enhancements to detection
        self.apply_persistent_enhancements()
        
    async def apply_persistent_enhancements(self):
        """Apply enhancements based on persistent knowledge"""
        
        if not self.persistence_engine.collective_cache:
            return
        
        collective = self.persistence_engine.collective_cache
        
        # Adjust ingression threshold based on collective intelligence
        if collective.highest_collective_level_achieved > 5:
            self.ingression_threshold = max(0.3, self.ingression_threshold - 0.1)
            
        # Update mathematical affordances based on learned knowledge
        for affordance, level in collective.mathematical_affordances_mastered.items():
            if affordance in self.mathematical_affordances:
                self.mathematical_affordances[affordance] = max(
                    self.mathematical_affordances[affordance], level
                )
        
        logger.info("🎯 Persistent enhancements applied to pattern detection")
    
    async def detect_pattern_ingression_with_persistence(self, thermal_event: Dict, gpio_response: Dict) -> Optional[IngressingPattern]:
        """Enhanced pattern detection with persistence information-attention"""
        
        # Get persistence-based threshold enhancement
        threshold_factor, enhancement_details = await self.persistence_engine.get_pattern_ingression_enhancement(
            thermal_event, gpio_response
        )
        
        # Temporarily adjust threshold
        original_threshold = self.ingression_threshold
        enhanced_threshold = original_threshold * threshold_factor
        self.ingression_threshold = enhanced_threshold
        
        # Perform standard detection
        pattern = self.detect_pattern_ingression(thermal_event, gpio_response)
        
        # Restore original threshold
        self.ingression_threshold = original_threshold
        
        # If pattern detected, persist it
        if pattern:
            await self.persistence_engine.persist_ingressed_pattern(
                pattern, thermal_event, gpio_response
            )
            
            logger.info(f"✨ PERSISTENT PATTERN INGRESSION: {pattern.pattern_type}")
            logger.info(f"   Enhanced threshold: {original_threshold:.3f} → {enhanced_threshold:.3f}")
            if enhancement_details:
                logger.info(f"   Enhancements: {enhancement_details}")
        
        return pattern

# Demonstration and testing
async def demonstrate_persistence_system():
    """Demonstrate persistence system capabilities"""
    
    logger.info("💾 DEMONSTRATING INGRESSING MINDS PERSISTENCE SYSTEM")
    logger.info("=" * 70)
    
    # Initialize persistence engine
    persistence_engine = IngressingMindsPersistenceEngine(
        node_id="demo_persistent_node"
    )
    
    await persistence_engine.initialize_persistence_system()
    
    # Create persistence-informationally-attending detector
    detector = PersistenceAwareIngressingMindsDetector(persistence_engine)
    await detector.apply_persistent_enhancements()
    
    # Simulate pattern detection over multiple "sessions"
    logger.info("🔄 Simulating pattern ingression across multiple sessions...")
    
    for session in range(3):
        logger.info(f"\n📅 Session {session + 1}/3")
        
        # Generate patterns for this session
        for cycle in range(5):
            thermal_event = {
                'event_type': 'persistence_test',
                'connection_interval': 5.0 if cycle % 2 == 0 else 1.618,
                'text_wrapping': 32,
                'printing_active': True,
                'qr_generation': cycle % 3 == 0,
                'information-dynamics_weight': 0.8 + cycle * 0.02
            }
            
            gpio_response = {
                'button_pressed': True,
                'press_duration': 150 + cycle * 10,
                'response_probability': 0.85 + cycle * 0.01
            }
            
            pattern = await detector.detect_pattern_ingression_with_persistence(
                thermal_event, gpio_response
            )
            
            if pattern:
                logger.info(f"   ✨ Pattern {cycle + 1}: {pattern.pattern_type}")
        
        # End session and start new one (simulating system restart)
        await persistence_engine.end_current_session()
        await persistence_engine.start_new_session()
        
        # Re-apply enhancements (simulating system restart)
        await detector.apply_persistent_enhancements()
        
        logger.info(f"   📊 Session complete - patterns persist across restart")
    
    # Generate final persistence report
    report = await persistence_engine.generate_persistence_report()
    logger.info(f"\n{report}")
    
    # Clean shutdown
    await persistence_engine.end_current_session()
    
    logger.info("\n💾 Persistence system demonstration complete!")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    asyncio.run(demonstrate_persistence_system())