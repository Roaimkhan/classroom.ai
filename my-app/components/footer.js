import React from 'react';
import { StyleSheet, TouchableOpacity } from 'react-native';
import { BlurView } from 'expo-blur';
import { FontAwesome6 } from '@expo/vector-icons';

export default function Footer({ activeTab, setActiveTab }) {
  return (
    <BlurView 
    blurType="light"
    blurAmount={100}
    style={[styles.container,styles.glassButton]}
    >
      {/* Courses Tab */}
      <TouchableOpacity 
        style={[styles.tab, activeTab === 'courses' && styles.activeTab]} 
        onPress={() => setActiveTab('courses')}
        activeOpacity={0.8}
      >
        <FontAwesome6 
          name="book" 
          size={20} 
          color={activeTab === 'courses' ? '#FFFFFF' : 'rgba(255, 255, 255, 0.7)'} 
        />
      </TouchableOpacity>

      {/* Assignments Tab */}
      <TouchableOpacity 
        style={[styles.tab, activeTab === 'assignments' && styles.activeTab]} 
        onPress={() => setActiveTab('assignments')}
        activeOpacity={0.8}
      >
        <FontAwesome6 
          name="clipboard-list" 
          size={20} 
          color={activeTab === 'assignments' ? '#FFFFFF' : 'rgba(255, 255, 255, 0.7)'} 
        />
      </TouchableOpacity>
    </BlurView>
  );
}

const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    bottom: 25,
    alignSelf: 'center',
    flexDirection: 'row',
    alignItems: 'center',
    padding: 6,
    gap: 8,
    
    // Glass Pill Base
    borderRadius: 40,
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.6)',

    // Soft Shadow
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.15,
    shadowRadius: 12,
    elevation: 6,
  },
  tab: {
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 30,
    justifyContent: 'center',
    alignItems: 'center',
  },
  activeTab: {
    // Frosted Pill Highlight Overlay
    backgroundColor: 'rgba(255, 255, 255, 0.3)',
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.4)',
  },
});