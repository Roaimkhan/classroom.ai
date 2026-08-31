import React, { useState, useEffect, useCallback } from 'react';
import { StyleSheet, Text, View, Alert } from 'react-native';
import AssignmentView from '../components/AssignmentScroll';
import CourseView from '../components/courseview';
import AssignmentDetailModal from '../components/AssignmentView'; // Import detail view modal

const API_TIMEOUT_MS = 10000;

export default function AgentDashboard({ activeTab }) {
  const [assignments, setAssignments] = useState([]);
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Modal State
  const [selectedAssignment, setSelectedAssignment] = useState(null);
  const [modalVisible, setModalVisible] = useState(false);

  // Handlers for opening/closing the assignment modal
  const handleOpenAssignment = useCallback((assignment) => {
    setSelectedAssignment(assignment);
    setModalVisible(true);
  }, []);

  const handleCloseAssignment = useCallback(() => {
    setModalVisible(false);
    setSelectedAssignment(null);
  }, []);

  // Sanitizers to prevent runtime type crashes
  const sanitizeAssignments = useCallback((rawData) => {
    if (!Array.isArray(rawData)) return [];
    return rawData.filter(item => item && typeof item === 'object').map(item => ({
      id: String(item.id || Math.random().toString(36).substring(7)),
      courseId: String(item.courseId || ''),
      coursename: String(item.coursename || item.courseId || 'Unknown Course'),
      title: String(item.title || 'Untitled Assignment'),
      description: String(item.description || 'No description provided.'),
      dueDate: item.dueDate ? String(item.dueDate) : null,
      due_date_status: String(item.due_date_status || 'Normal'),
      materials: Array.isArray(item.materials) ? item.materials : [],
    }));
  }, []);

  const sanitizeCourses = useCallback((rawData) => {
    if (!Array.isArray(rawData)) return [];
    return rawData.filter(item => item && typeof item === 'object').map(item => ({
      id: String(item.id || Math.random().toString(36).substring(7)),
      name: String(item.name || item.subject || 'Untitled Course'),
      section: item.section ? String(item.section) : null,
      room: item.room ? String(item.room) : null,
      subject: item.subject ? String(item.subject) : null,
      course_state: String(item.course_state || 'ACTIVE'),
    }));
  }, []);

  // Dedicated API caller (Only runs manually or once on startup)
  const fetchDashboardData = useCallback(async () => {
    setLoading(true);
    setError(null);

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), API_TIMEOUT_MS);

    try {
      const response = await fetch('http://192.168.0.71:8000/refresh', {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`Server returned status ${response.status}`);
      }

      const json = await response.json();

      if (!json || typeof json !== 'object') {
        throw new Error('Invalid JSON payload structure received.');
      }

      setAssignments(sanitizeAssignments(json.all_pending_assgn));
      setCourses(sanitizeCourses(json.registered_courses));

    } catch (err) {
      let errorMessage = 'Failed to sync classroom data.';
      
      if (err.name === 'AbortError') {
        errorMessage = 'Network request timed out.';
      } else if (err.message) {
        errorMessage = err.message;
      }

      setError(errorMessage);
      Alert.alert('Sync Error', errorMessage, [{ text: 'OK' }]);
      console.error('[Dashboard Fetch Error]:', err);
    } finally {
      clearTimeout(timeoutId);
      setLoading(false);
    }
  }, [sanitizeAssignments, sanitizeCourses]);

  // STRICTLY Initial Load: Runs 1 time when app opens
  useEffect(() => {
    fetchDashboardData();
  }, []); 

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <View>
          <Text style={styles.headerTitle}>GC Agent</Text>
          <Text style={styles.headerSubtitle}>Classroom Automation & AI</Text>
        </View>
      </View>

      {/* Switching tabs now re-uses in-memory cached state without triggering API calls */}
      {activeTab === 'assignments' ? (
        <AssignmentView 
          assignments={assignments}
          loading={loading}
          error={error}
          onRefresh={fetchDashboardData} // Manual trigger only via user tap
          onSelectAssignment={handleOpenAssignment} // Passed down to trigger modal open
        />
      ) : (
        <CourseView 
          courses={courses}
          loading={loading}
          error={error}
          onRefresh={fetchDashboardData} // Manual trigger only via user tap
        />
      )}

      {/* Dynamic Slide-Up Modal */}
      <AssignmentDetailModal 
        visible={modalVisible}
        onClose={handleCloseAssignment}
        assignment={selectedAssignment}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(255, 255, 255, 0.1)',
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#F8FAFC',
  },
  headerSubtitle: {
    fontSize: 12,
    color: '#94A3B8',
  },
});