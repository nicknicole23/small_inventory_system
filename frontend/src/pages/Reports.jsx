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
    totalProductsSold: 0,
    revenueTrend: null,
    salesTrend: null,
    avgOrderTrend: null,
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
      let sales = salesResponse.data;
      
      // If no sales data exists, generate sample data
      if (sales.length === 0) {
        try {
          await apiClient.post('/sales/generate-sample-data');
          // Fetch again after generating
          const newSalesResponse = await apiClient.get('/sales/');
          sales = newSalesResponse.data;
        } catch (genError) {
          console.error('Failed to generate sample data:', genError);
        }
      }
      
      setSalesData(sales);

      // Calculate date ranges based on selected period
      const now = new Date();
      let currentPeriodStart, previousPeriodStart, previousPeriodEnd;
      
      if (dateRange === 'week') {
        currentPeriodStart = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
        previousPeriodStart = new Date(now.getTime() - 14 * 24 * 60 * 60 * 1000);
        previousPeriodEnd = currentPeriodStart;
      } else if (dateRange === 'month') {
        currentPeriodStart = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
        previousPeriodStart = new Date(now.getTime() - 60 * 24 * 60 * 60 * 1000);
        previousPeriodEnd = currentPeriodStart;
      } else {
        currentPeriodStart = new Date(now.getTime() - 365 * 24 * 60 * 60 * 1000);
        previousPeriodStart = new Date(now.getTime() - 730 * 24 * 60 * 60 * 1000);
        previousPeriodEnd = currentPeriodStart;
      }

      // Filter sales for current and previous periods
      const currentSales = sales.filter(sale => {
        const saleDate = new Date(sale.created_at);
        return saleDate >= currentPeriodStart && saleDate <= now;
      });

      const previousSales = sales.filter(sale => {
        const saleDate = new Date(sale.created_at);
        return saleDate >= previousPeriodStart && saleDate < previousPeriodEnd;
      });

      // Calculate current period statistics
      const totalRevenue = currentSales.reduce((sum, sale) => sum + parseFloat(sale.total_amount || 0), 0);
      const totalSales = currentSales.length;
      const averageOrderValue = totalSales > 0 ? totalRevenue / totalSales : 0;
      
      // Calculate previous period statistics
      const prevRevenue = previousSales.reduce((sum, sale) => sum + parseFloat(sale.total_amount || 0), 0);
      const prevSales = previousSales.length;
      const prevAvgOrder = prevSales > 0 ? prevRevenue / prevSales : 0;

      // Calculate trends (percentage change)
      const calculateTrend = (current, previous) => {
        if (previous === 0) return current > 0 ? 100 : 0;
        return ((current - previous) / previous) * 100;
      };

      const revenueTrend = calculateTrend(totalRevenue, prevRevenue);
      const salesTrend = calculateTrend(totalSales, prevSales);
      const avgOrderTrend = calculateTrend(averageOrderValue, prevAvgOrder);
      
      // Calculate total products sold from current period sales
      let totalProductsSold = 0;
      currentSales.forEach(sale => {
        if (sale.items && Array.isArray(sale.items)) {
          totalProductsSold += sale.items.reduce((sum, item) => sum + (item.quantity || 0), 0);
        }
      });

      setStats({
        totalRevenue,
        totalSales,
        averageOrderValue,
        totalProductsSold,
        revenueTrend,
        salesTrend,
        avgOrderTrend,
        topProducts: []
      });
    } catch (error) {
      console.error('Failed to fetch reports data:', error);
    } finally {
      setLoading(false);
    }
  };

  const StatCard = ({ icon: Icon, title, value, trend, color }) => (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">{title}</p>
          <h3 className="text-2xl font-bold text-gray-900 dark:text-white">{value}</h3>
          {trend !== null && trend !== undefined && (
            <p className={`text-sm mt-1 ${trend > 0 ? 'text-green-600 dark:text-green-400' : trend < 0 ? 'text-red-600 dark:text-red-400' : 'text-gray-600 dark:text-gray-400'}`}>
              <TrendingUp className={`inline w-4 h-4 mr-1 ${trend < 0 ? 'rotate-180' : ''}`} />
              {Math.abs(trend).toFixed(1)}% from last period
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
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Reports & Analytics</h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">Track your business performance and insights</p>
        </div>
        
        {/* Date Range Filter */}
        <div className="flex items-center space-x-2 bg-white dark:bg-gray-800 rounded-lg shadow px-4 py-2">
          <Calendar className="w-5 h-5 text-gray-500 dark:text-gray-400" />
          <select
            value={dateRange}
            onChange={(e) => setDateRange(e.target.value)}
            className="border-none focus:ring-0 text-sm font-medium text-gray-700 dark:text-gray-300 dark:bg-gray-800"
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
          trend={stats.revenueTrend}
          color="bg-green-500"
        />
        <StatCard
          icon={BarChart3}
          title="Total Sales"
          value={stats.totalSales}
          trend={stats.salesTrend}
          color="bg-blue-500"
        />
        <StatCard
          icon={TrendingUp}
          title="Average Order Value"
          value={`$${stats.averageOrderValue.toFixed(2)}`}
          trend={stats.avgOrderTrend}
          color="bg-purple-500"
        />
        <StatCard
          icon={Package}
          title="Products Sold"
          value={stats.totalProductsSold}
          color="bg-orange-500"
        />
      </div>

      {/* Recent Sales */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
        <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Recent Sales</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Date
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Amount
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Payment Method
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Items
                </th>
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              {salesData.length === 0 ? (
                <tr>
                  <td colSpan="4" className="px-6 py-8 text-center text-gray-500 dark:text-gray-400">
                    No sales data available
                  </td>
                </tr>
              ) : (
                salesData.slice(0, 10).map((sale) => (
                  <tr key={sale.id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-300">
                      {new Date(sale.created_at).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                      ${parseFloat(sale.total_amount).toFixed(2)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-400">
                      <span className="capitalize">{sale.payment_method}</span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-400">
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
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Sales Trend</h3>
          <div className="flex items-center justify-center h-64 bg-gray-50 dark:bg-gray-700 rounded">
            <p className="text-gray-500 dark:text-gray-400">Chart visualization coming soon</p>
          </div>
        </div>
        
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Top Categories</h3>
          <div className="flex items-center justify-center h-64 bg-gray-50 dark:bg-gray-700 rounded">
            <p className="text-gray-500 dark:text-gray-400">Chart visualization coming soon</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Reports;
