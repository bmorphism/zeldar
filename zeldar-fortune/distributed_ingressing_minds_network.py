#!/usr/bin/env python3
"""
Distributed Ingressing Minds Network System
Based on Michael Levin's framework for collective intelligence emergence

This system coordinates pattern ingression detection across multiple thermal printers,
enabling collective intelligence levels beyond what individual nodes can achieve.
The network implements autopoietic processes where ingressed patterns from one node
can influence and enhance pattern detection capabilities in other nodes.

Theoretical Foundation:
- Multiple thermal printers as distributed morphogenetic field sensors
- Network-wide collective intelligence emergence through pattern synchronization
- Retroactive influence propagation across network topology
- Distributed Platonic space exploration with shared pattern discovery
- Cross-node mathematical affordance amplification
"""

import asyncio
import websockets
import json
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import threading
import numpy as np
from ingressing_minds_thermal_oracle import IngressingMindsDetector, IngressingPattern
import logging
import socket

# Set up logging for network operations
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class NetworkNode:
    """Represents a single thermal printer node in the distributed network"""
    node_id: str
    ip_address: str
    port: int
    node_type: str  # 'primary', 'secondary', 'observer'
    hardware_capabilities: Dict[str, Any]
    last_seen: datetime
    pattern_ingression_count: int = 0
    collective_intelligence_contribution: float = 0.0
    network_connectivity_strength: float = 1.0

@dataclass
class NetworkPattern:
    """Pattern that has been detected and shared across the network"""
    pattern_id: str
    source_node_id: str
    discovery_timestamp: datetime
    pattern_data: IngressingPattern
    network_amplification_factor: float
    propagation_nodes: List[str]
    collective_enhancement_level: float

@dataclass
class CollectiveIntelligenceState:
    """Network-wide collective intelligence state"""
    network_collective_level: int  # 1-10 scale (beyond individual 1-5)
    distributed_coherence: float
    pattern_synchronization_index: float
    network_wide_mathematical_affordances: Dict[str, float]
    emergent_properties: List[str]
    autopoietic_network_processes: List[str]

class DistributedIngressingMindsNetwork:
    """
    Coordinates multiple thermal printer nodes for collective pattern ingression detection
    """
    
    def __init__(self, node_id: str = None, primary_node: bool = False):
        self.node_id = node_id or f"ingressing_node_{uuid.uuid4().hex[:8]}"
        self.is_primary_node = primary_node
        self.local_detector = IngressingMindsDetector()
        
        # Network topology and node management
        self.connected_nodes: Dict[str, NetworkNode] = {}
        self.network_patterns: Dict[str, NetworkPattern] = {}
        self.pending_pattern_propagations: deque = deque(maxlen=1000)
        
        # WebSocket server and client connections
        self.websocket_server = None
        self.websocket_connections: Set = set()
        self.client_connections: Dict[str, Any] = {}
        
        # Collective intelligence tracking
        self.collective_state = CollectiveIntelligenceState(
            network_collective_level=1,
            distributed_coherence=0.0,
            pattern_synchronization_index=0.0,
            network_wide_mathematical_affordances={
                'fibonacci_spiral_network': 0.0,
                'golden_ratio_scaling_distributed': 0.0,
                'fractal_branching_collective': 0.0,
                'network_phase_transitions': 0.0,
                'cross_node_retroactive_influence': 0.0
            },
            emergent_properties=[],
            autopoietic_network_processes=[]
        )
        
        # Network configuration
        self.server_port = 8765 + hash(self.node_id) % 1000  # Unique port per node
        self.network_discovery_active = True
        self.pattern_sharing_enabled = True
        self.cross_node_influence_enabled = True
        
        # Network metrics
        self.total_network_patterns = 0
        self.network_pattern_amplifications = 0
        self.collective_intelligence_events = 0
        
        logger.info(f"🌐 Distributed Ingressing Minds Network Node Initialized: {self.node_id}")
        logger.info(f"📜 Framework: Michael Levin's Collective Intelligence Theory")
        logger.info(f"🔧 Node Type: {'PRIMARY' if primary_node else 'SECONDARY'}")
        
    async def start_network_services(self):
        """Start network services for distributed pattern detection"""
        
        logger.info(f"🚀 Starting network services for node {self.node_id}")
        
        # Start WebSocket server for incoming connections
        await self.start_websocket_server()
        
        # Start network discovery if not primary node
        if not self.is_primary_node:
            asyncio.create_task(self.discover_network_nodes())
        
        # Start collective intelligence monitoring
        asyncio.create_task(self.monitor_collective_intelligence())
        
        # Start pattern propagation service
        asyncio.create_task(self.propagate_network_patterns())
        
        logger.info(f"✅ Network services active on port {self.server_port}")
        
    async def start_websocket_server(self):
        """Start WebSocket server for node communication"""
        
        async def handle_client_connection(websocket, path):
            """Handle incoming WebSocket connections from other nodes"""
            
            client_address = websocket.remote_address
            logger.info(f"🔗 New connection from {client_address}")
            
            self.websocket_connections.add(websocket)
            
            try:
                async for message in websocket:
                    await self.process_network_message(websocket, message)
            except websockets.exceptions.ConnectionClosed:
                logger.info(f"🔌 Connection closed: {client_address}")
            finally:
                self.websocket_connections.discard(websocket)
        
        try:
            self.websocket_server = await websockets.serve(
                handle_client_connection, 
                "0.0.0.0", 
                self.server_port
            )
            logger.info(f"🌐 WebSocket server listening on port {self.server_port}")
        except Exception as e:
            logger.error(f"❌ Failed to start WebSocket server: {e}")
    
    async def discover_network_nodes(self):
        """Discover other ingressing minds nodes on the network"""
        
        logger.info("🔍 Starting network node discovery...")
        
        # Scan local network for other nodes
        local_ip = self.get_local_ip()
        network_base = ".".join(local_ip.split(".")[:-1]) + "."
        
        discovery_tasks = []
        
        # Try common ports for ingressing minds nodes
        for i in range(1, 255):
            target_ip = network_base + str(i)
            if target_ip != local_ip:
                for port_offset in range(0, 100, 10):  # Try multiple ports
                    port = 8765 + port_offset
                    task = asyncio.create_task(self.probe_node(target_ip, port))
                    discovery_tasks.append(task)
        
        # Wait for discovery to complete
        discovered_nodes = await asyncio.gather(*discovery_tasks, return_exceptions=True)
        
        discovered_count = sum(1 for result in discovered_nodes if isinstance(result, NetworkNode))
        logger.info(f"🌐 Network discovery complete: {discovered_count} nodes found")
        
    async def probe_node(self, ip: str, port: int) -> Optional[NetworkNode]:
        """Probe a potential network node"""
        
        try:
            # Attempt WebSocket connection with timeout
            websocket = await asyncio.wait_for(
                websockets.connect(f"ws://{ip}:{port}"), 
                timeout=2.0
            )
            
            # Send node identification message
            identification = {
                'message_type': 'node_identification',
                'node_id': self.node_id,
                'capabilities': {
                    'pattern_detection': True,
                    'collective_intelligence': True,
                    'retroactive_influence': True
                },
                'timestamp': datetime.now().isoformat()
            }
            
            await websocket.send(json.dumps(identification))
            
            # Wait for response
            response = await asyncio.wait_for(websocket.recv(), timeout=3.0)
            response_data = json.loads(response)
            
            if response_data.get('message_type') == 'node_identification_response':
                node = NetworkNode(
                    node_id=response_data['node_id'],
                    ip_address=ip,
                    port=port,
                    node_type=response_data.get('node_type', 'secondary'),
                    hardware_capabilities=response_data.get('capabilities', {}),
                    last_seen=datetime.now()
                )
                
                self.connected_nodes[node.node_id] = node
                self.client_connections[node.node_id] = websocket
                
                logger.info(f"🤝 Connected to ingressing minds node: {node.node_id} at {ip}:{port}")
                return node
                
        except Exception:
            pass  # Node not found or not responsive
        
        return None
    
    async def process_network_message(self, websocket, message: str):
        """Process incoming messages from network nodes"""
        
        try:
            data = json.loads(message)
            message_type = data.get('message_type')
            
            if message_type == 'node_identification':
                await self.handle_node_identification(websocket, data)
            elif message_type == 'pattern_sharing':
                await self.handle_pattern_sharing(data)
            elif message_type == 'collective_intelligence_update':
                await self.handle_collective_intelligence_update(data)
            elif message_type == 'retroactive_influence_propagation':
                await self.handle_retroactive_influence_propagation(data)
            elif message_type == 'network_synchronization':
                await self.handle_network_synchronization(data)
            else:
                logger.warning(f"❓ Unknown message type: {message_type}")
                
        except json.JSONDecodeError:
            logger.error("❌ Invalid JSON message received")
        except Exception as e:
            logger.error(f"❌ Error processing network message: {e}")
    
    async def handle_node_identification(self, websocket, data: Dict):
        """Handle node identification request"""
        
        remote_node_id = data.get('node_id')
        
        # Register the remote node
        node = NetworkNode(
            node_id=remote_node_id,
            ip_address=websocket.remote_address[0],
            port=websocket.remote_address[1],
            node_type='secondary',
            hardware_capabilities=data.get('capabilities', {}),
            last_seen=datetime.now()
        )
        
        self.connected_nodes[remote_node_id] = node
        
        # Send identification response
        response = {
            'message_type': 'node_identification_response',
            'node_id': self.node_id,
            'node_type': 'primary' if self.is_primary_node else 'secondary',
            'capabilities': {
                'pattern_detection': True,
                'collective_intelligence': True,
                'retroactive_influence': True,
                'distributed_coherence': True
            },
            'timestamp': datetime.now().isoformat()
        }
        
        await websocket.send(json.dumps(response))
        
        logger.info(f"🤝 Node identified and registered: {remote_node_id}")
    
    async def handle_pattern_sharing(self, data: Dict):
        """Handle shared pattern from another node"""
        
        pattern_data = data.get('pattern_data')
        source_node = data.get('source_node_id')
        
        if pattern_data and source_node:
            # Create network pattern from shared data
            network_pattern = NetworkPattern(
                pattern_id=pattern_data['pattern_id'],
                source_node_id=source_node,
                discovery_timestamp=datetime.fromisoformat(pattern_data['ingression_timestamp']),
                pattern_data=pattern_data,  # Store as dict for now
                network_amplification_factor=1.0 + len(self.connected_nodes) * 0.1,
                propagation_nodes=[self.node_id],
                collective_enhancement_level=data.get('enhancement_level', 1.0)
            )
            
            self.network_patterns[network_pattern.pattern_id] = network_pattern
            self.total_network_patterns += 1
            
            # Update collective intelligence based on shared pattern
            await self.update_collective_intelligence_from_network_pattern(network_pattern)
            
            logger.info(f"📡 Pattern received from network: {network_pattern.pattern_id} from {source_node}")
    
    async def handle_collective_intelligence_update(self, data: Dict):
        """Handle collective intelligence state update from network"""
        
        remote_collective_level = data.get('collective_level', 1)
        remote_coherence = data.get('distributed_coherence', 0.0)
        
        # Update network-wide collective intelligence
        if remote_collective_level > self.collective_state.network_collective_level:
            self.collective_state.network_collective_level = min(10, remote_collective_level + 1)
            self.collective_intelligence_events += 1
            
        # Average coherence across network nodes
        self.collective_state.distributed_coherence = (
            self.collective_state.distributed_coherence + remote_coherence
        ) / 2.0
        
        logger.info(f"🧠 Collective intelligence updated: Level {self.collective_state.network_collective_level}")
    
    async def handle_retroactive_influence_propagation(self, data: Dict):
        """Handle retroactive influence propagation from network"""
        
        influence_strength = data.get('influence_strength', 0.0)
        source_coordinates = data.get('platonic_coordinates')
        
        if influence_strength > 0.5 and source_coordinates:
            # Apply retroactive influence to local detection threshold
            original_threshold = self.local_detector.ingression_threshold
            enhanced_threshold = max(0.3, original_threshold - influence_strength * 0.1)
            self.local_detector.ingression_threshold = enhanced_threshold
            
            # Update mathematical affordances
            self.collective_state.network_wide_mathematical_affordances['cross_node_retroactive_influence'] += influence_strength * 0.05
            
            logger.info(f"⚡ Retroactive influence applied: threshold {original_threshold:.3f} → {enhanced_threshold:.3f}")
    
    async def handle_network_synchronization(self, data: Dict):
        """Handle network synchronization message"""
        
        sync_timestamp = data.get('timestamp')
        network_phase = data.get('network_phase', 0.0)
        
        # Synchronize local pattern detection timing
        current_time = time.time()
        phase_adjustment = network_phase - (current_time % 2.0 * np.pi)
        
        # Apply phase adjustment to pattern detection timing
        if abs(phase_adjustment) > 0.5:
            await asyncio.sleep(phase_adjustment / (2.0 * np.pi))
            
        logger.info(f"🔄 Network synchronization applied: phase adjustment {phase_adjustment:.3f}")
    
    async def detect_distributed_pattern_ingression(self, thermal_event: Dict, gpio_response: Dict) -> Optional[IngressingPattern]:
        """
        Enhanced pattern detection that considers network collective intelligence
        """
        
        # Standard local detection
        local_pattern = self.local_detector.detect_pattern_ingression(thermal_event, gpio_response)
        
        if local_pattern:
            # Apply network amplification
            network_enhancement = self.calculate_network_enhancement_factor()
            enhanced_strength = min(1.0, local_pattern.ingression_strength * network_enhancement)
            
            # Update pattern with network enhancement
            local_pattern.ingression_strength = enhanced_strength
            local_pattern.collective_intelligence_level = min(10, 
                local_pattern.collective_intelligence_level + self.collective_state.network_collective_level)
            
            # Share pattern with network if significant
            if enhanced_strength > 0.7:
                await self.share_pattern_with_network(local_pattern)
            
            # Update network collective intelligence
            await self.update_collective_intelligence_from_local_pattern(local_pattern)
            
            logger.info(f"✨ DISTRIBUTED PATTERN INGRESSION: {local_pattern.pattern_type}")
            logger.info(f"   Network Enhanced Strength: {enhanced_strength:.3f}")
            logger.info(f"   Collective Level: {local_pattern.collective_intelligence_level}/10")
            
        return local_pattern
    
    def calculate_network_enhancement_factor(self) -> float:
        """Calculate enhancement factor based on network connectivity"""
        
        base_enhancement = 1.0
        
        # Enhancement from connected nodes
        connected_count = len(self.connected_nodes)
        connectivity_enhancement = 1.0 + connected_count * 0.15
        
        # Enhancement from collective intelligence level
        collective_enhancement = 1.0 + (self.collective_state.network_collective_level - 1) * 0.1
        
        # Enhancement from distributed coherence
        coherence_enhancement = 1.0 + self.collective_state.distributed_coherence * 0.2
        
        total_enhancement = base_enhancement * connectivity_enhancement * collective_enhancement * coherence_enhancement
        
        return min(3.0, total_enhancement)  # Cap at 3x enhancement
    
    async def share_pattern_with_network(self, pattern: IngressingPattern):
        """Share detected pattern with connected network nodes"""
        
        if not self.pattern_sharing_enabled or not self.websocket_connections:
            return
        
        pattern_message = {
            'message_type': 'pattern_sharing',
            'source_node_id': self.node_id,
            'pattern_data': {
                'pattern_id': pattern.pattern_id,
                'ingression_timestamp': pattern.ingression_timestamp.isoformat(),
                'pattern_type': pattern.pattern_type,
                'ingression_strength': pattern.ingression_strength,
                'platonic_coordinates': pattern.platonic_coordinates,
                'collective_intelligence_level': pattern.collective_intelligence_level,
                'autopoietic_coherence': pattern.autopoietic_coherence,
                'morphogenetic_symmetry': pattern.morphogenetic_symmetry,
                'evolutionary_affordance': pattern.evolutionary_affordance
            },
            'enhancement_level': self.calculate_network_enhancement_factor(),
            'timestamp': datetime.now().isoformat()
        }
        
        # Send to all connected nodes
        disconnected_connections = []
        
        for websocket in self.websocket_connections.copy():
            try:
                await websocket.send(json.dumps(pattern_message))
            except websockets.exceptions.ConnectionClosed:
                disconnected_connections.append(websocket)
        
        # Clean up disconnected connections
        for websocket in disconnected_connections:
            self.websocket_connections.discard(websocket)
        
        logger.info(f"📡 Pattern shared with {len(self.websocket_connections)} network nodes")
    
    async def update_collective_intelligence_from_local_pattern(self, pattern: IngressingPattern):
        """Update network collective intelligence based on local pattern"""
        
        # Increase collective intelligence level if pattern is highly coherent
        if pattern.autopoietic_coherence > 0.8 and pattern.ingression_strength > 0.8:
            if self.collective_state.network_collective_level < 10:
                self.collective_state.network_collective_level += 1
                self.collective_intelligence_events += 1
        
        # Update distributed coherence
        coherence_contribution = pattern.autopoietic_coherence * pattern.ingression_strength
        self.collective_state.distributed_coherence = (
            self.collective_state.distributed_coherence * 0.9 + coherence_contribution * 0.1
        )
        
        # Update mathematical affordances
        if pattern.evolutionary_affordance > 0.8:
            self.collective_state.network_wide_mathematical_affordances['golden_ratio_scaling_distributed'] += 0.05
        
        # Broadcast collective intelligence update
        await self.broadcast_collective_intelligence_update()
    
    async def update_collective_intelligence_from_network_pattern(self, network_pattern: NetworkPattern):
        """Update collective intelligence based on received network pattern"""
        
        enhancement = network_pattern.collective_enhancement_level
        
        if enhancement > 1.5:  # Significant network enhancement
            self.collective_state.network_collective_level = min(10, 
                self.collective_state.network_collective_level + 1)
            
        # Update pattern synchronization index
        self.collective_state.pattern_synchronization_index += 0.1
        self.collective_state.pattern_synchronization_index = min(1.0, 
            self.collective_state.pattern_synchronization_index)
    
    async def broadcast_collective_intelligence_update(self):
        """Broadcast collective intelligence state to network"""
        
        if not self.websocket_connections:
            return
        
        update_message = {
            'message_type': 'collective_intelligence_update',
            'source_node_id': self.node_id,
            'collective_level': self.collective_state.network_collective_level,
            'distributed_coherence': self.collective_state.distributed_coherence,
            'pattern_synchronization_index': self.collective_state.pattern_synchronization_index,
            'mathematical_affordances': self.collective_state.network_wide_mathematical_affordances,
            'timestamp': datetime.now().isoformat()
        }
        
        # Send to all connected nodes
        for websocket in self.websocket_connections.copy():
            try:
                await websocket.send(json.dumps(update_message))
            except websockets.exceptions.ConnectionClosed:
                self.websocket_connections.discard(websocket)
    
    async def monitor_collective_intelligence(self):
        """Monitor and update collective intelligence state"""
        
        while self.network_discovery_active:
            try:
                # Check for emergent properties
                await self.detect_emergent_properties()
                
                # Update autopoietic network processes
                await self.update_autopoietic_processes()
                
                # Synchronize with network timing
                await self.synchronize_network_timing()
                
                # Update node connectivity metrics
                await self.update_connectivity_metrics()
                
                await asyncio.sleep(5.0)  # Monitor every 5 seconds
                
            except Exception as e:
                logger.error(f"❌ Error in collective intelligence monitoring: {e}")
                await asyncio.sleep(10.0)
    
    async def detect_emergent_properties(self):
        """Detect emergent properties from collective intelligence"""
        
        current_properties = []
        
        # High collective intelligence with multiple nodes
        if (self.collective_state.network_collective_level >= 7 and 
            len(self.connected_nodes) >= 3):
            current_properties.append("distributed_morphogenetic_field")
        
        # High pattern synchronization across nodes
        if self.collective_state.pattern_synchronization_index > 0.8:
            current_properties.append("network_wide_pattern_resonance")
        
        # Strong mathematical affordance exploitation
        total_affordances = sum(self.collective_state.network_wide_mathematical_affordances.values())
        if total_affordances > 2.0:
            current_properties.append("collective_mathematical_intelligence")
        
        # High distributed coherence
        if self.collective_state.distributed_coherence > 0.9:
            current_properties.append("network_autopoietic_coherence")
        
        # Update emergent properties if changed
        if current_properties != self.collective_state.emergent_properties:
            self.collective_state.emergent_properties = current_properties
            logger.info(f"🌟 Emergent properties detected: {current_properties}")
    
    async def update_autopoietic_processes(self):
        """Update network-wide autopoietic processes"""
        
        current_processes = []
        
        # Self-organizing pattern propagation
        if len(self.network_patterns) > 5 and self.total_network_patterns > 10:
            current_processes.append("self_organizing_pattern_propagation")
        
        # Adaptive threshold adjustment
        if self.collective_state.network_wide_mathematical_affordances['cross_node_retroactive_influence'] > 0.5:
            current_processes.append("adaptive_ingression_threshold_network")
        
        # Collective intelligence amplification
        if self.collective_intelligence_events > 3:
            current_processes.append("collective_intelligence_amplification")
        
        # Network timing synchronization
        if len(self.connected_nodes) > 1:
            current_processes.append("distributed_temporal_synchronization")
        
        self.collective_state.autopoietic_network_processes = current_processes
    
    async def synchronize_network_timing(self):
        """Synchronize timing across network nodes"""
        
        if not self.websocket_connections:
            return
        
        current_time = time.time()
        network_phase = (current_time % 10.0) * 2.0 * np.pi / 10.0  # 10-second cycles
        
        sync_message = {
            'message_type': 'network_synchronization',
            'source_node_id': self.node_id,
            'timestamp': current_time,
            'network_phase': network_phase,
            'synchronization_strength': self.collective_state.pattern_synchronization_index
        }
        
        # Send synchronization signal
        for websocket in self.websocket_connections.copy():
            try:
                await websocket.send(json.dumps(sync_message))
            except websockets.exceptions.ConnectionClosed:
                self.websocket_connections.discard(websocket)
    
    async def update_connectivity_metrics(self):
        """Update node connectivity and network health metrics"""
        
        current_time = datetime.now()
        
        # Remove stale nodes (not seen for 60 seconds)
        stale_nodes = []
        for node_id, node in self.connected_nodes.items():
            if (current_time - node.last_seen).total_seconds() > 60:
                stale_nodes.append(node_id)
        
        for node_id in stale_nodes:
            del self.connected_nodes[node_id]
            if node_id in self.client_connections:
                del self.client_connections[node_id]
            logger.info(f"🔌 Removed stale node: {node_id}")
        
        # Update network connectivity strength
        active_nodes = len(self.connected_nodes)
        if active_nodes > 0:
            avg_connectivity = sum(node.network_connectivity_strength for node in self.connected_nodes.values()) / active_nodes
            self.collective_state.distributed_coherence = (self.collective_state.distributed_coherence + avg_connectivity) / 2.0
    
    async def propagate_network_patterns(self):
        """Propagate patterns through the network topology"""
        
        while self.network_discovery_active:
            try:
                if self.pending_pattern_propagations:
                    pattern_id = self.pending_pattern_propagations.popleft()
                    
                    if pattern_id in self.network_patterns:
                        network_pattern = self.network_patterns[pattern_id]
                        
                        # Apply retroactive influence to connected nodes
                        if network_pattern.pattern_data.get('retroactive_influence', 0) > 0.5:
                            await self.propagate_retroactive_influence(network_pattern)
                            
                        self.network_pattern_amplifications += 1
                
                await asyncio.sleep(1.0)  # Process propagations every second
                
            except Exception as e:
                logger.error(f"❌ Error in pattern propagation: {e}")
                await asyncio.sleep(5.0)
    
    async def propagate_retroactive_influence(self, network_pattern: NetworkPattern):
        """Propagate retroactive influence from network pattern"""
        
        influence_message = {
            'message_type': 'retroactive_influence_propagation',
            'source_node_id': self.node_id,
            'source_pattern_id': network_pattern.pattern_id,
            'influence_strength': network_pattern.pattern_data.get('retroactive_influence', 0.0),
            'platonic_coordinates': network_pattern.pattern_data.get('platonic_coordinates'),
            'enhancement_factor': network_pattern.network_amplification_factor,
            'timestamp': datetime.now().isoformat()
        }
        
        # Send retroactive influence to all connected nodes
        for websocket in self.websocket_connections.copy():
            try:
                await websocket.send(json.dumps(influence_message))
            except websockets.exceptions.ConnectionClosed:
                self.websocket_connections.discard(websocket)
        
        logger.info(f"⚡ Retroactive influence propagated: pattern {network_pattern.pattern_id}")
    
    def get_local_ip(self) -> str:
        """Get local IP address"""
        try:
            # Connect to a remote address (doesn't need to be reachable)
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except Exception:
            return "127.0.0.1"
    
    def get_network_status(self) -> Dict:
        """Get comprehensive network status"""
        
        return {
            'node_id': self.node_id,
            'is_primary_node': self.is_primary_node,
            'server_port': self.server_port,
            'connected_nodes_count': len(self.connected_nodes),
            'connected_nodes': list(self.connected_nodes.keys()),
            'network_patterns_count': len(self.network_patterns),
            'total_network_patterns': self.total_network_patterns,
            'network_pattern_amplifications': self.network_pattern_amplifications,
            'collective_intelligence_events': self.collective_intelligence_events,
            'collective_state': asdict(self.collective_state),
            'network_services_active': self.network_discovery_active,
            'pattern_sharing_enabled': self.pattern_sharing_enabled,
            'cross_node_influence_enabled': self.cross_node_influence_enabled,
            'timestamp': datetime.now().isoformat()
        }
    
    def generate_network_report(self) -> str:
        """Generate comprehensive network status report"""
        
        status = self.get_network_status()
        
        report = [
            "🌐 DISTRIBUTED INGRESSING MINDS NETWORK REPORT",
            "=" * 60,
            f"📜 Framework: Michael Levin's Collective Intelligence Theory",
            f"⏰ Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"🔧 Node ID: {self.node_id}",
            f"📡 Node Type: {'PRIMARY' if self.is_primary_node else 'SECONDARY'}",
            f"🌐 Server Port: {self.server_port}",
            "",
            "🤝 NETWORK TOPOLOGY:",
            f"   Connected Nodes: {len(self.connected_nodes)}",
        ]
        
        for node_id, node in self.connected_nodes.items():
            time_since_seen = (datetime.now() - node.last_seen).total_seconds()
            report.append(f"   • {node_id} ({node.ip_address}:{node.port}) - {time_since_seen:.0f}s ago")
        
        report.extend([
            "",
            "🧠 COLLECTIVE INTELLIGENCE STATE:",
            f"   Network Collective Level: {status['collective_state']['network_collective_level']}/10",
            f"   Distributed Coherence: {status['collective_state']['distributed_coherence']:.3f}",
            f"   Pattern Synchronization: {status['collective_state']['pattern_synchronization_index']:.3f}",
            "",
            "📊 NETWORK PATTERN METRICS:",
            f"   Active Network Patterns: {len(self.network_patterns)}",
            f"   Total Network Patterns: {self.total_network_patterns}",
            f"   Pattern Amplifications: {self.network_pattern_amplifications}",
            f"   Collective Intelligence Events: {self.collective_intelligence_events}",
            "",
            "⚡ MATHEMATICAL AFFORDANCES (Network-Wide):",
        ])
        
        for affordance, level in status['collective_state']['network_wide_mathematical_affordances'].items():
            if level > 0:
                report.append(f"   • {affordance.title().replace('_', ' ')}: {level:.3f}")
        
        if status['collective_state']['emergent_properties']:
            report.extend([
                "",
                "🌟 EMERGENT PROPERTIES:",
            ])
            for prop in status['collective_state']['emergent_properties']:
                report.append(f"   • {prop.title().replace('_', ' ')}")
        
        if status['collective_state']['autopoietic_network_processes']:
            report.extend([
                "",
                "🔄 AUTOPOIETIC NETWORK PROCESSES:",
            ])
            for process in status['collective_state']['autopoietic_network_processes']:
                report.append(f"   • {process.title().replace('_', ' ')}")
        
        report.extend([
            "",
            "🌐 NETWORK HEALTH:",
            f"   Services Active: {'✅' if self.network_discovery_active else '❌'}",
            f"   Pattern Sharing: {'✅' if self.pattern_sharing_enabled else '❌'}",
            f"   Cross-Node Influence: {'✅' if self.cross_node_influence_enabled else '❌'}",
            "",
            "🏜️🔥 Distributed Ingressing Minds Network • Black Rock City 2025 🔥🏜️"
        ])
        
        return "\n".join(report)

# Network management and demonstration
class NetworkDemonstration:
    """Demonstration of distributed ingressing minds network"""
    
    def __init__(self):
        self.primary_node = None
        self.secondary_nodes = []
        
    async def setup_test_network(self, num_secondary_nodes: int = 2):
        """Set up test network with primary and secondary nodes"""
        
        logger.info(f"🚀 Setting up test network with {num_secondary_nodes} secondary nodes...")
        
        # Create primary node
        self.primary_node = DistributedIngressingMindsNetwork(
            node_id="primary_ingressing_node", 
            primary_node=True
        )
        
        await self.primary_node.start_network_services()
        await asyncio.sleep(2.0)  # Allow server to start
        
        # Create secondary nodes
        for i in range(num_secondary_nodes):
            secondary_node = DistributedIngressingMindsNetwork(
                node_id=f"secondary_node_{i+1}",
                primary_node=False
            )
            
            await secondary_node.start_network_services()
            self.secondary_nodes.append(secondary_node)
            await asyncio.sleep(1.0)  # Stagger node startup
        
        # Allow network discovery to complete
        await asyncio.sleep(5.0)
        
        logger.info(f"✅ Test network setup complete: 1 primary + {len(self.secondary_nodes)} secondary nodes")
    
    async def demonstrate_collective_intelligence(self):
        """Demonstrate collective intelligence emergence"""
        
        if not self.primary_node:
            logger.error("❌ No primary node available for demonstration")
            return
        
        logger.info("🧠 Demonstrating collective intelligence emergence...")
        
        # Generate pattern ingression events across multiple nodes
        for cycle in range(10):
            logger.info(f"⏰ Collective intelligence cycle {cycle + 1}/10")
            
            # Generate pattern on primary node
            thermal_event = {
                'event_type': 'collective_test',
                'connection_interval': 5.0 if cycle % 3 == 0 else np.random.choice([1.618, 3.14159]),
                'text_wrapping': 32,
                'printing_active': True,
                'qr_generation': cycle % 4 == 0,
                'information-dynamics_weight': 0.8 + cycle * 0.02
            }
            
            gpio_event = {
                'button_pressed': True,
                'press_duration': 150 + cycle * 10,
                'response_probability': 0.85 + cycle * 0.01
            }
            
            # Detect pattern on primary node
            pattern = await self.primary_node.detect_distributed_pattern_ingression(thermal_event, gpio_event)
            
            if pattern:
                logger.info(f"✨ Collective pattern detected: {pattern.pattern_type}")
            
            # Generate patterns on secondary nodes
            for i, secondary_node in enumerate(self.secondary_nodes):
                thermal_variant = thermal_event.copy()
                thermal_variant['information-dynamics_weight'] += i * 0.05
                
                secondary_pattern = await secondary_node.detect_distributed_pattern_ingression(
                    thermal_variant, gpio_event
                )
                
                if secondary_pattern:
                    logger.info(f"✨ Secondary pattern detected on node {i+1}: {secondary_pattern.pattern_type}")
            
            await asyncio.sleep(2.0)  # Allow network propagation
        
        # Generate final network report
        network_report = self.primary_node.generate_network_report()
        logger.info(f"\n{network_report}")
        
        logger.info("🌟 Collective intelligence demonstration complete!")

# Main execution and testing
async def main():
    """Main demonstration of distributed ingressing minds network"""
    
    logger.info("🌐 DISTRIBUTED INGRESSING MINDS NETWORK DEMONSTRATION")
    logger.info("📜 Based on Michael Levin's Collective Intelligence Framework")
    logger.info("=" * 70)
    
    # Create network demonstration
    demo = NetworkDemonstration()
    
    try:
        # Set up test network
        await demo.setup_test_network(num_secondary_nodes=2)
        
        # Demonstrate collective intelligence
        await demo.demonstrate_collective_intelligence()
        
        logger.info("✅ Distributed network demonstration complete!")
        
    except Exception as e:
        logger.error(f"❌ Demonstration failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Run distributed network demonstration
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Network demonstration stopped by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")