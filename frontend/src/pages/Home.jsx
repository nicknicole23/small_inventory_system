import { useState, useEffect } from 'react'
import { apiClient } from '../services/api'
import { DollarSign, Package, ShoppingBag, Activity } from 'lucide-react'
import StatCard from '../components/dashboard/StatCard'
import SalesChart from '../components/dashboard/SalesChart'
import RecentActivity from '../components/dashboard/RecentActivity'

function Home() {
  const [stats, setStats] = useState({
    active_products: 0,
    low_stock: 0,
    total_products: 0
  });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await apiClient.get('/inventory/stats');
        setStats(response.data);
      } catch (error) {
        console.error('Error fetching stats:', error);
      }
    };
    fetchStats();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
      </div>
      
      {/* Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatCard
          title="Total Revenue"
          value="$45,231.89"
          trend="+20.1%"
          trendUp={true}
          description="from last month"
          icon={DollarSign}
        />
        <StatCard
          title="Units Sold"
          value="+2350"
          trend="+180.1%"
          trendUp={true}
          description="from last month"
          icon={ShoppingBag}
        />
        <StatCard
          title="Active Products"
          value={stats.active_products.toString()}
          trend="+19%"
          trendUp={true}
          description="from last month"
          icon={Package}
        />
        <StatCard
          title="Low Stock Items"
          value={stats.low_stock.toString()}
          trend="-4"
          trendUp={false}
          description="since last hour"
          icon={Activity}
        />
      </div>

      {/* Charts & Activity Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        <SalesChart />
        <RecentActivity />
      </div>
    </div>
  )
}

export default Home
