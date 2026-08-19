import React from 'react';
import { StyleSheet, Text, View, Button } from 'react-native';
import * as WebBrowser from 'expo-web-browser';
import * as AuthSession from 'expo-auth-session';
import { supabase } from '../lib/supabase';

// Enables redirect back to the app after Google authentication
WebBrowser.maybeCompleteAuthSession();

export default function GoogleSignInButton() {
  const handleGoogleSignIn = async () => {
    try {
      // Generate the redirect URL for your Expo app
      const redirectTo = AuthSession.makeRedirectUri({
        scheme: 'your-app-scheme', // Or use standard Expo scheme
        path: 'auth',
      });

      // Request Supabase to generate the Google OAuth URL
      const { data, error } = await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: {
          redirectTo,
          skipBrowserRedirect: true,
        },
      });

      if (error) throw error;

      // Open the browser for user to pick their Google account
      const res = await WebBrowser.openAuthSessionAsync(data.url, redirectTo);

      if (res.type === 'success' && res.url) {
        // Extract tokens from the redirect URL fragment/query
        const urlParams = new URLSearchParams(res.url.split('#')[1] || res.url.split('?')[1]);
        const access_token = urlParams.get('access_token');
        const refresh_token = urlParams.get('refresh_token');

        if (access_token && refresh_token) {
          await supabase.auth.setSession({ access_token, refresh_token });
        }
      }
    } catch (err) {
      console.error('OAuth error:', err.message);
    }
  };

  return (
    <View style={styles.container}>
      <Button title="Sign in with Google (Web Flow)" onPress={handleGoogleSignIn} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { marginVertical: 10 },
});