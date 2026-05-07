import React, { useState } from 'react';
import Sidebar from '../components/Sidebar';
import TopNavbar from '../components/TopNavbar';

const Layout = ({ children }) => {
  const [isSidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <Sidebar isOpen={isSidebarOpen} onClose={() => setSidebarOpen(false)} />
      
      <div className="flex flex-col flex-1 w-full min-w-0">
        <TopNavbar onMenuClick={() => setSidebarOpen(true)} />
        
        <main className="flex-1 overflow-y-auto p-4 md:p-6 lg:p-8">
          <div className="mx-auto max-w-7xl h-full">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
};

export default Layout;
