import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
export default function AssignmentCard({ 
    course, 
    dueDate, 
    title, 
    description, 
    status, 
    onPressAssignment 
}) {    
    return (
        <View style={styles.card}>
            {/* Left Accent Stripe (Matches the orange accent bar on the left edge) */}
            {/* <View style={styles.accentStripe}>
                <Text style={styles.stripeText}>{status || "Due Soon"}</Text>
            </View> */}

            <View style={styles.contentContainer}>
                {/* Top Row: Subject & Due Date */}
                <View style={styles.topRow}>
                    <Text style={styles.subjectText}>{course || "AP World History"}</Text>
                    <Text style={styles.dueDateText}>{dueDate || "DUE: Today, 11:59 PM"}</Text>
                </View>

                {/* Middle Section: Title & Description */}
                <Text style={styles.titleText}>{title || "Chapter 14 Quiz: Roman Empire"}</Text>
                <Text style={styles.descText}>{description || "Multiple choice quiz. 20 min limit. Check materials."}</Text>

                {/* Bottom Row: Status Tag & Action Button */}
                <View style={styles.bottomRow}>
                    <TouchableOpacity 
                        style={styles.button} 
                        onPress={onPressAssignment}
                        activeOpacity={0.8}
                    >
                        <Text style={styles.buttonText}>Open Assignment</Text>
                    </TouchableOpacity>
                </View>
            </View>
        </View>
    );
}

const styles = StyleSheet.create({
    card: {
        backgroundColor: '#020202',
        borderRadius: 16,
        width: '97%',
        alignSelf: 'center',
        marginVertical: 8,
        flexDirection: 'row', // Allows the left accent stripe to sit side-by-side with content
        overflow: 'hidden',  // Keeps the stripe neatly clipped inside the rounded corners
        borderWidth: 1, 
        borderColor:'#363636', 
        borderStyle: 'solid',
        
        // iOS Shadow
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.08,
        shadowRadius: 6,
        // Android Shadow
        elevation: 3,
    },
    accentStripe: {
        width: 50,
        backgroundColor: '#ffffff',
        justifyContent: 'center', 
        alignItems: 'center',     
    },
    stripeText: {
        color: '#000000',
        fontSize: 20,
        fontWeight: 'bold',
        textTransform: 'uppercase',
        // Fixes wrapping: sets a fixed track length for the text before rotation
        width: 100, 
        textAlign: 'center',
        transform: [{ rotate: '-90deg' }], 
    },
    contentContainer: {
        flex: 1,
        padding: 16,
    },
    topRow: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 6,
    },
    subjectText: {
        fontSize: 13,
        fontWeight: 'bold',
        color: '#ffffff',
    },
    dueDateText: {
        fontSize: 11,
        fontWeight: '600',
        color: '#ffffff',
    },
    titleText: {
        fontSize: 17,
        fontWeight: 'bold',
        color: '#ffffff',
        marginBottom: 4,
    },
    descText: {
        fontSize: 13,
        color: '#7b7b7b',
        marginBottom: 16,
    },
    bottomRow: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        marginTop: 4,
    },
    statusText: {
        fontSize: 14,
        fontWeight: '600',
        color: '#e07a5f', // Orange text matching status theme
    },
    button: {
        backgroundColor: '#fdfcfc',
        paddingVertical: 8,
        paddingHorizontal: 16,
        borderRadius: 20, // Pill-shaped button style from screenshot
    },
    buttonText: {
        color: '#000000',
        fontSize: 13,
        fontWeight: 'bold',
    },
});