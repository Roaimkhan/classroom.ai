import React from 'react';
import { 
  StyleSheet, 
  Text, 
  View, 
  ScrollView, 
  TouchableOpacity, 
  ActivityIndicator 
} from 'react-native';
import { FontAwesome6 } from '@expo/vector-icons';

export default function CourseView({ 
  courses = [], 
  loading = false, 
  onRefresh = () => {} 
}) {
  return (
    <View style={styles.container}>
      {/* Metric Card */}
      <View style={styles.metricCard}>
        <TouchableOpacity 
          style={styles.courseCountBanner}
          onPress={onRefresh}
          activeOpacity={0.8}
        >
          {loading ? (
            <ActivityIndicator size="large" color="#ffffff" />
          ) : (
            <Text style={styles.metricValue} adjustsFontSizeToFit numberOfLines={1}>
              {courses.length}
            </Text>
          )}
        </TouchableOpacity>

        <View style={styles.metricTextContainer}>
          <Text style={styles.metricLabel}>Active</Text>
          <Text style={styles.metricSubLabel}>Enrolled Courses</Text>
          <Text style={styles.tapPrompt}>Tap box to sync 🔄</Text>
        </View>
      </View>

      {/* Section Title */}
      <Text style={styles.sectionTitle}>Your Courses</Text>

      {/* Courses List */}
      <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
        {courses.length === 0 && !loading ? (
          <View style={styles.emptyCard}>
            <Text style={styles.emptyText}>No courses found. Tap above to refresh!</Text>
          </View>
        ) : (
          courses.map((course, index) => (
            <TouchableOpacity 
              key={course.id || index} 
              style={styles.courseCard}
              activeOpacity={0.8}
              onPress={() => console.log('Opened Course:', course.name)}
            >
              <View style={styles.cardHeader}>
                <FontAwesome6 name="graduation-cap" size={20} color="#FFA07A" />
                <Text style={styles.courseCode}>{course.section || 'General'}</Text>
              </View>

              <Text style={styles.courseTitle} numberOfLines={1}>
                {course.name || 'Untitled Course'}
              </Text>

              <Text style={styles.instructorText} numberOfLines={1}>
                {course.instructor || 'Instructor: N/A'}
              </Text>
            </TouchableOpacity>
          ))
        )}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  metricCard: {
    flexDirection: 'row',
    justifyContent: 'flex-start',
    alignItems: 'center',
    borderRadius: 12,
    height: 200,
    padding: 10,
    marginHorizontal: 20,
    marginBottom: 24,
    backgroundColor: '#059669', // Distinct green theme for courses
  },
  courseCountBanner: {
    backgroundColor: '#10B981',
    height: '90%',
    width: '50%',
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
  },
  metricValue: {
    fontSize: 100,
    width: '100%',               
    textAlign: 'center',
    textAlignVertical: 'center', 
    includeFontPadding: false,   
    color: '#F8FAFC',
    fontWeight: 'bold',
  },
  metricTextContainer: {
    flex: 1,
    paddingLeft: 16,
    justifyContent: 'center',
  },
  metricLabel: {
    fontSize: 28,
    color: '#ffffff',
    fontWeight: 'bold',
  },
  metricSubLabel: {
    fontSize: 16,
    color: '#ffffff',
    marginBottom: 12,
  },
  tapPrompt: {
    fontSize: 12,
    color: '#ffffff',
    fontWeight: '600',
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#F8FAFC',
    paddingHorizontal: 20,
    marginBottom: 12,
  },
  scrollContent: {
    paddingHorizontal: 20,
    paddingBottom: 100, // Space for the floating bottom nav bar
  },
  courseCard: {
    backgroundColor: '#1E293B',
    borderRadius: 16,
    padding: 16,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.08)',
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  courseCode: {
    fontSize: 12,
    color: '#94A3B8',
    fontWeight: '600',
  },
  courseTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#F8FAFC',
    marginBottom: 4,
  },
  instructorText: {
    fontSize: 13,
    color: '#CBD5E1',
  },
  emptyCard: {
    width: '100%',
    height: 140,
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
    borderRadius: 16,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.1)',
    borderStyle: 'dashed',
  },
  emptyText: {
    color: '#F8FAFC',
    fontSize: 14,
  },
});