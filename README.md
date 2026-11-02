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

### Cognito sign-in setup
The UI uses the Cognito Hosted UI authorization-code flow with PKCE. Create a Cognito user pool app client configured as a public client (no client secret), enable the authorization-code grant and the `openid`, `email`, and `profile` scopes, and register the exact HTTPS callback and sign-out URL.

Set the public frontend values in `js/auth-config.js`:
```js
window.COGNITO_CONFIG = {
  domain: "https://your-domain.auth.your-region.amazoncognito.com",
  clientId: "your-public-app-client-id",
  redirectUri: "https://your-host/index.html"
};
```
Register that exact URL as the app client's allowed callback and sign-out URL. Sign-in returns to `index.html` regardless of which app page started it. Serve the app over HTTPS (localhost is supported for development); opening the HTML file directly is not supported.

Before starting the Java server, set `COGNITO_ISSUER` to `https://cognito-idp.<region>.amazonaws.com/<user-pool-id>` and `COGNITO_CLIENT_ID` to the same app client ID. In PowerShell:
```powershell
$env:COGNITO_ISSUER = "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_example"
$env:COGNITO_CLIENT_ID = "your-public-app-client-id"
```
The Java API rejects requests without a valid, unexpired Cognito access token; API routes return `503` when server-side Cognito settings are missing. Keep the app client secret out of the browser and repository.

### Method 1: Browser with Cognito
After configuring Cognito and hosting the app over HTTPS (or localhost), open the registered callback URL in a modern browser. The client-side fallback engine handles audio visualization, speaker diarization, and RAG search directly in the browser after sign-in.

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
