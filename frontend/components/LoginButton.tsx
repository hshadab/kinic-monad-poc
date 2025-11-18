"use client";

import { useAuth } from '../lib/useAuth';

export function LoginButton() {
  const { isAuthenticated, isLoading, principalText, login, logout } = useAuth();

  if (isLoading) {
    return (
      <div className="px-4 py-2 border-3 border-black bg-gray-200 text-gray-600 font-bold text-sm uppercase">
        Loading...
      </div>
    );
  }

  if (isAuthenticated && principalText) {
    return (
      <div className="flex items-center space-x-2">
        {/* User Principal Display */}
        <div
          className="px-3 py-2 border-3 border-black bg-kinic-cyan text-white font-bold text-xs uppercase flex items-center space-x-2"
          style={{ boxShadow: '3px 3px 0 0 #000' }}
          title={principalText}
        >
          <div className="w-2 h-2 bg-white rounded-full"></div>
          <span className="hidden sm:inline">
            {principalText.slice(0, 5)}...{principalText.slice(-3)}
          </span>
          <span className="sm:hidden">User</span>
        </div>

        {/* Logout Button */}
        <button
          onClick={logout}
          className="px-4 py-2 font-bold uppercase text-sm transition-all duration-100 border-3 border-black bg-white text-kinic-dark hover:bg-red-400 hover:text-white"
          style={{ boxShadow: '2px 2px 0 0 #000' }}
        >
          Logout
        </button>
      </div>
    );
  }

  return (
    <button
      onClick={login}
      className="px-5 py-2 font-bold uppercase text-sm transition-all duration-100 border-3 border-black bg-kinic-yellow text-kinic-dark hover:bg-kinic-orange hover:text-white"
      style={{ boxShadow: '3px 3px 0 0 #000' }}
    >
      <span className="flex items-center space-x-2">
        <svg
          className="w-4 h-4"
          fill="currentColor"
          viewBox="0 0 24 24"
        >
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>
        </svg>
        <span>Login</span>
      </span>
    </button>
  );
}
