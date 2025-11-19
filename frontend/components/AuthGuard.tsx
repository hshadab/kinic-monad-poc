"use client";

import { useAuth } from '@/lib/useAuth';
import { useEffect } from 'react';

interface AuthGuardProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

/**
 * AuthGuard component that requires Internet Identity login
 *
 * Usage:
 * <AuthGuard>
 *   <ProtectedContent />
 * </AuthGuard>
 */
export function AuthGuard({ children, fallback }: AuthGuardProps) {
  const { isAuthenticated, isLoading, login, principalText } = useAuth();

  useEffect(() => {
    // If not authenticated and not loading, show login prompt
    if (!isAuthenticated && !isLoading) {
      console.log('AuthGuard: User not authenticated');
    }
  }, [isAuthenticated, isLoading]);

  // Show loading state
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-kinic-light via-kinic-light-secondary to-kinic-light-tertiary flex items-center justify-center">
        <div className="text-center">
          <div className="w-20 h-20 border-8 border-kinic-cyan border-t-transparent rounded-full animate-spin mx-auto mb-6"></div>
          <p className="text-xl font-bold text-kinic-dark uppercase">Loading...</p>
        </div>
      </div>
    );
  }

  // Show login required screen
  if (!isAuthenticated) {
    if (fallback) {
      return <>{fallback}</>;
    }

    return (
      <div className="min-h-screen bg-gradient-to-br from-kinic-light via-kinic-light-secondary to-kinic-light-tertiary flex items-center justify-center px-4">
        <div className="max-w-2xl w-full">
          <div className="card-brutalist bg-white text-center p-8 md:p-12">
            {/* Lock Icon */}
            <div className="w-24 h-24 bg-kinic-orange border-4 border-black mx-auto mb-6 flex items-center justify-center" style={{ boxShadow: '6px 6px 0 0 #000' }}>
              <svg className="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={3}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>

            {/* Title */}
            <h1 className="text-3xl md:text-4xl font-black text-kinic-dark mb-4 uppercase tracking-tight">
              Login <span className="text-gradient">Required</span>
            </h1>

            {/* Description */}
            <p className="text-lg font-medium text-kinic-dark mb-8 leading-relaxed">
              This Kinic Memory Agent uses <strong>Internet Identity</strong> to keep your memories private and secure.
              Each user has their own isolated memory space.
            </p>

            {/* Features List */}
            <div className="text-left mb-8 space-y-3">
              <div className="flex items-start">
                <span className="text-kinic-cyan text-2xl mr-3 font-black">✓</span>
                <div>
                  <p className="font-bold text-kinic-dark">Private Memories</p>
                  <p className="text-sm text-kinic-text-secondary">Your data is isolated and only you can access it</p>
                </div>
              </div>
              <div className="flex items-start">
                <span className="text-kinic-cyan text-2xl mr-3 font-black">✓</span>
                <div>
                  <p className="font-bold text-kinic-dark">Blockchain Verified</p>
                  <p className="text-sm text-kinic-text-secondary">All operations logged on Monad with your identity</p>
                </div>
              </div>
              <div className="flex items-start">
                <span className="text-kinic-cyan text-2xl mr-3 font-black">✓</span>
                <div>
                  <p className="font-bold text-kinic-dark">Easy Login</p>
                  <p className="text-sm text-kinic-text-secondary">Use Gmail, Apple, or biometric authentication</p>
                </div>
              </div>
            </div>

            {/* Login Button */}
            <button
              onClick={login}
              className="btn-brutalist px-10 py-5 bg-kinic-orange text-white text-lg w-full sm:w-auto"
            >
              <span className="flex items-center justify-center space-x-3">
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>
                </svg>
                <span>Login with Internet Identity</span>
              </span>
            </button>

            {/* Info */}
            <p className="text-xs text-kinic-text-secondary mt-6">
              Powered by Internet Computer's decentralized identity system
            </p>
          </div>

          {/* Why Internet Identity */}
          <div className="mt-8 card-brutalist bg-kinic-cyan text-white p-6">
            <h3 className="font-black text-lg mb-3 uppercase">Why Internet Identity?</h3>
            <p className="text-sm leading-relaxed">
              Internet Identity is a blockchain authentication system that lets you log in securely without passwords.
              Your identity is cryptographic and works across all Internet Computer applications.
            </p>
          </div>
        </div>
      </div>
    );
  }

  // User is authenticated - show protected content
  return <>{children}</>;
}

export default AuthGuard;
