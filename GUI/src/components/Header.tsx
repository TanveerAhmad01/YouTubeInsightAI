import React from 'react';
import { Youtube } from 'lucide-react';

const Header: React.FC = () => {
  return (
    <header className="bg-white shadow-sm py-4 px-6">
      <div className="max-w-7xl mx-auto flex justify-between items-center">
        <div className="flex items-center space-x-2">
          <Youtube className="text-blue-900" size={24} />
          <span className="font-bold text-xl text-blue-900">YTinsights</span>
        </div>
      </div>
    </header>
  );
};

export default Header;