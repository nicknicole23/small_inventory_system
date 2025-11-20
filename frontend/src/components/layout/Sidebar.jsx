import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Package, Tags, BarChart3, Settings, LogOut, ShoppingBag } from 'lucide-react';
import { cn } from '../../lib/utils';

const Sidebar = () => {
  const navItems = [
    { icon: LayoutDashboard, label: 'Dashboard', path: '/' },
    { icon: Package, label: 'Inventory', path: '/inventory' },
    { icon: Tags, label: 'Categories', path: '/categories' },
    { icon: ShoppingBag, label: 'Sales', path: '/sales' },
    { icon: BarChart3, label: 'Reports', path: '/reports' },
    { icon: Settings, label: 'Settings', path: '/settings' },
  ];

  return (
    <aside className="hidden w-64 flex-col border-r border-gray-200 bg-white md:flex">
      <div className="flex h-16 items-center border-b border-gray-200 px-6">
        <div className="flex items-center gap-2 font-bold text-xl text-gray-900">
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
                    ? "bg-blue-50 text-blue-600"
                    : "text-gray-700 hover:bg-gray-100 hover:text-gray-900"
                )
              }
            >
              <item.icon className="h-4 w-4" />
              {item.label}
            </NavLink>
          ))}
        </nav>
      </div>
      <div className="border-t border-gray-200 p-4">
        <div className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 cursor-pointer">
          <div className="h-8 w-8 rounded-full bg-gray-200 flex items-center justify-center">
             <span className="text-xs font-medium">JD</span>
          </div>
          <div className="flex-1 overflow-hidden">
            <p className="truncate font-medium text-gray-900">John Doe</p>
            <p className="truncate text-xs text-gray-500">john@example.com</p>
          </div>
          <LogOut className="h-4 w-4 text-gray-500" />
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
