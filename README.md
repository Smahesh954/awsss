# AI Meeting Notes Agent (Background Recorder)

> Implementation of **Project 8: AI Meeting Notes Agent (Background Recorder)** with modular **HTML**, **CSS**, **Java**, and **JavaScript** files.

---

## 📁 Project Architecture & File Breakdown

This project cleanly separates markup, styling, backend processing, and client interactivity across dedicated files:

```
ai-meeting-notes-agent/
│
├── 🌐 HTML Files (User Interface & Architecture Specs)
│   ├── index.html            # Main Live Recording Dashboard, Diarization Stream & RAG Assistant
│   ├── architecture.html     # AWS Event-Driven Architecture, CI/CD, & DLQ Specification
│   └── history.html          # Historical Meeting Archive & Indexed Knowledge Base
│
├── 🎨 CSS Files (Modular Styling & Themes)
│   ├── css/base.css          # CSS Variables, Theme, Typography, Layout Grid & Base UI
│   └── css/components.css    # Audio Visualizer, Diarization Bubbles, RAG Chat & AWS Nodes
│
├── ☕ Java Files (Zero-Dependency Backend Server & RAG Engine)
│   ├── src/MeetingNotesServer.java  # OpenJDK HTTP Server (REST API + Static File Server)
│   ├── src/MeetingService.java      # Meeting Models, Diarization Turns & Structured JSON
│   └── src/RAGEngine.java           # Chunking Algorithm (Speaker/Timestamp aware) & Vector Query
│
├── ⚡ JavaScript Files (Frontend Interactivity)
│   ├── js/app.js             # Web Audio API Visualizer, Live Ingestion & Diarization Streamer
│   ├── js/rag.js             # Interactive RAG Assistant with Speaker Citations
│   └── js/pipeline.js        # 8-Stage AWS EventBridge Pipeline Simulator & DLQ Tester
│
├── 🚀 Scripts
│   ├── run.bat               # 1-Click Windows Launcher (Compiles and runs Java Server)
│   └── README.md             # Complete Documentation
```

---

## 🎯 Key Project 8 Concepts Implemented

1. **Real-time / Streaming Audio Transcription Pipeline:**
   - Ingests audio streams with real-time waveform visualization via Web Audio API.
2. **Speaker Diarization:**
   - Color-coded speaker identification (`Alice [Cloud Architect]`, `Bob [ML Engineer]`, `Charlie [DevOps Lead]`) with confidence scores.
3. **Speaker-Attributed Timestamped Chunking for RAG:**
   - Chunks transcripts preserving dialogue context, speaker names, and timestamp boundaries (`[00:01:15]`).
4. **Structured LLM Output:**
   - Automatic generation of action items, owners, priorities, and decisions in validated JSON format.
5. **Decoupled AWS Event-Driven Architecture:**
   - Asynchronous orchestration across 8 AWS services:
     `S3` ➔ `EventBridge` ➔ `Lambda` ➔ `Amazon Transcribe` ➔ `Amazon Bedrock` ➔ `OpenSearch Serverless` ➔ `DynamoDB` ➔ `Amazon SNS/SES`.
6. **CI/CD & DLQ Testing:**
   - Dead-Letter Queue (DLQ) simulation for corrupted audio streams and shadow pipeline deployment testing.

---

## 🚀 How to Run

### Method 1: Standalone Browser Mode (Zero Setup)
Simply double-click or open `index.html` in any modern web browser (Edge, Chrome, Firefox). The client-side fallback engine handles audio visualization, speaker diarization, and RAG search directly in the browser!

### Method 2: With Java Backend Server (Port 8080)
1. Open PowerShell or Command Prompt in this folder:
   ```powershell
   cd C:\Users\mahes\.gemini\antigravity\scratch\ai-meeting-notes-agent
   ```
2. Double-click `run.bat` or run:
   ```cmd
   javac -d bin src\RAGEngine.java src\MeetingService.java src\MeetingNotesServer.java
   java -cp bin src.MeetingNotesServer
   ```
3. Open your browser and navigate to:
   ```
   http://localhost:8080
   ```
