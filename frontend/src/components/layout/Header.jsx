import React from 'react';
import { Search, Bell, Sun, Menu } from 'lucide-react';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';

const Header = () => {
  return (
    <header className="flex h-16 items-center justify-between border-b border-gray-200 bg-white px-6">
      <div className="flex items-center gap-4 md:hidden">
        <Button variant="ghost" size="icon" className="md:hidden">
          <Menu className="h-5 w-5" />
        </Button>
        <span className="font-bold text-lg">ShopSync</span>
      </div>
      
      <div className="hidden md:flex md:flex-1 md:items-center md:gap-4">
        <div className="relative w-full max-w-md">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-gray-500" />
          <Input
            type="search"
            placeholder="Search inventory..."
            className="w-full bg-gray-50 pl-9 md:w-[300px] lg:w-[400px]"
          />
        </div>
      </div>

      <div className="flex items-center gap-2">
        <Button variant="ghost" size="icon" className="text-gray-500">
          <Sun className="h-5 w-5" />
        </Button>
        <Button variant="ghost" size="icon" className="text-gray-500 relative">
          <Bell className="h-5 w-5" />
          <span className="absolute top-2 right-2 h-2 w-2 rounded-full bg-red-600 ring-2 ring-white" />
        </Button>
      </div>
    </header>
  );
};

export default Header;
