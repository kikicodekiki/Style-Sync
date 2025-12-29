import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { wardrobeAPI } from '../services/api';

export const useWardrobe = (userId) => {
  const queryClient = useQueryClient();

  const wardrobeQuery = useQuery({
    queryKey: ['wardrobe', userId],
    queryFn: () => wardrobeAPI.getWardrobe(userId),
    enabled: !!userId,
  });

  const addItemMutation = useMutation({
    mutationFn: ({ userId, formData }) => wardrobeAPI.addItem(userId, formData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['wardrobe', userId] });
    },
  });

  const deleteItemMutation = useMutation({
    mutationFn: ({ userId, itemId }) => wardrobeAPI.deleteItem(userId, itemId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['wardrobe', userId] });
    },
  });

  return {
    wardrobe: wardrobeQuery.data || [],
    isLoading: wardrobeQuery.isLoading,
    error: wardrobeQuery.error,
    addItem: addItemMutation.mutate,
    deleteItem: deleteItemMutation.mutate,
    isAdding: addItemMutation.isPending,
    isDeleting: deleteItemMutation.isPending,
  };
};
