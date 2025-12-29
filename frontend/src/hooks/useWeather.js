import { useQuery } from '@tanstack/react-query';
import { weatherAPI } from '../services/api';

export const useWeather = () => {
  return useQuery({
    queryKey: ['weather'],
    queryFn: () => weatherAPI.getWeather(),
    refetchInterval: 300000, // Refetch every 5 minutes
    staleTime: 300000, // Consider data stale after 5 minutes
  });
};
