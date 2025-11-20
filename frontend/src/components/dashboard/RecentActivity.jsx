import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card';
import { Package, ShoppingCart, AlertCircle } from 'lucide-react';

const activities = [
  {
    id: 1,
    type: 'sale',
    message: 'New order #1234 from Sarah M.',
    time: '5 min ago',
    icon: ShoppingCart,
    color: 'text-blue-600',
    bg: 'bg-blue-100',
  },
  {
    id: 2,
    type: 'stock',
    message: 'Restocked "Wireless Mouse" (50 units)',
    time: '2 hours ago',
    icon: Package,
    color: 'text-green-600',
    bg: 'bg-green-100',
  },
  {
    id: 3,
    type: 'alert',
    message: 'Low stock alert: "Mechanical Keyboard"',
    time: '4 hours ago',
    icon: AlertCircle,
    color: 'text-orange-600',
    bg: 'bg-orange-100',
  },
  {
    id: 4,
    type: 'sale',
    message: 'New order #1233 from Mike R.',
    time: '5 hours ago',
    icon: ShoppingCart,
    color: 'text-blue-600',
    bg: 'bg-blue-100',
  },
];

const RecentActivity = () => {
  return (
    <Card className="col-span-3">
      <CardHeader>
        <CardTitle>Recent Activity</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-8">
          {activities.map((activity) => (
            <div key={activity.id} className="flex items-center">
              <div className={`flex h-9 w-9 items-center justify-center rounded-full ${activity.bg} ${activity.color}`}>
                <activity.icon className="h-5 w-5" />
              </div>
              <div className="ml-4 space-y-1">
                <p className="text-sm font-medium leading-none">{activity.message}</p>
                <p className="text-xs text-gray-500">{activity.time}</p>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

export default RecentActivity;
