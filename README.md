# StyleSync - AI-Powered Sustainable Fashion Agent

StyleSync is a GenAI-powered web application that helps users manage a digital wardrobe and receive AI-generated outfit recommendations based on weather, occasion, and personal style preferences.

## Project Structure

```
Style-Sync/
├── frontend/          # React frontend application
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   ├── pages/         # Page components
│   │   ├── hooks/         # Custom React hooks
│   │   ├── services/      # API service layer
│   │   └── context/       # React Context providers
│   └── README.md       # Frontend-specific documentation
└── README.md          # This file
```

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

- React 18 with Vite
- React Router for navigation
- TanStack Query for data fetching
- Tailwind CSS for styling
- Axios for API calls
- Lucide React for icons

## Contributing

This project follows a component-based architecture. When adding new features:

1. Create components in `/components`
2. Add pages in `/pages`
3. Use custom hooks in `/hooks` for data fetching
4. Update API services in `/services/api.js`
5. Commit changes with clear messages

## License

MIT
