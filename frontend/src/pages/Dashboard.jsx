import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useWardrobe } from '../hooks/useWardrobe';
import WardrobeCard from '../components/WardrobeCard';
import AddItemModal from '../components/AddItemModal';
import { Plus, Filter, X } from 'lucide-react';

const Dashboard = () => {
  const { user } = useAuth();
  const { wardrobe, isLoading, addItem, deleteItem, isAdding } = useWardrobe(user?.userId);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [showFilters, setShowFilters] = useState(false);
  const [filters, setFilters] = useState({
    category: '',
    style: '',
    weather: '',
  });

  const handleAddItem = async (formData) => {
    await addItem({ userId: user.userId, formData });
    setIsModalOpen(false);
  };

  const handleDeleteItem = async (itemId) => {
    if (window.confirm('Are you sure you want to delete this item?')) {
      await deleteItem({ userId: user.userId, itemId });
    }
  };

  const filteredWardrobe = wardrobe.filter((item) => {
    if (filters.category && item.category?.toLowerCase() !== filters.category.toLowerCase()) {
      return false;
    }
    if (filters.style && item.style?.toLowerCase() !== filters.style.toLowerCase()) {
      return false;
    }
    if (filters.weather && item.weather?.toLowerCase() !== filters.weather.toLowerCase()) {
      return false;
    }
    return true;
  });

  const clearFilters = () => {
    setFilters({ category: '', style: '', weather: '' });
  };

  const activeFiltersCount = Object.values(filters).filter((v) => v).length;

  return (
    <div>
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 space-y-4 sm:space-y-0">
        <div>
          <h1 className="text-3xl font-bold text-charcoal mb-2">My Wardrobe</h1>
          <p className="text-gray-600">
            {isLoading ? 'Loading...' : `${filteredWardrobe.length} items`}
          </p>
        </div>
        <div className="flex space-x-3">
          <button
            onClick={() => setShowFilters(!showFilters)}
            className={`btn-secondary flex items-center space-x-2 ${showFilters ? 'bg-charcoal text-white' : ''}`}
          >
            <Filter size={18} />
            <span>Filter</span>
            {activeFiltersCount > 0 && (
              <span className="bg-white text-charcoal rounded-full w-5 h-5 flex items-center justify-center text-xs">
                {activeFiltersCount}
              </span>
            )}
          </button>
          <button
            onClick={() => setIsModalOpen(true)}
            className="btn-primary flex items-center space-x-2"
          >
            <Plus size={18} />
            <span className="hidden sm:inline">Add Item</span>
          </button>
        </div>
      </div>

      {/* Filters Sidebar */}
      {showFilters && (
        <div className="card mb-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-charcoal">Filters</h2>
            {activeFiltersCount > 0 && (
              <button
                onClick={clearFilters}
                className="text-sm text-charcoal hover:text-gray-600 flex items-center space-x-1"
              >
                <X size={16} />
                <span>Clear</span>
              </button>
            )}
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-charcoal mb-2">
                Category
              </label>
              <select
                value={filters.category}
                onChange={(e) => setFilters({ ...filters, category: e.target.value })}
                className="input-field"
              >
                <option value="">All Categories</option>
                <option value="shirt">Shirt</option>
                <option value="jeans">Jeans</option>
                <option value="jacket">Jacket</option>
                <option value="dress">Dress</option>
                <option value="shoes">Shoes</option>
                <option value="accessory">Accessory</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-charcoal mb-2">
                Style
              </label>
              <select
                value={filters.style}
                onChange={(e) => setFilters({ ...filters, style: e.target.value })}
                className="input-field"
              >
                <option value="">All Styles</option>
                <option value="casual">Casual</option>
                <option value="formal">Formal</option>
                <option value="sporty">Sporty</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-charcoal mb-2">
                Weather
              </label>
              <select
                value={filters.weather}
                onChange={(e) => setFilters({ ...filters, weather: e.target.value })}
                className="input-field"
              >
                <option value="">All Weather</option>
                <option value="cold">Cold</option>
                <option value="warm">Warm</option>
              </select>
            </div>
          </div>
        </div>
      )}

      {/* Wardrobe Grid */}
      {isLoading ? (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
          {[...Array(10)].map((_, i) => (
            <WardrobeCard key={i} item={{}} isLoading={true} />
          ))}
        </div>
      ) : filteredWardrobe.length === 0 ? (
        <div className="card text-center py-12">
          <p className="text-gray-600 mb-4">
            {activeFiltersCount > 0
              ? 'No items match your filters'
              : 'Your wardrobe is empty. Add your first item!'}
          </p>
          {activeFiltersCount === 0 && (
            <button onClick={() => setIsModalOpen(true)} className="btn-primary">
              Add Item
            </button>
          )}
        </div>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
          {filteredWardrobe.map((item) => (
            <WardrobeCard
              key={item.id || item._id}
              item={item}
              onDelete={handleDeleteItem}
              isLoading={false}
            />
          ))}
        </div>
      )}

      {/* Add Item Modal */}
      <AddItemModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onAdd={handleAddItem}
        isProcessing={isAdding}
      />
    </div>
  );
};

export default Dashboard;
