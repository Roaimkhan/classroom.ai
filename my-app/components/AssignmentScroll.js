import React from 'react';
import { 
  StyleSheet, 
  Text, 
  View, 
  ScrollView, 
  ActivityIndicator,
  RefreshControl,
} from 'react-native';
import AssignmentCard from './assignmentcards';
import Skeleton from './Skeleton';

export default function AssignmentScroll({ 
  assignments, 
  loading, 
  onRefresh,
  onSelectAssignment,
}) {
  return (
    <View style={styles.container}>
      {/* Metric Card */}
      <View style={styles.metricCard}>
        <View style={styles.PendinAssgnBanner}>
          {loading ? (
            <ActivityIndicator size="large" color="#ffffff" />
          ) : (
            <Text style={styles.metricValue} adjustsFontSizeToFit numberOfLines={1}>
              {assignments.length}
            </Text>
          )}
        </View>

        <View style={styles.metricTextContainer}>
          <Text style={styles.metricLabel}>Pending</Text>
          <Text style={styles.metricSubLabel}>Assignments</Text>
          <Text style={styles.tapPrompt}>Pull down to refresh</Text>
        </View>
      </View>

      {/* Section Title */}
      <Text style={styles.sectionTitle}>Recent Assignments</Text>

      {/* Assignments List */}
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
        refreshControl={
          <RefreshControl
            refreshing={loading}
            onRefresh={onRefresh}
            tintColor="#FFFFFF"
            colors={["#FFFFFF"]}
            progressBackgroundColor="#212121"
          />
        }
      >
        <View style={styles.horizontalScrollContent}>
          {loading ? (
            Array.from({ length: 3 }, (_, index) => (
              <View key={`assignment-skeleton-${index}`} style={styles.assignmentSkeletonCard}>
                <Skeleton style={styles.assignmentSkeletonStripe} />
                <View style={styles.assignmentSkeletonContent}>
                  <View style={styles.assignmentSkeletonTopRow}>
                    <Skeleton style={styles.assignmentSkeletonSubject} />
                    <Skeleton style={styles.assignmentSkeletonDate} />
                  </View>
                  <Skeleton style={styles.assignmentSkeletonTitle} />
                  <Skeleton style={styles.assignmentSkeletonDescription} />
                  <Skeleton style={styles.assignmentSkeletonButton} />
                </View>
              </View>
            ))
          ) : assignments.length === 0 ? (
            <View style={styles.emptyCard}>
              <Text style={styles.emptyText}>No assignments found. Pull down to refresh.</Text>
            </View>
          ) : (
            assignments.map((item, index) => (
              <View key={item.id || index} style={styles.cardWrapper}>
                <AssignmentCard 
                  course={item.coursename || "Unknown Course"}
                  title={item.title || "Untitled Assignment"}
                  dueDate={item.dueDate ?? "No due date"}
                  description={item.description || "No description provided."}
                  status={item.due_date_status || "Normal"}
                  onPressAssignment={() => onSelectAssignment?.(item)}
                />
              </View>
            ))
          )}
        </View>
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
    borderWidth: 1, 
    borderColor:'#363636', 
    borderStyle: 'solid',
  },
  PendinAssgnBanner: {
    backgroundColor: '#b3b3b3',
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
    color: '#000000',
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
    // Lets the final card scroll completely above the fixed footer.
    paddingBottom: 180,
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
  assignmentSkeletonCard: {
    height: 158,
    width: '97%',
    alignSelf: 'center',
    marginVertical: 8,
    flexDirection: 'row',
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: '#363636',
    borderRadius: 16,
    backgroundColor: '#020202',
  },
  assignmentSkeletonStripe: {
    width: 50,
    height: '100%',
    borderRadius: 0,
  },
  assignmentSkeletonContent: {
    flex: 1,
    padding: 16,
  },
  assignmentSkeletonTopRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 12,
  },
  assignmentSkeletonSubject: {
    width: '38%',
    height: 13,
  },
  assignmentSkeletonDate: {
    width: '28%',
    height: 13,
  },
  assignmentSkeletonTitle: {
    width: '64%',
    height: 18,
    marginBottom: 9,
  },
  assignmentSkeletonDescription: {
    width: '84%',
    height: 13,
    marginBottom: 18,
  },
  assignmentSkeletonButton: {
    width: 128,
    height: 32,
    borderRadius: 20,
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
