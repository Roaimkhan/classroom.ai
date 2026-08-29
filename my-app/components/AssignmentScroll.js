import React from 'react';
import { 
  StyleSheet, 
  Text, 
  View, 
  ScrollView, 
  TouchableOpacity, 
  ActivityIndicator 
} from 'react-native';
import AssignmentCard from './assignmentcards';

export default function AssignmentScroll({ 
  assignments, 
  loading, 
  onRefresh 
}) {
  return (
    <View style={styles.container}>
      {/* Metric Card */}
      <View style={styles.metricCard}>
        <TouchableOpacity 
          style={styles.PendinAssgnBanner}
          onPress={onRefresh}
          activeOpacity={0.8}
        >
          {loading ? (
            <ActivityIndicator size="large" color="#ffffff" />
          ) : (
            <Text style={styles.metricValue} adjustsFontSizeToFit numberOfLines={1}>
              {assignments.length}
            </Text>
          )}
        </TouchableOpacity>

        <View style={styles.metricTextContainer}>
          <Text style={styles.metricLabel}>Pending</Text>
          <Text style={styles.metricSubLabel}>Assignments</Text>
          <Text style={styles.tapPrompt}>Tap orange box to refresh 🔄</Text>
        </View>
      </View>

      {/* Section Title */}
      <Text style={styles.sectionTitle}>Recent Assignments</Text>

      {/* Assignments List */}
      <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
        <ScrollView contentContainerStyle={styles.horizontalScrollContent}>
          {assignments.length === 0 && !loading ? (
            <View style={styles.emptyCard}>
              <Text style={styles.emptyText}>No assignments found. Tap above to refresh!</Text>
            </View>
          ) : (
            assignments.map((item, index) => (
              <View key={item.id || index} style={styles.cardWrapper}>
                <AssignmentCard 
                  subject={item.courseId || "Unknown Course"}
                  title={item.title || "Untitled Assignment"}
                  dueDate={item.dueDate ?? "No due date"}
                  description={item.description || "No description provided."}
                  status={item.due_date_status || "Normal"}
                  onPressAssignment={() => console.log('Opened:', item.title)}
                />
              </View>
            ))
          )}
        </ScrollView>
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
    backgroundColor: '#1abcfe',
  },
  PendinAssgnBanner: {
    backgroundColor: '#a259ff',
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
    // backgroundColor: '#a259ff',
  },
  horizontalScrollContent: {
    paddingHorizontal: 20,
    justifyContent: 'center',
    // backgroundColor: '#000000',
    width: '100%',
  },
  cardWrapper: {
    width: '100%',
    marginRight: 16,
  },
  emptyCard: {
    width: '100%',
    height: 140,
    borderRadius: 16,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: 'rgba(146, 146, 146, 0.2)',
    borderStyle: 'dashed',
    alignSelf: 'center',
  },
  emptyText: {
    color: '#F8FAFC',
    fontSize: 14,
  },
});