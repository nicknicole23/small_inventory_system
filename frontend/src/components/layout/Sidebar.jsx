import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { LayoutDashboard, Package, Tags, BarChart3, Settings, LogOut, ShoppingBag } from 'lucide-react';
import { cn } from '../../lib/utils';
import { useAuth } from '../../context/AuthContext';

const Sidebar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  
  const navItems = [
    { icon: LayoutDashboard, label: 'Dashboard', path: '/' },
    { icon: Package, label: 'Inventory', path: '/inventory' },
    { icon: Tags, label: 'Categories', path: '/categories' },
    { icon: ShoppingBag, label: 'Sales', path: '/sales' },
    { icon: BarChart3, label: 'Reports', path: '/reports' },
    { icon: Settings, label: 'Settings', path: '/settings' },
  ];

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const getInitials = (firstName, lastName, email) => {
    if (firstName && lastName) {
      return `${firstName[0]}${lastName[0]}`.toUpperCase();
    }
    if (firstName) {
      return firstName.substring(0, 2).toUpperCase();
    }
    if (email) {
      return email.substring(0, 2).toUpperCase();
    }
    return 'U';
  };

  const getDisplayName = (firstName, lastName, username) => {
    if (firstName && lastName) {
      return `${firstName} ${lastName}`;
    }
    if (firstName) {
      return firstName;
    }
    return username || 'User';
  };

  return (
    <aside className="hidden w-64 flex-col border-r border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 md:flex">
      <div className="flex h-16 items-center border-b border-gray-200 dark:border-gray-700 px-6">
        <div className="flex items-center gap-2 font-bold text-xl text-gray-900 dark:text-white">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-600 text-white">
            <ShoppingBag className="h-5 w-5" />
          </div>
          ShopSync
        </div>
      </div>
      <div className="flex-1 overflow-y-auto py-4">
        <nav className="grid gap-1 px-2">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                cn(
                  "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                  isActive
                    ? "bg-blue-50 dark:bg-blue-900/50 text-blue-600 dark:text-blue-400"
                    : "text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 hover:text-gray-900 dark:hover:text-white"
                )
              }
            >
              <item.icon className="h-4 w-4" />
              {item.label}
            </NavLink>
          ))}
        </nav>
      </div>
      <div className="border-t border-gray-200 dark:border-gray-700 p-4">
        <div 
          onClick={handleLogout}
          className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer"
        >
          <div className="h-8 w-8 rounded-full bg-blue-600 flex items-center justify-center">
             <span className="text-xs font-medium text-white">
               {user && getInitials(user.first_name, user.last_name, user.email)}
             </span>
          </div>
          <div className="flex-1 overflow-hidden">
            <p className="truncate font-medium text-gray-900 dark:text-white">
              {user && getDisplayName(user.first_name, user.last_name, user.username)}
            </p>
            <p className="truncate text-xs text-gray-500 dark:text-gray-400">
              {user?.email || 'user@example.com'}
            </p>
          </div>
          <LogOut className="h-4 w-4 text-gray-500 dark:text-gray-400" />
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
