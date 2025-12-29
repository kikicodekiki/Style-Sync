import { useState } from 'react';
import { MessageSquare, Heart, ThumbsUp, ThumbsDown } from 'lucide-react';

const OutfitDisplay = ({ outfit, onFeedback, onSave }) => {
  const [feedbackGiven, setFeedbackGiven] = useState(false);
  const [saving, setSaving] = useState(false);

  if (!outfit) {
    return (
      <div className="card text-center py-12">
        <p className="text-gray-600">Generate an outfit to see recommendations</p>
      </div>
    );
  }

  const handleFeedback = async (type) => {
    if (feedbackGiven) return;
    
    setFeedbackGiven(true);
    await onFeedback(type);
    
    if (type === 'liked' && onSave) {
      // Show save prompt after a brief delay
      setTimeout(() => {
        const shouldSave = window.confirm('Would you like to save this outfit to your favorites?');
        if (shouldSave) {
          handleSave();
        }
      }, 500);
    }
  };

  const handleSave = async () => {
    if (saving) return;
    setSaving(true);
    await onSave();
    setSaving(false);
  };

  const top = outfit.top || outfit.top_item;
  const bottom = outfit.bottom || outfit.bottom_item;

  return (
    <div className="space-y-6">
      {/* Outfit Images */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Top */}
        <div className="card">
          <h3 className="text-lg font-semibold text-charcoal mb-4">Top</h3>
          <div className="aspect-square bg-soft-grey rounded-lg overflow-hidden mb-4">
            {top?.image_url || top?.imageUrl ? (
              <img
                src={top.image_url || top.imageUrl}
                alt={top.category || 'Top'}
                className="w-full h-full object-cover"
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center text-gray-400">
                No image available
              </div>
            )}
          </div>
          <div className="space-y-1">
            <p className="font-medium text-charcoal">{top?.category || 'Unknown'}</p>
            {top?.style && <p className="text-sm text-gray-600">Style: {top.style}</p>}
          </div>
        </div>

        {/* Bottom */}
        <div className="card">
          <h3 className="text-lg font-semibold text-charcoal mb-4">Bottom</h3>
          <div className="aspect-square bg-soft-grey rounded-lg overflow-hidden mb-4">
            {bottom?.image_url || bottom?.imageUrl ? (
              <img
                src={bottom.image_url || bottom.imageUrl}
                alt={bottom.category || 'Bottom'}
                className="w-full h-full object-cover"
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center text-gray-400">
                No image available
              </div>
            )}
          </div>
          <div className="space-y-1">
            <p className="font-medium text-charcoal">{bottom?.category || 'Unknown'}</p>
            {bottom?.style && <p className="text-sm text-gray-600">Style: {bottom.style}</p>}
          </div>
        </div>
      </div>

      {/* AI Explanation */}
      {outfit.explanation && (
        <div className="card bg-blue-50 border-blue-200">
          <div className="flex items-start space-x-3">
            <MessageSquare className="text-blue-600 mt-1" size={20} />
            <div className="flex-1">
              <h4 className="font-semibold text-blue-900 mb-2">AI Recommendation</h4>
              <p className="text-blue-800 text-sm leading-relaxed">
                {outfit.explanation}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Feedback Buttons */}
      <div className="card">
        <div className="flex items-center justify-between">
          <div>
            <h4 className="font-semibold text-charcoal mb-1">How do you like this outfit?</h4>
            <p className="text-sm text-gray-600">
              Your feedback helps improve recommendations
            </p>
          </div>
          <div className="flex items-center space-x-3">
            <button
              onClick={() => handleFeedback('liked')}
              disabled={feedbackGiven}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all ${
                feedbackGiven
                  ? 'bg-green-100 text-green-700 cursor-not-allowed'
                  : 'bg-green-50 text-green-700 hover:bg-green-100'
              }`}
            >
              <ThumbsUp size={20} />
              <span>Like</span>
            </button>
            <button
              onClick={() => handleFeedback('disliked')}
              disabled={feedbackGiven}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all ${
                feedbackGiven
                  ? 'bg-red-100 text-red-700 cursor-not-allowed'
                  : 'bg-red-50 text-red-700 hover:bg-red-100'
              }`}
            >
              <ThumbsDown size={20} />
              <span>Dislike</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OutfitDisplay;
