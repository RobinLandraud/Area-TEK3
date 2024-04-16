import React, { useState } from 'react';
import { StyleSheet, Text, View , Button, TextInput} from 'react-native';
import { StatusBar } from 'expo-status-bar';

const AboutPage = () => {
    return (
        <View style={styles.container}>
            <StatusBar style="auto" />
            <Text style={{ fontSize: 24, fontWeight: 'bold', marginBottom: 16 }}>A propos</Text>
        </View>
    );
}

export default AboutPage;

const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: '#fff',
      alignItems: 'center',
      justifyContent: 'center',
    },
});