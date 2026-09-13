import React, { useState, useEffect } from 'react';
import { StyleSheet, View, Text, ActivityIndicator } from 'react-native';
import { supabase } from './supabaseClient';
import AgentDashboard from './screens/dashboard';
import Footer from './components/footer';
import { GoogleSignInButton } from './components/signInWithGoogle';
import { GoogleSignin } from '@react-native-google-signin/google-signin';

const webclientId = process.env.EXPO_PUBLIC_GOOGLE_WEB_CLIENT_ID; 

GoogleSignin.configure({
    webClientId: webclientId,
    scopes: [
        "https://www.googleapis.com/auth/classroom.courses.readonly",
        "https://www.googleapis.com/auth/classroom.student-submissions.me.readonly",
    ],
    offlineAccess: true,
    forceCodeForRefreshToken: true,
  });
export default function App() {
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('assignments');

  useEffect(() => {
    // 1) Check initial auth session on app boot
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      setLoading(false);
    });

    // 2) Listen for real-time sign in/out state changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
    });

    return () => subscription.unsubscribe();
  }, []);

  // Show a loading spinner while checking local secure storage for an active session
  if (loading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" color="#4285F4" />
      </View>
    );
  }

  // GATEKEEPER: If no user session exists, show the Login Screen
  if (!session) {
    return (
      <View style={styles.loginContainer}>
        <Text style={styles.title}>GC Agent</Text>
        <Text style={styles.subtitle}>Sign in to manage your Google Classroom & Drive workflow</Text>
        <GoogleSignInButton />
      </View>
    );
  }

  // MAIN APP: If logged in, show your dashboard and tabs
  return (
    <View style={styles.container}>
      <AgentDashboard activeTab={activeTab} />
      <Footer activeTab={activeTab} setActiveTab={setActiveTab} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#030303',
  },
  centered: {
    flex: 1,
    backgroundColor: '#030303',
    justifyContent: 'center',
    alignItems: 'center',
  },
  loginContainer: {
    flex: 1,
    backgroundColor: '#030303',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#ffffff',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 14,
    color: '#888888',
    textAlign: 'center',
    marginBottom: 32,
  },
});