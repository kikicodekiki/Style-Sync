import { useState } from 'react';
import { X, Upload, Loader2 } from 'lucide-react';

const AddItemModal = ({ isOpen, onClose, onAdd, isProcessing }) => {
  const [formData, setFormData] = useState({
    category: '',
    style: '',
    weather: '',
    image: null,
  });
  const [dragActive, setDragActive] = useState(false);
  const [preview, setPreview] = useState(null);

  if (!isOpen) return null;

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      handleFile(file);
    }
  };

  const handleFileInput = (e) => {
    const file = e.target.files[0];
    if (file) {
      handleFile(file);
    }
  };

  const handleFile = (file) => {
    setFormData((prev) => ({ ...prev, image: file }));
    const reader = new FileReader();
    reader.onloadend = () => {
      setPreview(reader.result);
    };
    reader.readAsDataURL(file);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const data = new FormData();
    data.append('image', formData.image);
    data.append('category', formData.category);
    data.append('style', formData.style);
    data.append('weather', formData.weather);

    onAdd(data);
  };

  const handleClose = () => {
    if (!isProcessing) {
      setFormData({ category: '', style: '', weather: '', image: null });
      setPreview(null);
      onClose();
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-md w-full max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-xl font-bold text-charcoal">Add Clothing Item</h2>
          <button
            onClick={handleClose}
            disabled={isProcessing}
            className="text-gray-400 hover:text-charcoal transition-colors disabled:opacity-50"
          >
            <X size={24} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {/* Image Upload */}
          <div>
            <label className="block text-sm font-medium text-charcoal mb-2">
              Upload Image
            </label>
            <div
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
              className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
                dragActive
                  ? 'border-charcoal bg-soft-grey'
                  : 'border-gray-300 hover:border-gray-400'
              }`}
            >
              {preview ? (
                <div className="space-y-4">
                  <img
                    src={preview}
                    alt="Preview"
                    className="max-h-48 mx-auto rounded-lg object-cover"
                  />
                  <button
                    type="button"
                    onClick={() => {
                      setPreview(null);
                      setFormData((prev) => ({ ...prev, image: null }));
                    }}
                    className="text-sm text-red-600 hover:text-red-700"
                  >
                    Remove image
                  </button>
                </div>
              ) : (
                <>
                  <Upload className="mx-auto text-gray-400 mb-4" size={48} />
                  <p className="text-gray-600 mb-2">
                    Drag and drop an image here, or click to select
                  </p>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleFileInput}
                    className="hidden"
                    id="image-upload"
                    disabled={isProcessing}
                  />
                  <label
                    htmlFor="image-upload"
                    className="inline-block btn-secondary cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Choose File
                  </label>
                </>
              )}
            </div>
          </div>

          {/* Category */}
          <div>
            <label htmlFor="category" className="block text-sm font-medium text-charcoal mb-2">
              Category
            </label>
            <select
              id="category"
              value={formData.category}
              onChange={(e) => setFormData({ ...formData, category: e.target.value })}
              required
              className="input-field"
              disabled={isProcessing}
            >
              <option value="">Select category</option>
              <option value="shirt">Shirt</option>
              <option value="jeans">Jeans</option>
              <option value="jacket">Jacket</option>
              <option value="dress">Dress</option>
              <option value="shoes">Shoes</option>
              <option value="accessory">Accessory</option>
            </select>
          </div>

          {/* Style */}
          <div>
            <label htmlFor="style" className="block text-sm font-medium text-charcoal mb-2">
              Style
            </label>
            <select
              id="style"
              value={formData.style}
              onChange={(e) => setFormData({ ...formData, style: e.target.value })}
              required
              className="input-field"
              disabled={isProcessing}
            >
              <option value="">Select style</option>
              <option value="casual">Casual</option>
              <option value="formal">Formal</option>
              <option value="sporty">Sporty</option>
            </select>
          </div>

          {/* Weather */}
          <div>
            <label htmlFor="weather" className="block text-sm font-medium text-charcoal mb-2">
              Best for Weather
            </label>
            <select
              id="weather"
              value={formData.weather}
              onChange={(e) => setFormData({ ...formData, weather: e.target.value })}
              required
              className="input-field"
              disabled={isProcessing}
            >
              <option value="">Select weather</option>
              <option value="cold">Cold</option>
              <option value="warm">Warm</option>
            </select>
          </div>

          {/* Processing State */}
          {isProcessing && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="flex items-center space-x-3">
                <Loader2 className="animate-spin text-blue-600" size={20} />
                <div>
                  <p className="text-sm font-medium text-blue-900">Processing...</p>
                  <p className="text-xs text-blue-700">
                    AI is analyzing your clothing item. This may take a moment.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Submit Button */}
          <div className="flex space-x-3">
            <button
              type="button"
              onClick={handleClose}
              disabled={isProcessing}
              className="flex-1 btn-secondary disabled:opacity-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isProcessing || !formData.image}
              className="flex-1 btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isProcessing ? (
                <span className="flex items-center justify-center">
                  <Loader2 className="animate-spin mr-2" size={16} />
                  Processing...
                </span>
              ) : (
                'Add Item'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AddItemModal;
