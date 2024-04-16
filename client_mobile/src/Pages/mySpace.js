import React, { useState } from 'react';
import { StyleSheet, Text, View , Button, TextInput} from 'react-native';
import { StatusBar } from 'expo-status-bar';

const MySpacePage = () => {
  return (
    <View style={styles.container}>
      <StatusBar style="auto" />
      <Text style={{ fontSize: 24, fontWeight: 'bold', marginBottom: 16 }}>Mon espace</Text>
    </View>
  );
}

export default MySpacePage;

const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: '#fff',
      alignItems: 'center',
      justifyContent: 'center',
    },
});