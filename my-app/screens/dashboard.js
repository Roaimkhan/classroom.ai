import React, { useState } from 'react';
import { 
  StyleSheet, 
  Text, 
  View, 
  ScrollView,
  TouchableOpacity,
  ActivityIndicator
} from 'react-native';
import AssignmentCard from '../components/assignmentcards';

export default function AgentDashboard() {
    // 1. State for assignments list and loading indicator
    const [assignments, setAssignments] = useState([]);
    const [loading, setLoading] = useState(false);

    // 2. Updated Fetch Function
    const fetchPendingAssignments = async () => {
        setLoading(true);
        try {
            const response = await fetch('http://192.168.0.71:8000/fetchPendingAssignments', {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error(`HTTP Error: ${response.status}`);
            }

            const json = await response.json();
            console.log("Fetched payload:", json);

            // Check how your API returns the list. 
            // If it returns an array directly: json
            // If it returns an object like { assignments: [...] }: json.assignments
            const fetchedList = Array.isArray(json) ? json : json.all_pending_assgn || [];            
            setAssignments(fetchedList);
        } catch (error) {
            console.error("Fetch error details:", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <View style={styles.container}>
            {/* Header */}
            <View style={styles.header}>
                <View>
                    <Text style={styles.headerTitle}>GC Agent</Text>
                    <Text style={styles.headerSubtitle}>Classroom Automation & AI</Text>
                </View>
            </View>

            {/* Main Vertical Scroll */}
                
                {/* Metric Card (Your custom counter UI) */}
                <View style={styles.metricCard}>
                    <TouchableOpacity 
                        style={styles.PendinAssgnBanner}
                        onPress={fetchPendingAssignments}
                        activeOpacity={0.8}
                    >
                        {loading ? (
                            <ActivityIndicator size="large" color="#ffffff" />
                        ) : (
                            <Text style={styles.metricValue} adjustsFontSizeToFit={true} numberOfLines={1}>
                                {assignments.length}
                            </Text>
                        )}
                    </TouchableOpacity>

                    {/* Adding some context text to the empty right side of the card */}
                    <View style={styles.metricTextContainer}>
                        <Text style={styles.metricLabel}>Pending</Text>
                        <Text style={styles.metricSubLabel}>Assignments</Text>
                        <Text style={styles.tapPrompt}>Tap orange box to refresh 🔄</Text>
                    </View>
                </View>

                {/* Section Title */}
                <Text style={styles.sectionTitle}>Recent Assignments</Text>
            <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>

                {/* Horizontal Scroll Window for Cards */}
                <ScrollView 
                    contentContainerStyle={styles.horizontalScrollContent}
                >
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
                                    dueDate={item.dueDate ?? "No due date"} // Uses 'No due date' if null or undefined
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
        backgroundColor: '#000000', // Your dark background theme
        justifyContent: 'center',
    },
    header: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        paddingHorizontal: 20,
        paddingVertical: 16,
        borderBottomWidth: 1,
        borderBottomColor: 'rgba(255, 255, 255, 0.1)', // Softened the border for dark mode
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
    scrollContent: {
        paddingVertical: 20,
    },
    metricCard: {
        flexDirection: 'row',
        justifyContent: 'flex-start',
        alignItems: 'center',
        // backgroundColor: '#0F172A',
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
        fontSize: 100, // Reduced slightly so it doesn't clip on smaller phones
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
    horizontalScrollContent: {
        paddingHorizontal: 20, // aligns with the rest of your app margins
        justifyContent: 'center',
        backgroundColor: '#0F172A',
        width:'100%'

    },
    cardWrapper: {
        width: '100%',
        marginRight: 16, // Gap between assignment cards
    },
    emptyCard: {
        width :'100%',
        height: 140,
        backgroundColor: 'rgba(255, 255, 255, 0.1)',
        borderRadius: 16,
        justifyContent: 'center',
        alignItems: 'center',
        borderWidth: 1,
        borderColor: 'rgba(255, 255, 255, 0.2)',
        borderStyle: 'dashed',
        alignSelf: 'center',
    },
    emptyText: {
        color: '#F8FAFC',
        fontSize: 14,
    },
});