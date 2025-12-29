import { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { outfitAPI } from '../services/api';
import { Heart, Trash2 } from 'lucide-react';

const Saved = () => {
  const { user } = useAuth();
  const [savedOutfits, setSavedOutfits] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchSavedOutfits();
  }, [user]);

  const fetchSavedOutfits = async () => {
    if (!user?.userId) return;

    setIsLoading(true);
    setError('');
    try {
      const data = await outfitAPI.getSavedOutfits(user.userId);
      setSavedOutfits(Array.isArray(data) ? data : data.outfits || []);
    } catch (err) {
      setError('Failed to load saved outfits. Please try again.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (outfitId) => {
    if (!window.confirm('Are you sure you want to remove this outfit from saved?')) {
      return;
    }

    try {
      // Remove from local state immediately for better UX
      setSavedOutfits(savedOutfits.filter((outfit) => 
        (outfit.id || outfit.outfit_id) !== outfitId
      ));
      
      // If API supports delete endpoint, uncomment this:
      // await api.delete(`/api/users/${user.userId}/outfits/saved/${outfitId}`);
    } catch (err) {
      console.error('Failed to delete outfit:', err);
      // Refresh the list if deletion failed
      fetchSavedOutfits();
      alert('Failed to remove outfit. Please try again.');
    }
  };

  if (isLoading) {
    return (
      <div>
        <h1 className="text-3xl font-bold text-charcoal mb-6">Saved Outfits</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="card animate-pulse">
              <div className="aspect-square bg-gray-200 rounded-lg mb-4"></div>
              <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
              <div className="h-4 bg-gray-200 rounded w-1/2"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold text-charcoal mb-2">Saved Outfits</h1>
          <p className="text-gray-600">
            {savedOutfits.length} {savedOutfits.length === 1 ? 'outfit' : 'outfits'} saved
          </p>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
          {error}
        </div>
      )}

      {savedOutfits.length === 0 ? (
        <div className="card text-center py-12">
          <Heart className="mx-auto text-gray-400 mb-4" size={48} />
          <p className="text-gray-600 mb-2">No saved outfits yet</p>
          <p className="text-sm text-gray-500 mb-4">
            Like an outfit to save it here for later
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {savedOutfits.map((outfit) => {
            const top = outfit.top || outfit.top_item;
            const bottom = outfit.bottom || outfit.bottom_item;
            const outfitId = outfit.id || outfit.outfit_id;

            return (
              <div key={outfitId} className="card group hover:shadow-md transition-shadow">
                <div className="grid grid-cols-2 gap-2 mb-4">
                  {/* Top */}
                  <div className="aspect-square bg-soft-grey rounded-lg overflow-hidden">
                    {top?.image_url || top?.imageUrl ? (
                      <img
                        src={top.image_url || top.imageUrl}
                        alt={top.category || 'Top'}
                        className="w-full h-full object-cover"
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center text-gray-400 text-xs">
                        Top
                      </div>
                    )}
                  </div>
                  {/* Bottom */}
                  <div className="aspect-square bg-soft-grey rounded-lg overflow-hidden">
                    {bottom?.image_url || bottom?.imageUrl ? (
                      <img
                        src={bottom.image_url || bottom.imageUrl}
                        alt={bottom.category || 'Bottom'}
                        className="w-full h-full object-cover"
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center text-gray-400 text-xs">
                        Bottom
                      </div>
                    )}
                  </div>
                </div>

                <div className="space-y-2">
                  {outfit.explanation && (
                    <p className="text-sm text-gray-600 line-clamp-2">
                      {outfit.explanation}
                    </p>
                  )}
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2 text-sm text-gray-500">
                      <Heart size={16} className="text-red-500" />
                      <span>Saved</span>
                    </div>
                    <button
                      onClick={() => handleDelete(outfitId)}
                      className="text-red-500 hover:text-red-700 opacity-0 group-hover:opacity-100 transition-opacity"
                      aria-label="Remove from saved"
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default Saved;
