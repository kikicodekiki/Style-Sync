import { Cloud, CloudRain, Sun, CloudSun, Thermometer, Droplets, Wind } from 'lucide-react';

const WeatherWidget = ({ weather, isLoading }) => {
  if (isLoading) {
    return (
      <div className="card animate-pulse">
        <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
        <div className="h-16 bg-gray-200 rounded"></div>
      </div>
    );
  }

  if (!weather) {
    return (
      <div className="card">
        <p className="text-gray-600">Weather data unavailable</p>
      </div>
    );
  }

  const getWeatherIcon = (condition, temperature) => {
    const temp = temperature || 0;
    if (condition?.toLowerCase().includes('rain')) {
      return <CloudRain className="text-blue-500" size={48} />;
    } else if (condition?.toLowerCase().includes('cloud')) {
      return <Cloud className="text-gray-500" size={48} />;
    } else if (temp > 20) {
      return <Sun className="text-yellow-500" size={48} />;
    } else {
      return <CloudSun className="text-gray-400" size={48} />;
    }
  };

  const temp = weather.temperature || weather.temp || 0;
  const condition = weather.condition || weather.weather || 'Unknown';
  const humidity = weather.humidity || 0;
  const windSpeed = weather.wind_speed || weather.windSpeed || 0;

  return (
    <div className="card bg-gradient-to-br from-blue-50 to-indigo-50 border-blue-200">
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-sm font-medium text-gray-600 mb-1">Current Weather</h3>
          <p className="text-xs text-gray-500">
            {weather.location || weather.city || 'Your Location'}
          </p>
        </div>
        {getWeatherIcon(condition, temp)}
      </div>

      <div className="space-y-3">
        <div className="flex items-center space-x-3">
          <div className="bg-white rounded-lg p-2">
            <Thermometer className="text-red-500" size={20} />
          </div>
          <div>
            <p className="text-2xl font-bold text-charcoal">{Math.round(temp)}°C</p>
            <p className="text-sm text-gray-600">{condition}</p>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-3 pt-3 border-t border-blue-200">
          <div className="flex items-center space-x-2">
            <Droplets className="text-blue-500" size={18} />
            <div>
              <p className="text-xs text-gray-600">Humidity</p>
              <p className="text-sm font-medium text-charcoal">{humidity}%</p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <Wind className="text-gray-500" size={18} />
            <div>
              <p className="text-xs text-gray-600">Wind</p>
              <p className="text-sm font-medium text-charcoal">{windSpeed} km/h</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WeatherWidget;
