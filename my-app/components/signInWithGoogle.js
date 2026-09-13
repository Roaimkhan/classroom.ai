import React from 'react';
import { Pressable, Text } from 'react-native';
import { GoogleSignin } from '@react-native-google-signin/google-signin';
import { supabase } from '../supabaseClient'; 

const edgefunctionUrl = process.env.EXPO_PUBLIC_EDGE_FUNCTION_URL; 
// 1) The authentication and token-handing flow
export async function signInWithGoogle() {
  await GoogleSignin.hasPlayServices({ showPlayServicesUpdateDialog: true });

  const response = await GoogleSignin.signIn();
  
  // Newer SDK versions nest fields under `.data`
  const idToken = response.data?.idToken ?? response.idToken;
  const serverAuthCode = response.data?.serverAuthCode ?? response.serverAuthCode;

  if (!idToken) throw new Error('No ID token returned from Google');

  // 1) Log the user into Supabase (authentication half)
  const { data: authData, error: authError } = await supabase.auth.signInWithIdToken({
    provider: 'google',
    token: idToken,
  });
  if (authError) throw authError;

  // 2) Hand off the serverAuthCode to your Edge Function for secure exchange + storage
  if (serverAuthCode) {
    const { data: sessionData } = await supabase.auth.getSession();
    
    // Make sure to replace with your actual Supabase Project Reference URL
    const response = await fetch(edgefunctionUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${sessionData.session?.access_token}`,
      },
      body: JSON.stringify({ serverAuthCode }),
    });

    if (!response.ok) {
      const errText = await response.text();
      console.error('Failed to store Google credentials on server:', errText);
    }
  }

  return authData.session;
}

// 2) The UI Component
export function GoogleSignInButton() {
  return (
    <Pressable 
      onPress={() => signInWithGoogle().catch((err) => console.error('Google Sign-In Error:', err))}
      style={{ padding: 12, backgroundColor: '#4285F4', borderRadius: 8, alignItems: 'center' }}
    >
      <Text style={{ color: '#fff', fontWeight: 'bold' }}>Sign in with Google</Text>
    </Pressable>
  );
}