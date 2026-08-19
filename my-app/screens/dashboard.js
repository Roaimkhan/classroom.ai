import React, {useState} from 'react';
import { 
  StyleSheet, 
  Text, 
  View, 
  ScrollView, 
  SafeAreaView 
} from 'react-native';

export default function AgentDashboard() {
    const [data, setData] = useState(null);

    const handlePress = async () => {
    try {
        const response = await fetch('http://your-backend-url/api');
        const json = await response.json();
        setData(json);
    } catch (error) {
        console.error(error);
    }
    };

  return (
    <SafeAreaView style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <View>
          <Text style={styles.headerTitle}>GC Agent</Text>
          <Text style={styles.headerSubtitle}>Classroom Automation & AI</Text>
        </View>
      </View>

      <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
        
        {/* Pending Assignments Card */}
        <View style={styles.metricCard}>
          <Text style={styles.metricLabel}>Pending Assignments</Text>
          <Text style={styles.metricValue} onPress={handlePress}>{data}</Text>
        </View>

      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#020617', // slate-950
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#1E293B',
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
    padding: 20,
  },
  metricCard: {
    backgroundColor: '#0F172A',
    borderRadius: 12,
    padding: 20,
    borderWidth: 1,
    borderColor: '#1E293B',
  },
  metricLabel: {
    fontSize: 12,
    color: '#94A3B8',
    textTransform: 'uppercase',
    fontWeight: '600',
  },
  metricValue: {
    fontSize: 36,
    fontWeight: 'bold',
    color: '#F8FAFC',
    marginTop: 8,
  },
});