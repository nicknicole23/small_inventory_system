import { useState, useEffect } from 'react';
import { BarChart3, TrendingUp, DollarSign, Package, Calendar } from 'lucide-react';
import { apiClient } from '../services/api';

const Reports = () => {
  const [loading, setLoading] = useState(true);
  const [dateRange, setDateRange] = useState('week'); // week, month, year
  const [salesData, setSalesData] = useState([]);
  const [stats, setStats] = useState({
    totalRevenue: 0,
    totalSales: 0,
    averageOrderValue: 0,
    topProducts: []
  });

  useEffect(() => {
    fetchReportsData();
  }, [dateRange]);

  const fetchReportsData = async () => {
    try {
      setLoading(true);
      // Fetch sales data
      const salesResponse = await apiClient.get('/sales/');
      const sales = salesResponse.data;
      setSalesData(sales);

      // Calculate statistics
      const totalRevenue = sales.reduce((sum, sale) => sum + sale.total_amount, 0);
      const totalSales = sales.length;
      const averageOrderValue = totalSales > 0 ? totalRevenue / totalSales : 0;

      // Get top products (simplified - would need more detailed data in production)
      setStats({
        totalRevenue,
        totalSales,
        averageOrderValue,
        topProducts: []
      });
    } catch (error) {
      console.error('Failed to fetch reports data:', error);
    } finally {
      setLoading(false);
    }
  };

  const StatCard = ({ icon: Icon, title, value, trend, color }) => (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-600 mb-1">{title}</p>
          <h3 className="text-2xl font-bold text-gray-900">{value}</h3>
          {trend && (
            <p className={`text-sm mt-1 ${trend > 0 ? 'text-green-600' : 'text-red-600'}`}>
              <TrendingUp className="inline w-4 h-4 mr-1" />
              {Math.abs(trend)}% from last period
            </p>
          )}
        </div>
        <div className={`p-3 rounded-full ${color}`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Reports & Analytics</h1>
          <p className="text-gray-600 mt-1">Track your business performance and insights</p>
        </div>
        
        {/* Date Range Filter */}
        <div className="flex items-center space-x-2 bg-white rounded-lg shadow px-4 py-2">
          <Calendar className="w-5 h-5 text-gray-500" />
          <select
            value={dateRange}
            onChange={(e) => setDateRange(e.target.value)}
            className="border-none focus:ring-0 text-sm font-medium text-gray-700"
          >
            <option value="week">Last 7 Days</option>
            <option value="month">Last 30 Days</option>
            <option value="year">Last Year</option>
          </select>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          icon={DollarSign}
          title="Total Revenue"
          value={`$${stats.totalRevenue.toFixed(2)}`}
          trend={12.5}
          color="bg-green-500"
        />
        <StatCard
          icon={BarChart3}
          title="Total Sales"
          value={stats.totalSales}
          trend={8.3}
          color="bg-blue-500"
        />
        <StatCard
          icon={TrendingUp}
          title="Average Order Value"
          value={`$${stats.averageOrderValue.toFixed(2)}`}
          trend={-2.1}
          color="bg-purple-500"
        />
        <StatCard
          icon={Package}
          title="Products Sold"
          value="--"
          color="bg-orange-500"
        />
      </div>

      {/* Recent Sales */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Recent Sales</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Date
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Amount
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Payment Method
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Items
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {salesData.length === 0 ? (
                <tr>
                  <td colSpan="4" className="px-6 py-8 text-center text-gray-500">
                    No sales data available
                  </td>
                </tr>
              ) : (
                salesData.slice(0, 10).map((sale) => (
                  <tr key={sale.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {new Date(sale.created_at).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      ${sale.total_amount.toFixed(2)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                      <span className="capitalize">{sale.payment_method}</span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                      {sale.items?.length || 0} items
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Charts Section - Placeholder */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Sales Trend</h3>
          <div className="flex items-center justify-center h-64 bg-gray-50 rounded">
            <p className="text-gray-500">Chart visualization coming soon</p>
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Categories</h3>
          <div className="flex items-center justify-center h-64 bg-gray-50 rounded">
            <p className="text-gray-500">Chart visualization coming soon</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Reports;
