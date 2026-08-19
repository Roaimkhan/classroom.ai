import React from 'react';
import Dashboard from './screens/dashboard';

export default function App() {
  return <Dashboard />;
}

/*
import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, Button, ActivityIndicator } from 'react-native';
import { supabase } from './lib/supabase';
import GoogleSignInButton from './components/GoogleSignInButton';
import { GoogleSignin } from '@react-native-google-signin/google-signin';

export default function App() {
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // 1. Fetch current session on app startup
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      setLoading(false);
    });

    // 2. Listen for auth state changes (SIGN_IN, SIGN_OUT, TOKEN_REFRESHED)
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
      setLoading(false);
    });

    return () => subscription.unsubscribe();
  }, []);

  const handleSignOut = async () => {
    try {
      setLoading(true);
      // Sign out from Google Native SDK and Supabase
      await GoogleSignin.signOut();
      await supabase.auth.signOut();
    } catch (error) {
      console.error('Sign out error:', error.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.container}>
        <ActivityIndicator size="large" color="#0000ff" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {session && session.user ? (
        <View style={styles.profileContainer}>
          <Text style={styles.welcomeText}>Welcome, {session.user.email}!</Text>
          <Button title="Sign Out" onPress={handleSignOut} color="#d9534f" />
        </View>
      ) : (
        <View style={styles.loginContainer}>
          <Text style={styles.titleText}>Welcome Back</Text>
          <GoogleSignInButton />
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  profileContainer: {
    alignItems: 'center',
    gap: 15,
  },
  loginContainer: {
    alignItems: 'center',
    gap: 15,
  },
  welcomeText: {
    fontSize: 18,
    fontWeight: 'bold',
  },
  titleText: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 10,
  },
});
*/