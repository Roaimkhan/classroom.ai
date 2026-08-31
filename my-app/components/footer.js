import React, { useEffect } from 'react';
import { StyleSheet, TouchableOpacity, View } from 'react-native';
import { BlurView } from 'expo-blur';
import { FontAwesome6 } from '@expo/vector-icons';
import Animated, { 
  useSharedValue, 
  useAnimatedStyle, 
  withSpring 
} from 'react-native-reanimated';

export default function Footer({ activeTab, setActiveTab }) {
  // Shared value for blob offset (0 for 'courses', index offset for 'assignments')
  const translateX = useSharedValue(0);

  // Tab button width + gap (Padding: 24*2 + Icon: ~20 + safety margins ≈ 68px width per tab + 8px gap)
  const TAB_SLIDE_DISTANCE = 68; 

  useEffect(() => {
    // Trigger smooth spring animation on tab change
    translateX.value = withSpring(activeTab === 'courses' ? 0 : TAB_SLIDE_DISTANCE, {
      damping: 18,
      stiffness: 150,
      mass: 0.8,
    });
  }, [activeTab]);

  const animatedBlobStyle = useAnimatedStyle(() => ({
    transform: [{ translateX: translateX.value }],
  }));

  return (
    <BlurView 
      blurType="light"
      blurAmount={100}
      style={[styles.container, styles.glassButton]}
    >
      {/* Moving Sliding Blob Highlight */}
      <Animated.View style={[styles.blob, animatedBlobStyle]} />

      {/* Courses Tab */}
      <TouchableOpacity 
        style={styles.tab} 
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
        style={styles.tab} 
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
    zIndex: 1, // Ensures icons sit on top of the moving blob
  },
  blob: {
    position: 'absolute',
    top: 6,
    left: 6,
    right: 6,
    bottom: 6,
    width: 68, // Match exact width of tab container
    height: '100%',
    backgroundColor: 'rgba(255, 255, 255, 0.35)',
    borderRadius: 30,
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.5)',
    zIndex: 0,
  },
});