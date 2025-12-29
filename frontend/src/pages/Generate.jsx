import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useWeather } from '../hooks/useWeather';
import { outfitAPI, feedbackAPI } from '../services/api';
import WeatherWidget from '../components/WeatherWidget';
import OutfitDisplay from '../components/OutfitDisplay';
import { Sparkles, Loader2 } from 'lucide-react';

const Generate = () => {
  const { user } = useAuth();
  const { data: weather, isLoading: weatherLoading } = useWeather();
  const [occasion, setOccasion] = useState('');
  const [generatedOutfit, setGeneratedOutfit] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState('');

  const handleGenerate = async () => {
    if (!occasion) {
      setError('Please select an occasion');
      return;
    }

    if (!weather) {
      setError('Weather data not available. Please wait...');
      return;
    }

    setError('');
    setIsGenerating(true);
    setGeneratedOutfit(null);

    try {
      const response = await outfitAPI.generateOutfit(user.userId, occasion, weather);
      setGeneratedOutfit(response);
    } catch (err) {
      setError(
        err.response?.data?.message || 'Failed to generate outfit. Please try again.'
      );
    } finally {
      setIsGenerating(false);
    }
  };

  const handleFeedback = async (feedbackType) => {
    if (!generatedOutfit?.id && !generatedOutfit?.outfit_id) {
      console.error('No outfit ID available for feedback');
      return;
    }

    try {
      const outfitId = generatedOutfit.id || generatedOutfit.outfit_id;
      await feedbackAPI.submitFeedback(user.userId, outfitId, feedbackType);
      // Show success message
      console.log('Feedback submitted successfully');
    } catch (err) {
      console.error('Failed to submit feedback:', err);
      // Optionally show error to user
    }
  };

  const handleSave = async () => {
    if (!generatedOutfit?.id && !generatedOutfit?.outfit_id) {
      console.error('No outfit ID available to save');
      return;
    }

    try {
      const outfitId = generatedOutfit.id || generatedOutfit.outfit_id;
      await outfitAPI.saveOutfit(user.userId, outfitId);
      alert('Outfit saved to favorites!');
    } catch (err) {
      console.error('Failed to save outfit:', err);
      alert('Failed to save outfit. Please try again.');
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-charcoal mb-2">Outfit Generator</h1>
        <p className="text-gray-600">
          Get AI-powered outfit recommendations based on weather and occasion
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - Weather & Controls */}
        <div className="lg:col-span-1 space-y-6">
          <WeatherWidget weather={weather} isLoading={weatherLoading} />

          {/* Generation Controls */}
          <div className="card">
            <h2 className="text-lg font-semibold text-charcoal mb-4">
              Generate Outfit
            </h2>

            <div className="space-y-4">
              <div>
                <label
                  htmlFor="occasion"
                  className="block text-sm font-medium text-charcoal mb-2"
                >
                  Occasion
                </label>
                <select
                  id="occasion"
                  value={occasion}
                  onChange={(e) => setOccasion(e.target.value)}
                  className="input-field"
                  disabled={isGenerating}
                >
                  <option value="">Select an occasion</option>
                  <option value="gym">Gym</option>
                  <option value="friends">Friends</option>
                  <option value="formal">Formal</option>
                  <option value="casual">Casual</option>
                  <option value="work">Work</option>
                </select>
              </div>

              {error && (
                <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
                  {error}
                </div>
              )}

              <button
                onClick={handleGenerate}
                disabled={isGenerating || !occasion || weatherLoading}
                className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
              >
                {isGenerating ? (
                  <>
                    <Loader2 className="animate-spin" size={20} />
                    <span>Generating...</span>
                  </>
                ) : (
                  <>
                    <Sparkles size={20} />
                    <span>Generate Outfit</span>
                  </>
                )}
              </button>
            </div>

            {isGenerating && (
              <div className="mt-4 bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div className="flex items-center space-x-3">
                  <Loader2 className="animate-spin text-blue-600" size={20} />
                  <div>
                    <p className="text-sm font-medium text-blue-900">
                      AI is creating your perfect outfit...
                    </p>
                    <p className="text-xs text-blue-700 mt-1">
                      Analyzing weather, occasion, and your style preferences
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Right Column - Outfit Display */}
        <div className="lg:col-span-2">
          {generatedOutfit ? (
            <OutfitDisplay
              outfit={generatedOutfit}
              onFeedback={handleFeedback}
              onSave={handleSave}
            />
          ) : (
            <div className="card text-center py-12">
              <Sparkles className="mx-auto text-gray-400 mb-4" size={48} />
              <p className="text-gray-600 mb-2">Ready to generate your outfit?</p>
              <p className="text-sm text-gray-500">
                Select an occasion and click "Generate Outfit" to get started
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Generate;
