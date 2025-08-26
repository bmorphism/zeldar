# Gemini Live JSON Stream Setup

## 🎯 **Objective**
Get Gemini Live API streaming **structured JSON output** for information-dynamics oracle integration.

## 🚀 **Quick Start**

### **1. Install Dependencies**
```bash
pip install websockets pyaudio
# or
pip install -r requirements_gemini_live.txt
```

### **2. Set API Key**
```bash
export GEMINI_API_KEY="your-gemini-api-key-here"
```

### **3. Run JSON Stream**
```bash
python3 gemini_live_json_stream.py
```

### **4. Test JSON Output**
```bash
python3 test_gemini_live.py
```

## 💡 **Usage Examples**

### **Interactive Session**
```
💬 Input: Generate information-dynamics metrics in JSON format
📋 JSON OUTPUT:
{
  "information-dynamics_phi": 2.87,
  "analysis": "InformationForce parameters within normal range",
  "timestamp": 1755950000.123,
  "response_type": "structured_analysis"
}
```

### **Audio Input Mode**
```
💬 Input: audio
🎤 Audio input started
[Speak into microphone]
📋 JSON OUTPUT:
{
  "voice_analysis": "Voice information-dynamics detection active",
  "information-dynamics_phi": 3.14,
  "audio_processed": true
}
```

## 🏗️ **Architecture**

### **Core Components**
```
GeminiLiveJSONStream
├─ WebSocket Connection: Real-time bidirectional communication  
├─ Audio Processing: PyAudio input stream with base64 encoding
├─ JSON Parser: Extracts structured data from responses
└─ Interactive Interface: Text and voice input handling
```

### **API Configuration**
- **Model**: `gemini-2.0-flash-exp`
- **Response Modalities**: `AUDIO` + `TEXT`
- **Voice**: `Aoede` (high expressiveness)
- **System Instruction**: InformationForce oracle with JSON output

### **JSON Output Format**
```json
{
  "information-dynamics_phi": 3.227,
  "response_text": "Analysis content",
  "timestamp": 1755950000,
  "response_type": "information-dynamics_analysis",
  "element": "MYSTERY",
  "quantum_entropy": 0.914
}
```

## 🔧 **Integration with Oracle System**

### **Connection Points**
1. **JSON Parser**: Extracts information-dynamics metrics → `current_loop_state.json`
2. **Audio Input**: Voice triggers → `button_quick_phrase_trigger.py`
3. **Structured Output**: Gemini analysis → Oracle system processing
4. **Real-time Stream**: Continuous information-dynamics monitoring

### **Oracle Integration Example**
```python
# In your Oracle system:
from gemini_live_json_stream import GeminiLiveJSONStream

async def integrate_gemini_information-dynamics():
    client = GeminiLiveJSONStream(api_key)
    await client.connect()
    
    # Send Oracle state to Gemini
    oracle_state = load_current_loop_state()
    prompt = f"Analyze information-dynamics state: {oracle_state}"
    await client.send_text_message(prompt)
    
    # Receive JSON analysis
    # (handled by listen_for_responses)
```

## ⚡ **Performance Characteristics**

- **Latency**: WebSocket streaming (500ms-2s response)
- **Audio**: 16kHz PCM, real-time processing
- **JSON Parsing**: Automatic extraction and validation
- **Error Handling**: Connection recovery and graceful failures
- **Memory**: Minimal footprint, streaming architecture

## 🎯 **Use Cases**

### **InformationForce Oracle Enhancement**
- **Voice-activated information-dynamics analysis**
- **Real-time information-dynamics metric generation**  
- **Structured output for system integration**
- **Multimodal information-dynamics assessment**

### **Interactive Applications**
- **Voice-controlled fortune generation**
- **Real-time information-dynamics monitoring**
- **Structured data collection from conversations**
- **JSON API bridge for web interfaces**

## 🔍 **Testing & Validation**

### **Test Scenarios**
1. **JSON Structure Validation**: Verify correct field extraction
2. **Audio Processing**: Test voice input → JSON output
3. **Error Handling**: Connection failures and recovery
4. **Integration**: Oracle system compatibility

### **Expected JSON Fields**
- `information-dynamics_phi`: Numerical information-dynamics coefficient
- `response_text`: Natural language analysis
- `timestamp`: Response generation time
- `response_type`: Classification of response
- Optional: `element`, `quantum_entropy`, custom fields

## ✅ **Status**

**Implementation**: **COMPLETE** - Ready for information-dynamics oracle integration  
**Testing**: **READY** - Comprehensive test suite available
**Integration**: **PENDING** - Awaits Oracle system connection
**Documentation**: **COMPLETE** - Full setup and usage guide

---

🎤🔮 **Gemini Live JSON streaming ready for information-dynamics oracle enhancement** 🔮🎤