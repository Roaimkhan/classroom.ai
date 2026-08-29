import React from 'react';
import { 
  Modal, 
  View, 
  Text, 
  StyleSheet, 
  TouchableOpacity, 
  ScrollView, 
  Pressable 
} from 'react-native';
import { BlurView } from 'expo-blur';
import { FontAwesome6 } from '@expo/vector-icons';

export default function AssignmentView({ visible, onClose }) {
  return (
    <Modal
      animationType="slide"
      transparent={true}
      visible={visible}
      onRequestClose={onClose}
    >
      {/* Dimmed Backdrop with Tap-to-Close */}
      <Pressable style={styles.overlay} onPress={onClose}>
        <BlurView intensity={30} tint="dark" style={StyleSheet.absoluteFill} />
      </Pressable>

      {/* Main Modal Card */}
      <View style={styles.modalContainer}>
        {/* Top Handle Bar */}
        <View style={styles.dragHandle} />

        {/* Modal Header */}
        <View style={styles.header}>
          <View style={styles.headerTitleGroup}>
            <Text style={styles.assignmentId}>872038706318</Text>
            <Text style={styles.title}>TEST B</Text>
          </View>

          <TouchableOpacity onPress={onClose} style={styles.closeButton}>
            <FontAwesome6 name="xmark" size={18} color="#A0A0A0" />
          </TouchableOpacity>
        </View>

        {/* Status Badge Line */}
        <View style={styles.statusRow}>
          <View style={styles.badge}>
            <Text style={styles.badgeText}>WITHOUT DUE DATE</Text>
          </View>
          <Text style={styles.dueDateText}>No due date</Text>
        </View>

        {/* Scrollable Assignment Details Body */}
        <ScrollView 
          showsVerticalScrollIndicator={false} 
          contentContainerStyle={styles.scrollBody}
        >
          <Text style={styles.sectionLabel}>Description</Text>
          <Text style={styles.descriptionText}>
            This assignment from test b. Make sure to complete all requirements and attach your solution files before submitting.
          </Text>

          {/* Attachments Placeholder */}
          <Text style={styles.sectionLabel}>Attachments</Text>
          <TouchableOpacity style={styles.attachmentCard} activeOpacity={0.7}>
            <FontAwesome6 name="file-pdf" size={22} color="#FF5252" />
            <View style={styles.attachmentMeta}>
              <Text style={styles.attachmentTitle}>Assignment_Instructions.pdf</Text>
              <Text style={styles.attachmentSize}>2.4 MB</Text>
            </View>
            <FontAwesome6 name="arrow-down-to-line" size={16} color="#707070" />
          </TouchableOpacity>

          {/* Submission / Status Info */}
          <Text style={styles.sectionLabel}>Your Work</Text>
          <View style={styles.workBox}>
            <FontAwesome6 name="circle-check" size={20} color="#4CAF50" />
            <Text style={styles.workStatusText}>Not Submitted</Text>
          </View>
        </ScrollView>

        {/* Footer Action Buttons */}
        <View style={styles.actionFooter}>
          <TouchableOpacity style={styles.primaryBtn} activeOpacity={0.85}>
            <FontAwesome6 name="upload" size={16} color="#FFFFFF" style={{ marginRight: 8 }} />
            <Text style={styles.primaryBtnText}>Submit Assignment</Text>
          </TouchableOpacity>
        </View>
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  overlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: 'rgba(0, 0, 0, 0.6)',
  },
  modalContainer: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    maxHeight: '85%',
    backgroundColor: '#000000',
    borderTopLeftRadius: 28,
    borderTopRightRadius: 28,
    borderWidth: 1,
    borderColor: '#262626',
    paddingHorizontal: 20,
    paddingTop: 12,
    paddingBottom: 30,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: -10 },
    shadowOpacity: 0.35,
    shadowRadius: 16,
    elevation: 20,
  },
  dragHandle: {
    width: 36,
    height: 4,
    backgroundColor: '#3A3A3A',
    borderRadius: 2,
    alignSelf: 'center',
    marginBottom: 16,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 12,
  },
  headerTitleGroup: {
    flex: 1,
  },
  assignmentId: {
    color: '#8E8E93',
    fontSize: 12,
    fontWeight: '600',
    letterSpacing: 0.5,
    marginBottom: 2,
  },
  title: {
    color: '#FFFFFF',
    fontSize: 22,
    fontWeight: '700',
  },
  closeButton: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: '#222222',
    justifyContent: 'center',
    alignItems: 'center',
  },
  statusRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 20,
    paddingBottom: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#222222',
  },
  badge: {
    backgroundColor: '#FF5522',
    paddingVertical: 4,
    paddingHorizontal: 10,
    borderRadius: 6,
  },
  badgeText: {
    color: '#FFFFFF',
    fontSize: 10,
    fontWeight: '800',
    letterSpacing: 0.5,
  },
  dueDateText: {
    color: '#A0A0A0',
    fontSize: 13,
  },
  scrollBody: {
    paddingBottom: 20,
  },
  sectionLabel: {
    color: '#8E8E93',
    fontSize: 12,
    fontWeight: '700',
    textTransform: 'uppercase',
    letterSpacing: 0.8,
    marginTop: 12,
    marginBottom: 8,
  },
  descriptionText: {
    color: '#E0E0E0',
    fontSize: 15,
    lineHeight: 22,
  },
  attachmentCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#1E1E1E',
    padding: 12,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#2A2A2A',
    marginBottom: 12,
  },
  attachmentMeta: {
    flex: 1,
    marginLeft: 12,
  },
  attachmentTitle: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: '600',
  },
  attachmentSize: {
    color: '#707070',
    fontSize: 12,
    marginTop: 2,
  },
  workBox: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#1E1E1E',
    padding: 14,
    borderRadius: 12,
    gap: 10,
  },
  workStatusText: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: '600',
  },
  actionFooter: {
    paddingTop: 16,
    borderTopWidth: 1,
    borderTopColor: '#222222',
  },
  primaryBtn: {
    backgroundColor: '#FF5522',
    flexDirection: 'row',
    height: 50,
    borderRadius: 25,
    justifyContent: 'center',
    alignItems: 'center',
  },
  primaryBtnText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '700',
  },
});