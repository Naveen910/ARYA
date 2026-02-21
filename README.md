# ARYA - AI ETF Trading Agent

**ARYA** is an AI-driven multi-agent system designed to provide real-time BUY/SELL/HOLD signals for Exchange-Traded Funds (ETFs). It integrates market news, sentiment analysis, technical indicators, and macroeconomic data to deliver informed trading recommendations.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Setup](#setup)
- [Usage](#usage)

---

## Overview

ARYA uses a coordinator agent to orchestrate multiple specialized agents:

- **NewsAgent:** Fetches and processes market and company news.
- **SentimentAgent:** Analyzes news and market sentiment.
- **TechnicalAgent:** Extracts and interprets technical indicators.
- **MacroAgent:** Monitors macroeconomic indicators and regimes.
- **AggregatorAgent:** Combines outputs from all agents to generate the final trading signal.

---

## Features

- Real-time ETF signal generation (BUY/SELL/HOLD)
- Multi-agent architecture for modularity and scalability
- Integration with Google Gemini LLM for advanced reasoning
- Support for custom ETFs and market data sources

---

## Architecture

```
                     ┌────────────────┐
                     │  Coordinator   │
                     │     Agent      │
                     └───────┬────────┘
                             │
             ┌───────────────┼─────────────────┐
             │               │                 │
        ┌───────────┐   ┌────────────┐   ┌────────────┐
        │   News    │   │ Sentiment  │   │ Technical  │
        │   Agent   │   │   Agent    │   │   Agent    │
        └───────────┘   └────────────┘   └────────────┘
             │               │                 │
             └───────────────┼─────────────────┘
                             │
                       ┌─────────────┐
                       │ Aggregator  │
                       │    Agent    │
                       └─────────────┘
                             │
                         BUY/SELL/HOLD

```

---

## Setup

1. Clone the repository:

```bash
git clone https://github.com/Naveen910/ARYA
cd ARYA
```

2. Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your API key:

```ini
GOOGLE_API_KEY=your_google_api_key_here
```

---

## Usage

Start ARYA via the ADK CLI:

```bash
pip install google-adk
adk run ARYA
```

Example interaction:

```
[user]: hi
[ETFCoordinator]: Hello! I am the ETF signal coordinator. I can help you by providing BUY/SELL/HOLD signals for ETFs. To do this, I need to gather some information. What ETF are you interested in, and what kind of information are you looking for? For example, are you interested in recent news, sentiment, technical indicators, or the overall macro regime?
[user]: GROWWRAIL
[ETFCoordinator]: Generating signals for GROWWRAIL...
```

---
