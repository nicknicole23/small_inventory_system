import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card';
import { Package, ShoppingCart, AlertCircle } from 'lucide-react';
import { productService } from '../../services/api';

const RecentActivity = () => {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchRecentActivity();
  }, []);

  const fetchRecentActivity = async () => {
    try {
      setLoading(true);
      const data = await productService.getRecentActivity();
      
      // Transform the data to include icon and styling info
      const transformedData = data.map(activity => {
        let icon, color, bg;
        
        switch (activity.type) {
          case 'sale':
            icon = ShoppingCart;
            color = 'text-blue-600';
            bg = 'bg-blue-100';
            break;
          case 'stock':
            icon = Package;
            color = 'text-green-600';
            bg = 'bg-green-100';
            break;
          case 'alert':
            icon = AlertCircle;
            color = 'text-orange-600';
            bg = 'bg-orange-100';
            break;
          default:
            icon = Package;
            color = 'text-gray-600';
            bg = 'bg-gray-100';
        }
        
        return {
          ...activity,
          icon,
          color,
          bg,
          formattedTime: formatTimeAgo(activity.time)
        };
      });
      
      setActivities(transformedData);
      setError(null);
    } catch (err) {
      console.error('Error fetching recent activity:', err);
      setError('Failed to load recent activity');
    } finally {
      setLoading(false);
    }
  };

  const formatTimeAgo = (timestamp) => {
    const now = new Date();
    const time = new Date(timestamp);
    const diffInSeconds = Math.floor((now - time) / 1000);
    
    if (diffInSeconds < 60) return 'Just now';
    if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} min ago`;
    if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} hours ago`;
    if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)} days ago`;
    return time.toLocaleDateString();
  };

  return (
    <Card className="col-span-3">
      <CardHeader>
        <CardTitle>Recent Activity</CardTitle>
      </CardHeader>
      <CardContent>
        {loading ? (
          <div className="flex justify-center items-center py-8">
            <div className="text-gray-500">Loading...</div>
          </div>
        ) : error ? (
          <div className="flex justify-center items-center py-8">
            <div className="text-red-500">{error}</div>
          </div>
        ) : activities.length === 0 ? (
          <div className="flex justify-center items-center py-8">
            <div className="text-gray-500">No recent activity</div>
          </div>
        ) : (
          <div className="space-y-8">
            {activities.map((activity) => (
              <div key={activity.id} className="flex items-center">
                <div className={`flex h-9 w-9 items-center justify-center rounded-full ${activity.bg} ${activity.color}`}>
                  <activity.icon className="h-5 w-5" />
                </div>
                <div className="ml-4 space-y-1">
                  <p className="text-sm font-medium leading-none">{activity.message}</p>
                  <p className="text-xs text-gray-500">{activity.formattedTime}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default RecentActivity;
