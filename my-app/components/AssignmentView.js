import React, { useState } from 'react';
import { 
  Modal, 
  View, 
  Text, 
  StyleSheet, 
  TouchableOpacity, 
  ScrollView, 
  Pressable,
  Linking,
  Alert,
} from 'react-native';
import { BlurView } from 'expo-blur';
import { FontAwesome6 } from '@expo/vector-icons';

const getMaterialUrl = (material) => {
  if (!material || typeof material !== 'object') return null;

  if (typeof material.driveFile === 'string' && material.driveFile) {
    return `https://drive.google.com/open?id=${encodeURIComponent(material.driveFile)}`;
  }

  const url = material.youtubeVideoLink || material.Link;
  return typeof url === 'string' && /^https?:\/\//i.test(url) ? url : null;
};

const getMaterialTitle = (material, index) => {
  if (material.driveFile) return `Google Drive file ${index + 1}`;
  if (material.youtubeVideoLink) return `YouTube video ${index + 1}`;
  return `Link ${index + 1}`;
};

const API_BASE_URL = 'http://192.168.0.71:8000';
const COMPLETE_ASSIGNMENT_TIMEOUT_MS = 1000000;

export default function AssignmentView({ visible, onClose, assignment }) {
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Guard clause to handle null or undefined data
  if (!assignment) return null;

  const attachments = (Array.isArray(assignment.materials) ? assignment.materials : [])
    .map((material, index) => ({ material, index, url: getMaterialUrl(material) }))
    .filter(({ url }) => url);

  const handleOpenAttachment = async (url) => {
    try {
      const supported = await Linking.canOpenURL(url);
      if (!supported) throw new Error('This link cannot be opened on this device.');
      await Linking.openURL(url);
    } catch (error) {
      Alert.alert('Unable to open attachment', error.message || 'Please try again.');
    }
  };

  const handleSubmitAssignment = async () => {
    if (!assignment.id) {
      Alert.alert('Unable to submit assignment', 'This assignment does not have an ID.');
      return;
    }

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), COMPLETE_ASSIGNMENT_TIMEOUT_MS);

    setIsSubmitting(true);
    try {
      const response = await fetch(
        `${API_BASE_URL}/assignments/${encodeURIComponent(assignment.id)}/complete`,
        {
          method: 'POST',
          headers: { Accept: 'application/json' },
          signal: controller.signal,
        },
      );

      if (!response.ok) {
        throw new Error(`Server returned status ${response.status}`);
      }

      Alert.alert('Assignment submitted', 'Your assignment has been sent for completion.');
    } catch (error) {
      const message = error.name === 'AbortError'
        ? 'The request timed out. Please try again.'
        : error.message || 'Please try again.';
      Alert.alert('Unable to submit assignment', message);
      console.error('[Assignment Submit Error]:', error);
    } finally {
      clearTimeout(timeoutId);
      setIsSubmitting(false);
    }
  };

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
            <Text style={styles.assignmentId}>
              {assignment.id || assignment.subject || 'ASSIGNMENT'}
            </Text>
            <Text style={styles.title}>
              {assignment.title || 'Untitled Assignment'}
            </Text>
          </View>

          <TouchableOpacity onPress={onClose} style={styles.closeButton}>
            <FontAwesome6 name="xmark" size={18} color="#A0A0A0" />
          </TouchableOpacity>
        </View>

        {/* Status Badge Line */}
        <View style={styles.statusRow}>
          <View style={styles.badge}>
            <Text style={styles.badgeText}>
              {(assignment.status || assignment.due_date_status || 'PENDING').toUpperCase()}
            </Text>
          </View>
          <Text style={styles.dueDateText}>
            {assignment.dueDate || 'No due date'}
          </Text>
        </View>

        {/* Scrollable Assignment Details Body */}
        <ScrollView 
          showsVerticalScrollIndicator={false} 
          contentContainerStyle={styles.scrollBody}
        >
          <Text style={styles.sectionLabel}>Description</Text>
          <Text style={styles.descriptionText}>
            {assignment.description || 'No description provided.'}
          </Text>

          {/* Attachments */}
          <Text style={styles.sectionLabel}>Attachments</Text>
          {attachments.length ? (
            attachments.map(({ material, index, url }) => (
              <TouchableOpacity
                key={`${assignment.id}-${index}`}
                style={styles.attachmentCard}
                activeOpacity={0.7}
                onPress={() => handleOpenAttachment(url)}
              >
                <FontAwesome6 name="link" size={20} color="#5D9CEC" />
                <View style={styles.attachmentMeta}>
                  <Text style={styles.attachmentTitle} numberOfLines={1}>
                    {getMaterialTitle(material, index)}
                  </Text>
                  <Text style={styles.attachmentSize}>Tap to open</Text>
                </View>
                <FontAwesome6 name="arrow-up-right-from-square" size={15} color="#A0A0A0" />
              </TouchableOpacity>
            ))
          ) : (
            <Text style={styles.emptyAttachmentsText}>No attachments were provided.</Text>
          )}

          {/* Submission / Status Info */}
          <Text style={styles.sectionLabel}>Your Work</Text>
          <View style={styles.workBox}>
            <FontAwesome6 
              name={assignment.isSubmitted ? "circle-check" : "circle-xmark"} 
              size={20} 
              color={assignment.isSubmitted ? "#4CAF50" : "#FF5252"} 
            />
            <Text style={styles.workStatusText}>
              {assignment.isSubmitted ? "Submitted" : "Not Submitted"}
            </Text>
          </View>
        </ScrollView>

        {/* Footer Action Buttons */}
        <View style={styles.actionFooter}>
          <TouchableOpacity
            style={[styles.primaryBtn, isSubmitting && styles.primaryBtnDisabled]}
            activeOpacity={0.85}
            disabled={isSubmitting}
            onPress={handleSubmitAssignment}
          >
            <FontAwesome6 name="upload" size={16} color="#000000" style={{ marginRight: 8 }} />
            <Text style={styles.primaryBtnText}>
              {isSubmitting ? 'Submitting...' : 'Submit Assignment'}
            </Text>
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
    backgroundColor: '#FFFFFF',
    paddingVertical: 4,
    paddingHorizontal: 10,
    borderRadius: 6,
  },
  badgeText: {
    color: '#000',
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
  emptyAttachmentsText: {
    color: '#707070',
    fontSize: 13,
    marginBottom: 8,
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
    backgroundColor: '#908484',
    flexDirection: 'row',
    height: 50,
    borderRadius: 25,
    justifyContent: 'center',
    alignItems: 'center',
  },
  primaryBtnDisabled: {
    opacity: 0.6,
  },
  primaryBtnText: {
    color: '#000000',
    fontSize: 16,
    fontWeight: '700',
  },
});
