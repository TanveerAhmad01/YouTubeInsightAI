import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-white py-6 border-t border-slate-200">
      <div className="max-w-7xl mx-auto px-4 md:px-6">
        <div className="flex justify-center text-slate-500 text-sm">
          &copy; {new Date().getFullYear()} YTinsights. All rights reserved.
        </div>
      </div>
    </footer>
  );
};

export default Footer;