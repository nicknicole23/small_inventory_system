import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card';
import { cn } from '../../lib/utils';

const StatCard = ({ title, value, trend, trendUp, icon: Icon, description }) => {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium text-gray-500">
          {title}
        </CardTitle>
        {Icon && <Icon className="h-4 w-4 text-gray-500" />}
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        <p className="text-xs text-gray-500 mt-1">
          <span className={cn("font-medium", trendUp ? "text-green-600" : "text-red-600")}>
            {trend}
          </span>{' '}
          {description}
        </p>
      </CardContent>
    </Card>
  );
};

export default StatCard;
