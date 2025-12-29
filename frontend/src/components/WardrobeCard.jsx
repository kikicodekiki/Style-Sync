import { Trash2 } from 'lucide-react';
import { useState } from 'react';

const WardrobeCard = ({ item, onDelete, isLoading }) => {
  const [imageError, setImageError] = useState(false);

  const getCategoryColor = (category) => {
    const colors = {
      shirt: 'bg-blue-100 text-blue-800',
      jeans: 'bg-indigo-100 text-indigo-800',
      jacket: 'bg-purple-100 text-purple-800',
      dress: 'bg-pink-100 text-pink-800',
      shoes: 'bg-amber-100 text-amber-800',
      accessory: 'bg-gray-100 text-gray-800',
    };
    return colors[category?.toLowerCase()] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="group relative card hover:shadow-md transition-shadow">
      {isLoading ? (
        <div className="animate-pulse">
          <div className="aspect-square bg-gray-200 rounded-lg mb-4"></div>
          <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
        </div>
      ) : (
        <>
          <div className="aspect-square overflow-hidden rounded-lg mb-4 bg-soft-grey relative">
            {imageError ? (
              <div className="w-full h-full flex items-center justify-center text-gray-400">
                <span>Image not available</span>
              </div>
            ) : (
              <img
                src={item.image_url || item.imageUrl || '/placeholder-clothing.jpg'}
                alt={item.category || 'Clothing item'}
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                onError={() => setImageError(true)}
              />
            )}
          </div>
          
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className={`px-2 py-1 rounded text-xs font-medium ${getCategoryColor(item.category)}`}>
                {item.category || 'Unknown'}
              </span>
              {onDelete && (
                <button
                  onClick={() => onDelete(item.id || item._id)}
                  className="text-red-500 hover:text-red-700 opacity-0 group-hover:opacity-100 transition-opacity"
                  aria-label="Delete item"
                >
                  <Trash2 size={16} />
                </button>
              )}
            </div>
            
            {item.style && (
              <p className="text-sm text-gray-600">Style: {item.style}</p>
            )}
            
            {item.weather && (
              <p className="text-xs text-gray-500">Best for: {item.weather}</p>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default WardrobeCard;
