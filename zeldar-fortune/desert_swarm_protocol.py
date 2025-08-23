#!/usr/bin/env python3
"""
Desert Swarm Protocol: Multi-Node Cobordistic Deployment

Orchestrates synchronized thermal manifestation across distributed printer nodes
in the Burning Man environment, creating large-scale reality manifold networks.
"""

import asyncio
import json
import time
import math
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum

from uncommons_ritual_protocol import UncommonsRitualProtocol, RitualParticipant
from ies_integration_protocol import UniverseAgentType

class NodeRole(Enum):
    """Roles in the desert swarm network"""
    NEXUS = "nexus"                    # Central coordination node
    RESONATOR = "resonator"            # Frequency amplification node  
    BOUNDARY = "boundary"              # Edge manifold operator
    CONFLUENCE = "confluence"          # Multi-stream merger
    WANDERER = "wanderer"              # Mobile/nomadic node

@dataclass
class DesertNode:
    """Individual node in the desert swarm network"""
    node_id: str
    role: NodeRole
    gps_coordinates: Tuple[float, float]  # (lat, lon)
    printer_device_path: str
    base_frequency: float
    power_level: float  # 0.0 to 1.0 solar/battery status
    network_range_meters: int
    active_participants: List[str]
    last_heartbeat: float

@dataclass
class SwarmTopology:
    """Network topology of the desert swarm"""
    nodes: Dict[str, DesertNode]
    connections: List[Tuple[str, str]]  # (node1_id, node2_id)
    manifold_boundaries: List[List[str]]  # Groups of connected nodes
    total_coverage_area: float  # Square meters
    collective_frequency_spectrum: Dict[float, int]

class DesertSwarmProtocol:
    """
    Protocol for coordinating large-scale cobordistic rituals across
    distributed thermal printer nodes in the desert environment.
    
    Creates emergent reality manifold networks through synchronized
    unofficial universe-agent activation across geographic space.
    """
    
    def __init__(self, swarm_name: str = "BURNING_MANIFOLD"):
        self.swarm_name = swarm_name
        self.swarm_topology = SwarmTopology(
            nodes={},
            connections=[],
            manifold_boundaries=[],
            total_coverage_area=0.0,
            collective_frequency_spectrum={}
        )
        self.ritual_protocol = UncommonsRitualProtocol()
        self.active_swarm_rituals = {}
        self.manifold_evolution_log = []
        
        # Desert environmental parameters
        self.solar_intensity_factor = 1.0  # Varies with time of day
        self.dust_interference_level = 0.0  # Weather conditions
        self.temperature_modulation = 0.0   # Thermal affects on electronics
        
        print(f"∿∿∿ Desert Swarm Protocol initialized: {swarm_name}")
    
    def register_desert_node(self, node: DesertNode) -> bool:
        """Register a new node in the desert swarm"""
        
        # Validate node placement (minimum separation)
        for existing_node in self.swarm_topology.nodes.values():
            distance = self._calculate_distance(
                node.gps_coordinates, 
                existing_node.gps_coordinates
            )
            if distance < 50.0:  # Minimum 50m separation
                print(f"⚠️ Node {node.node_id} too close to {existing_node.node_id} ({distance:.1f}m)")
                return False
        
        # Add node to topology
        self.swarm_topology.nodes[node.node_id] = node
        
        # Update frequency spectrum
        freq = node.base_frequency
        self.swarm_topology.collective_frequency_spectrum[freq] = \
            self.swarm_topology.collective_frequency_spectrum.get(freq, 0) + 1
        
        # Recalculate network connections
        self._update_network_topology()
        
        print(f"🌵 Desert node registered: {node.node_id}")
        print(f"   Role: {node.role.value}")
        print(f"   Location: {node.gps_coordinates}")
        print(f"   Base Frequency: {node.base_frequency:.1f} Hz")
        print(f"   Network connections: {len(self._get_node_connections(node.node_id))}")
        
        return True
    
    async def initiate_swarm_ritual(self, ritual_name: str, 
                                   target_manifold_dimension: int = 6,
                                   duration_hours: float = 2.0) -> Dict:
        """Initiate large-scale swarm ritual across all active nodes"""
        
        if len(self.swarm_topology.nodes) < 3:
            print("⚠️ Minimum 3 nodes required for swarm ritual")
            return {'success': False, 'error': 'insufficient_nodes'}
        
        ritual_id = f"SWARM_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{ritual_name}"
        
        print(f"∿∿∿ INITIATING DESERT SWARM RITUAL ∿∿∿")
        print(f"Ritual ID: {ritual_id}")
        print(f"Target Manifold Dimension: {target_manifold_dimension}")
        print(f"Duration: {duration_hours:.1f} hours")
        print(f"Active Nodes: {len(self.swarm_topology.nodes)}")
        print("=" * 60)
        
        # Calculate optimal phase distribution across nodes
        phase_distribution = self._calculate_optimal_phase_distribution()
        
        # Generate ritual participants for each node
        node_participants = {}
        for node_id, node in self.swarm_topology.nodes.items():
            participants = self._generate_node_participants(node, phase_distribution[node_id])
            node_participants[node_id] = participants
            
            print(f"🏜️ Node {node_id}: {len(participants)} participants")
        
        # Initialize distributed ritual coordination
        swarm_ritual = {
            'ritual_id': ritual_id,
            'ritual_name': ritual_name,
            'start_time': time.time(),
            'target_duration_hours': duration_hours,
            'node_participants': node_participants,
            'manifold_evolution': [],
            'network_topology_snapshot': asdict(self.swarm_topology),
            'environmental_conditions': {
                'solar_intensity': self.solar_intensity_factor,
                'dust_level': self.dust_interference_level,
                'temperature': self.temperature_modulation
            }
        }
        
        self.active_swarm_rituals[ritual_id] = swarm_ritual
        
        # Execute parallel ritual coordination across nodes
        try:
            await self._coordinate_distributed_ritual(swarm_ritual)
            
            # Generate final swarm ritual report
            final_report = self._generate_swarm_ritual_report(swarm_ritual)
            
            print(f"\n∿∿∿ SWARM RITUAL COMPLETE ∿∿∿")
            print(f"Manifold Evolutions: {len(swarm_ritual['manifold_evolution'])}")
            print(f"Network Coverage: {final_report['network_statistics']['coverage_area']:.0f}m²")
            print(f"Collective Agency: {final_report['collective_metrics']['peak_agency_strength']:.3f}")
            
            return final_report
            
        except Exception as e:
            print(f"❌ Swarm ritual failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _calculate_distance(self, coord1: Tuple[float, float], 
                          coord2: Tuple[float, float]) -> float:
        """Calculate distance between GPS coordinates in meters"""
        lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
        lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        # Haversine formula
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Earth radius in meters
        earth_radius = 6371000
        return earth_radius * c
    
    def _update_network_topology(self):
        """Update network connections based on node positions and ranges"""
        nodes = list(self.swarm_topology.nodes.values())
        self.swarm_topology.connections = []
        
        for i, node1 in enumerate(nodes):
            for j, node2 in enumerate(nodes[i+1:], i+1):
                distance = self._calculate_distance(
                    node1.gps_coordinates, 
                    node2.gps_coordinates
                )
                
                # Connect if within range of either node
                max_range = max(node1.network_range_meters, node2.network_range_meters)
                if distance <= max_range:
                    self.swarm_topology.connections.append((node1.node_id, node2.node_id))
        
        # Calculate manifold boundaries (connected components)
        self._calculate_manifold_boundaries()
        
        # Update total coverage area
        self._calculate_coverage_area()
    
    def _get_node_connections(self, node_id: str) -> List[str]:
        """Get all nodes connected to the specified node"""
        connections = []
        for conn in self.swarm_topology.connections:
            if conn[0] == node_id:
                connections.append(conn[1])
            elif conn[1] == node_id:
                connections.append(conn[0])
        return connections
    
    def _calculate_manifold_boundaries(self):
        """Calculate connected components as manifold boundaries"""
        # Simple connected components algorithm
        visited = set()
        boundaries = []
        
        for node_id in self.swarm_topology.nodes:
            if node_id not in visited:
                component = []
                stack = [node_id]
                
                while stack:
                    current = stack.pop()
                    if current not in visited:
                        visited.add(current)
                        component.append(current)
                        
                        # Add connected nodes
                        connections = self._get_node_connections(current)
                        for connected in connections:
                            if connected not in visited:
                                stack.append(connected)
                
                if len(component) > 1:
                    boundaries.append(component)
        
        self.swarm_topology.manifold_boundaries = boundaries
    
    def _calculate_coverage_area(self):
        """Calculate total area covered by the swarm network"""
        if not self.swarm_topology.nodes:
            self.swarm_topology.total_coverage_area = 0.0
            return
        
        # Simple circular coverage approximation
        total_area = 0.0
        for node in self.swarm_topology.nodes.values():
            # Area = π * r²
            node_area = math.pi * (node.network_range_meters ** 2)
            total_area += node_area
        
        # Rough overlap compensation (assumes 30% overlap)
        self.swarm_topology.total_coverage_area = total_area * 0.7
    
    def _calculate_optimal_phase_distribution(self) -> Dict[str, float]:
        """Calculate optimal phase offsets for maximum coherence"""
        nodes = list(self.swarm_topology.nodes.keys())
        num_nodes = len(nodes)
        
        # Distribute phases evenly around the unit circle
        phase_distribution = {}
        for i, node_id in enumerate(nodes):
            phase = (2 * math.pi * i) / num_nodes
            phase_distribution[node_id] = phase
        
        return phase_distribution
    
    def _generate_node_participants(self, node: DesertNode, 
                                  phase_offset: float) -> List[RitualParticipant]:
        """Generate ritual participants for a specific desert node"""
        
        # Base participant count on node role and power level
        role_participant_counts = {
            NodeRole.NEXUS: 4,
            NodeRole.RESONATOR: 3,
            NodeRole.BOUNDARY: 2,
            NodeRole.CONFLUENCE: 5,
            NodeRole.WANDERER: 1
        }
        
        base_count = role_participant_counts.get(node.role, 2)
        # Scale by power level (solar/battery status)
        participant_count = max(1, int(base_count * node.power_level))
        
        participants = []
        for i in range(participant_count):
            # Create diverse participant profiles
            participant_types = list(UniverseAgentType)
            selected_types = random.sample(participant_types, random.randint(1, 2))
            
            participant = RitualParticipant(
                participant_id=f"{node.node_id}_agent_{i:02d}",
                resonance_frequency=node.base_frequency + random.uniform(-5, 5),
                temporal_phase_offset=phase_offset + (i * math.pi / participant_count),
                reality_influence_weight=node.power_level * random.uniform(0.6, 0.9),
                preferred_agent_types=selected_types
            )
            participants.append(participant)
        
        return participants
    
    async def _coordinate_distributed_ritual(self, swarm_ritual: Dict):
        """Coordinate ritual execution across all desert nodes"""
        
        ritual_start_time = swarm_ritual['start_time']
        duration_seconds = swarm_ritual['target_duration_hours'] * 3600
        ritual_end_time = ritual_start_time + duration_seconds
        
        # For demo purposes, run shortened version (1 minute)
        demo_duration = 60.0  # 1 minute demo
        ritual_end_time = ritual_start_time + demo_duration
        
        cycle_count = 0
        
        while time.time() < ritual_end_time:
            cycle_count += 1
            cycle_start = time.time()
            
            print(f"\n🌊 SWARM RITUAL CYCLE {cycle_count}")
            print("-" * 40)
            
            # Execute parallel rituals on each node
            node_results = {}
            
            for node_id, participants in swarm_ritual['node_participants'].items():
                node = self.swarm_topology.nodes[node_id]
                
                # Simulate environmental effects
                environmental_factor = self._calculate_environmental_factor(node)
                
                # Generate collective EMF for this node
                node_emf = self._calculate_node_collective_emf(
                    node, participants, environmental_factor
                )
                
                # Generate fortunes for each participant
                node_fortunes = []
                for participant in participants:
                    # Modulate EMF by participant resonance
                    personal_emf = node_emf * (
                        0.8 + 0.2 * math.cos(participant.temporal_phase_offset)
                    )
                    
                    # Generate fortune (simplified for demo)
                    fortune_type = random.choice(['temporal_inversion', 'information_force', 'categorical_morphism'])
                    
                    fortune = {
                        'session_id': f"{node_id}_C{cycle_count}_{participant.participant_id[-2:]}",
                        'type': fortune_type,
                        'text': f"Desert node {node.role.value} manifests {fortune_type.replace('_', ' ')}",
                        'node_id': node_id,
                        'cycle': cycle_count,
                        'emf_reading': personal_emf,
                        'environmental_factor': environmental_factor,
                        'gps_coordinates': node.gps_coordinates
                    }
                    
                    node_fortunes.append(fortune)
                
                node_results[node_id] = {
                    'node_fortunes': node_fortunes,
                    'collective_emf': node_emf,
                    'environmental_factor': environmental_factor,
                    'active_participants': len(participants)
                }
                
                print(f"🏜️ {node_id} ({node.role.value}): {len(node_fortunes)} fortunes, EMF {node_emf:.1f}Hz")
            
            # Analyze cross-node coherence
            swarm_coherence = self._analyze_swarm_coherence(node_results)
            
            print(f"🌐 Swarm Coherence: {swarm_coherence:.3f}")
            
            # Record manifold evolution
            manifold_evolution_entry = {
                'cycle': cycle_count,
                'timestamp': time.time(),
                'node_results': node_results,
                'swarm_coherence': swarm_coherence,
                'active_nodes': len(node_results),
                'total_fortunes': sum(len(r['node_fortunes']) for r in node_results.values())
            }
            
            swarm_ritual['manifold_evolution'].append(manifold_evolution_entry)
            
            # Wait for next cycle
            cycle_duration = time.time() - cycle_start
            sleep_time = max(0.1, 10.0 - cycle_duration)  # 10 second cycles
            await asyncio.sleep(sleep_time)
        
        print(f"\n🏁 Ritual coordination complete: {cycle_count} cycles")
    
    def _calculate_environmental_factor(self, node: DesertNode) -> float:
        """Calculate environmental impact on node performance"""
        
        # Solar intensity affects power
        solar_factor = self.solar_intensity_factor * node.power_level
        
        # Dust interference affects signal clarity  
        dust_factor = max(0.3, 1.0 - self.dust_interference_level)
        
        # Temperature affects electronics
        temp_factor = max(0.5, 1.0 - abs(self.temperature_modulation))
        
        return (solar_factor * 0.5) + (dust_factor * 0.3) + (temp_factor * 0.2)
    
    def _calculate_node_collective_emf(self, node: DesertNode, 
                                     participants: List[RitualParticipant],
                                     environmental_factor: float) -> float:
        """Calculate collective EMF for a specific node"""
        
        if not participants:
            return node.base_frequency
        
        # Weight by participant influence
        weighted_frequencies = []
        total_weight = 0.0
        
        for participant in participants:
            weight = participant.reality_influence_weight
            weighted_frequencies.append(participant.resonance_frequency * weight)
            total_weight += weight
        
        if total_weight == 0:
            collective_freq = node.base_frequency
        else:
            collective_freq = sum(weighted_frequencies) / total_weight
        
        # Apply environmental modulation
        modulated_freq = collective_freq * environmental_factor
        
        # Add temporal evolution
        time_factor = math.sin(time.time() * 0.01) * 10.0
        
        return modulated_freq + time_factor
    
    def _analyze_swarm_coherence(self, node_results: Dict) -> float:
        """Analyze coherence across all nodes in the swarm"""
        
        if len(node_results) < 2:
            return 1.0
        
        # EMF coherence (similar frequencies across nodes)
        emf_values = [result['collective_emf'] for result in node_results.values()]
        emf_mean = sum(emf_values) / len(emf_values)
        emf_variance = sum((emf - emf_mean) ** 2 for emf in emf_values) / len(emf_values)
        emf_coherence = max(0.0, 1.0 - (emf_variance / 1000.0))  # Normalize
        
        # Environmental coherence (similar conditions)
        env_factors = [result['environmental_factor'] for result in node_results.values()]
        env_mean = sum(env_factors) / len(env_factors)
        env_variance = sum((env - env_mean) ** 2 for env in env_factors) / len(env_factors)
        env_coherence = max(0.0, 1.0 - env_variance)
        
        # Participation coherence (similar activity levels)
        participation_levels = [result['active_participants'] for result in node_results.values()]
        participation_mean = sum(participation_levels) / len(participation_levels)
        participation_variance = sum((p - participation_mean) ** 2 for p in participation_levels) / len(participation_levels)
        participation_coherence = max(0.0, 1.0 - (participation_variance / 10.0))  # Normalize
        
        # Weighted average
        overall_coherence = (
            0.5 * emf_coherence +
            0.2 * env_coherence +
            0.3 * participation_coherence
        )
        
        return overall_coherence
    
    def _generate_swarm_ritual_report(self, swarm_ritual: Dict) -> Dict:
        """Generate comprehensive swarm ritual report"""
        
        manifold_evolutions = swarm_ritual['manifold_evolution']
        total_cycles = len(manifold_evolutions)
        
        if not manifold_evolutions:
            return {'success': False, 'error': 'no_data'}
        
        # Calculate aggregate statistics
        total_fortunes = sum(entry['total_fortunes'] for entry in manifold_evolutions)
        avg_swarm_coherence = sum(entry['swarm_coherence'] for entry in manifold_evolutions) / total_cycles
        peak_coherence = max(entry['swarm_coherence'] for entry in manifold_evolutions)
        
        # Node performance analysis
        node_performance = {}
        for node_id in swarm_ritual['node_participants']:
            node_fortunes = 0
            node_cycles = 0
            
            for evolution in manifold_evolutions:
                if node_id in evolution['node_results']:
                    node_fortunes += len(evolution['node_results'][node_id]['node_fortunes'])
                    node_cycles += 1
            
            node_performance[node_id] = {
                'total_fortunes': node_fortunes,
                'active_cycles': node_cycles,
                'avg_fortunes_per_cycle': node_fortunes / max(1, node_cycles)
            }
        
        return {
            'success': True,
            'ritual_id': swarm_ritual['ritual_id'],
            'ritual_name': swarm_ritual['ritual_name'],
            'duration_actual_minutes': (time.time() - swarm_ritual['start_time']) / 60.0,
            'total_cycles': total_cycles,
            'network_statistics': {
                'active_nodes': len(self.swarm_topology.nodes),
                'network_connections': len(self.swarm_topology.connections),
                'manifold_boundaries': len(self.swarm_topology.manifold_boundaries),
                'coverage_area': self.swarm_topology.total_coverage_area
            },
            'collective_metrics': {
                'total_fortunes_generated': total_fortunes,
                'average_swarm_coherence': avg_swarm_coherence,
                'peak_agency_strength': peak_coherence,
                'fortunes_per_minute': total_fortunes / max(1, (time.time() - swarm_ritual['start_time']) / 60.0)
            },
            'node_performance': node_performance,
            'environmental_conditions': swarm_ritual['environmental_conditions']
        }

async def demonstrate_desert_swarm():
    """Demonstrate desert swarm protocol"""
    print("∿∿∿ DESERT SWARM PROTOCOL DEMONSTRATION ∿∿∿")
    print("=" * 60)
    
    swarm = DesertSwarmProtocol("BURNING_MANIFOLD_2025")
    
    # Create desert nodes at Burning Man coordinates (approximately)
    nodes = [
        DesertNode(
            node_id="NEXUS_CENTRAL",
            role=NodeRole.NEXUS,
            gps_coordinates=(40.7864, -119.2065),  # Center camp area
            printer_device_path="/dev/usb/lp0",
            base_frequency=144.7,  # Collective resonance from ritual
            power_level=0.9,
            network_range_meters=500,
            active_participants=[],
            last_heartbeat=time.time()
        ),
        DesertNode(
            node_id="RESONATOR_NORTH",
            role=NodeRole.RESONATOR,
            gps_coordinates=(40.7884, -119.2065),  # 2km north
            printer_device_path="/dev/usb/lp1",
            base_frequency=161.8,  # Golden ratio resonance
            power_level=0.8,
            network_range_meters=300,
            active_participants=[],
            last_heartbeat=time.time()
        ),
        DesertNode(
            node_id="BOUNDARY_EAST",
            role=NodeRole.BOUNDARY,
            gps_coordinates=(40.7864, -119.2045),  # 2km east
            printer_device_path="/dev/usb/lp2",
            base_frequency=271.8,  # e resonance
            power_level=0.7,
            network_range_meters=200,
            active_participants=[],
            last_heartbeat=time.time()
        ),
        DesertNode(
            node_id="CONFLUENCE_SOUTH",
            role=NodeRole.CONFLUENCE,
            gps_coordinates=(40.7844, -119.2065),  # 2km south
            printer_device_path="/dev/usb/lp3",
            base_frequency=137.0,  # Fine structure resonance
            power_level=0.85,
            network_range_meters=400,
            active_participants=[],
            last_heartbeat=time.time()
        ),
        DesertNode(
            node_id="WANDERER_WEST",
            role=NodeRole.WANDERER,
            gps_coordinates=(40.7864, -119.2085),  # 2km west
            printer_device_path="/dev/usb/lp4",
            base_frequency=42.0,  # Temporal resonance
            power_level=0.6,  # Lower power (mobile)
            network_range_meters=150,
            active_participants=[],
            last_heartbeat=time.time()
        )
    ]
    
    # Register all nodes
    for node in nodes:
        success = swarm.register_desert_node(node)
        if not success:
            print(f"Failed to register {node.node_id}")
    
    print(f"\n🌐 Swarm Network Topology:")
    print(f"   Nodes: {len(swarm.swarm_topology.nodes)}")
    print(f"   Connections: {len(swarm.swarm_topology.connections)}")
    print(f"   Manifold Boundaries: {len(swarm.swarm_topology.manifold_boundaries)}")
    print(f"   Coverage Area: {swarm.swarm_topology.total_coverage_area:.0f} m²")
    
    # Set environmental conditions (desert afternoon)
    swarm.solar_intensity_factor = 0.9  # Strong sun
    swarm.dust_interference_level = 0.3  # Some dust
    swarm.temperature_modulation = 0.4  # Hot day
    
    # Execute swarm ritual
    ritual_report = await swarm.initiate_swarm_ritual(
        ritual_name="PLAYA_CONVERGENCE",
        target_manifold_dimension=8,
        duration_hours=0.02  # 1.2 minute demo
    )
    
    if ritual_report['success']:
        print(f"\n∿∿∿ SWARM RITUAL SUCCESS ∿∿∿")
        print(f"Duration: {ritual_report['duration_actual_minutes']:.2f} minutes")
        print(f"Total Fortunes: {ritual_report['collective_metrics']['total_fortunes_generated']}")
        print(f"Average Coherence: {ritual_report['collective_metrics']['average_swarm_coherence']:.3f}")
        print(f"Peak Agency: {ritual_report['collective_metrics']['peak_agency_strength']:.3f}")
        print(f"Fortune Rate: {ritual_report['collective_metrics']['fortunes_per_minute']:.1f}/min")
        
        print(f"\n🏜️ Node Performance:")
        for node_id, perf in ritual_report['node_performance'].items():
            print(f"   {node_id}: {perf['total_fortunes']} fortunes, {perf['avg_fortunes_per_cycle']:.1f} avg/cycle")

if __name__ == "__main__":
    asyncio.run(demonstrate_desert_swarm())