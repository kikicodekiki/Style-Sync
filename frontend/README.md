# StyleSync Frontend

A modern, responsive React web application for AI-powered sustainable fashion recommendations.

## Features

- 🔐 **Authentication**: Simple username/password login and signup with JWT
- 👔 **Digital Wardrobe**: Upload, view, and manage your clothing items
- 🤖 **AI Outfit Generation**: Get personalized outfit recommendations based on weather and occasion
- 🌤️ **Weather Integration**: Real-time weather data for smart outfit suggestions
- 💝 **Feedback System**: Like/dislike outfits to improve recommendations
- ⭐ **Saved Outfits**: Save your favorite outfit combinations

## Tech Stack

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **TanStack Query (React Query)** - Data fetching and state management
- **Axios** - HTTP client
- **Tailwind CSS** - Utility-first CSS framework
- **Lucide React** - Icon library

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn/pnpm

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create a `.env` file in the frontend directory:
```bash
cp .env.example .env
```

3. Update the `.env` file with your API base URL:
```
VITE_API_BASE_URL=http://localhost:8000
```

### Development

Start the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### Build

Build for production:
```bash
npm run build
```

Preview production build:
```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/      # Reusable UI components
│   │   ├── Layout.jsx
│   │   ├── WardrobeCard.jsx
│   │   ├── AddItemModal.jsx
│   │   ├── WeatherWidget.jsx
│   │   └── OutfitDisplay.jsx
│   ├── pages/           # Page components
│   │   ├── Login.jsx
│   │   ├── Dashboard.jsx
│   │   ├── Generate.jsx
│   │   └── Saved.jsx
│   ├── hooks/           # Custom React hooks
│   │   ├── useWeather.js
│   │   └── useWardrobe.js
│   ├── services/        # API service layer
│   │   └── api.js
│   ├── context/         # React Context providers
│   │   └── AuthContext.jsx
│   ├── App.jsx          # Main app component with routing
│   ├── main.jsx         # Entry point
│   └── index.css        # Global styles
├── public/              # Static assets
└── package.json
```

## API Integration

The app expects the following API endpoints:

### Authentication
- `POST /api/login` - User login
- `POST /api/signup` - User registration

### Wardrobe
- `GET /api/users/{userId}/wardrobe` - Get user's wardrobe
- `POST /api/users/{userId}/wardrobe` - Add clothing item
- `DELETE /api/users/{userId}/wardrobe/{itemId}` - Delete clothing item

### Weather
- `GET /api/weather` - Get current weather data

### Outfit Generation
- `POST /api/users/{userId}/outfit/generate` - Generate outfit recommendation
- `GET /api/users/{userId}/outfits/saved` - Get saved outfits
- `POST /api/users/{userId}/outfits/saved` - Save outfit to favorites

### Feedback
- `POST /api/users/{userId}/feedback` - Submit outfit feedback

## Design System

### Colors
- Primary: Charcoal (#2c2c2c)
- Background: Soft Grey (#f5f5f5)
- Accent: White

### Typography
- Clean, minimalist font stack
- High contrast for readability

### Components
All components follow a consistent design language with:
- Rounded corners
- Subtle shadows
- Smooth transitions
- Responsive layouts

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

MIT
