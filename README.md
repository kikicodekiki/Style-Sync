# StyleSync - AI-Powered Sustainable Fashion Agent

StyleSync is a GenAI-powered web application that helps users manage a digital wardrobe and receive AI-generated outfit recommendations based on weather, occasion, and personal style preferences.

## Project Structure

```
Style-Sync/
├── frontend/              # React frontend application
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   ├── pages/         # Page components
│   │   ├── hooks/         # Custom React hooks
│   │   ├── services/      # API service layer
│   │   └── context/       # React Context providers
│   └── README.md          # Frontend-specific documentation
├── backend/               # Python Flask API backend
│   ├── app/
│   │   ├── agents/        # AI agents (VAA, SRA, Feedback)
│   │   ├── api/           # REST API controllers
│   │   ├── models/        # SQLAlchemy database models
│   │   └── services/      # Business logic layer
│   ├── uploads/           # Uploaded clothing images
│   ├── feedback_data/     # RL training signal JSON files
│   ├── requirements.txt
│   └── run.py
└── README.md              # This file
```

## Backend Setup

### Prerequisites

- Python 3.9+
- [Ollama](https://ollama.ai) with `llama3.2` model (for AI recommendations)
- OpenWeatherMap API key (optional, has mock fallback)

### Quick Start

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

5. Install and start Ollama with LLaMA:
```bash
# Install Ollama from https://ollama.ai
ollama pull llama3.2
ollama serve  # Runs on localhost:11434
```

6. Start the Flask server:
```bash
python run.py
```
The API will be available at `http://localhost:8000`.

### AI Agents

| Agent | Purpose | AI Model |
|-------|---------|----------|
| **Vision Analysis Agent (VAA)** | Classifies clothing images (category, color, style) | YOLOv8 + ColorThief + LLaMA |
| **Styling Recommendation Agent (SRA)** | Generates outfit recommendations | LLaMA via Ollama |
| **Feedback Agent (FA)** | Processes user feedback into RL training signals | Rule-based + JSON signals |

## Frontend Setup

See [frontend/README.md](./frontend/README.md) for detailed setup instructions.

### Quick Start

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file:
```bash
cp .env.example .env
```

4. Start development server:
```bash
npm run dev
```

## Features

- ✅ User Authentication (Login/Sign-up with JWT)
- ✅ Digital Wardrobe Management (Upload, view, filter clothing items)
- ✅ AI Outfit Generation (Weather and occasion-based recommendations)
- ✅ Weather Integration (Real-time weather data)
- ✅ Feedback System (Like/dislike outfits for learning)
- ✅ Saved Outfits (Save favorite combinations)

## API Architecture

The frontend interfaces with a 3-layer REST API architecture. Ensure your backend API is running and accessible at the configured base URL (default: `http://localhost:8000`).

## Design Philosophy

- **Minimalist & High-Fashion**: Clean, elegant UI inspired by Pinterest and Vogue
- **Neutral Palette**: Whites, soft greys, and charcoals to let clothing colors stand out
- **Responsive**: Fully responsive design for mobile, tablet, and desktop
- **User-Centric**: Intuitive navigation and smooth interactions

## Tech Stack

**Frontend:**
- React 18 with Vite
- React Router for navigation
- TanStack Query for data fetching
- Tailwind CSS for styling
- Axios for API calls
- Lucide React for icons

**Backend:**
- Python Flask with SQLAlchemy (SQLite)
- Flask-JWT-Extended for authentication
- LLaMA 3.2 via Ollama for outfit generation
- YOLOv8 (ultralytics) for clothing detection
- ColorThief for dominant color extraction
- OpenWeatherMap API for weather data

## Contributing

This project follows a component-based architecture. When adding new features:

1. Create components in `/components`
2. Add pages in `/pages`
3. Use custom hooks in `/hooks` for data fetching
4. Update API services in `/services/api.js`
5. Commit changes with clear messages

## License

MIT
