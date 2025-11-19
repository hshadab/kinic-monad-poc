"use client";

import { AuthClient } from '@dfinity/auth-client';
import { Identity } from '@dfinity/agent';
import { Principal } from '@dfinity/principal';
import { useState, useEffect, useCallback } from 'react';

export interface AuthState {
  isAuthenticated: boolean;
  principal: Principal | null;
  principalText: string | null;
  identity: Identity | null;
  authClient: AuthClient | null;
}

export function useAuth() {
  const [authState, setAuthState] = useState<AuthState>({
    isAuthenticated: false,
    principal: null,
    principalText: null,
    identity: null,
    authClient: null,
  });

  const [isLoading, setIsLoading] = useState(true);

  // Initialize auth client on mount
  useEffect(() => {
    initAuth();
  }, []);

  const initAuth = async () => {
    try {
      const client = await AuthClient.create();
      const isAuthenticated = await client.isAuthenticated();

      if (isAuthenticated) {
        const identity = client.getIdentity();
        const principal = identity.getPrincipal();

        setAuthState({
          isAuthenticated: true,
          principal,
          principalText: principal.toText(),
          identity,
          authClient: client,
        });
      } else {
        setAuthState(prev => ({
          ...prev,
          authClient: client,
        }));
      }
    } catch (error) {
      console.error('Failed to initialize auth:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const login = useCallback(async () => {
    if (!authState.authClient) {
      console.error('Auth client not initialized');
      return;
    }

    try {
      // Determine the identity provider URL based on environment
      const isLocalhost = window.location.hostname === 'localhost' ||
                         window.location.hostname === '127.0.0.1';

      // Use Internet Identity 2.0 URL for production
      const identityProvider = isLocalhost
        ? `http://localhost:4943/?canisterId=${process.env.NEXT_PUBLIC_INTERNET_IDENTITY_CANISTER_ID || 'rdmx6-jaaaa-aaaaa-aaadq-cai'}`
        : 'https://identity.internetcomputer.org';

      await authState.authClient.login({
        identityProvider,
        maxTimeToLive: BigInt(7 * 24 * 60 * 60 * 1000 * 1000 * 1000), // 7 days in nanoseconds

        // Enable Internet Identity 2.0 features
        // This allows users to authenticate with Gmail, Apple, and other methods
        allowPinAuthentication: true,

        // Optional: Set derivation origin for consistent principal across domains
        // derivationOrigin: 'https://kinicmemory.com',

        onSuccess: async () => {
          const identity = authState.authClient!.getIdentity();
          const principal = identity.getPrincipal();

          setAuthState(prev => ({
            ...prev,
            isAuthenticated: true,
            principal,
            principalText: principal.toText(),
            identity,
          }));

          console.log('Login successful:', principal.toText());
        },
        onError: (error) => {
          console.error('Login failed:', error);
        },
      });
    } catch (error) {
      console.error('Login error:', error);
    }
  }, [authState.authClient]);

  const logout = useCallback(async () => {
    if (!authState.authClient) {
      console.error('Auth client not initialized');
      return;
    }

    try {
      await authState.authClient.logout();

      setAuthState(prev => ({
        ...prev,
        isAuthenticated: false,
        principal: null,
        principalText: null,
        identity: null,
      }));

      console.log('Logout successful');
    } catch (error) {
      console.error('Logout error:', error);
    }
  }, [authState.authClient]);

  return {
    ...authState,
    isLoading,
    login,
    logout,
  };
}
