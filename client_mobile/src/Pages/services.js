import React, { useState } from 'react';
import { StyleSheet, Text, View , Button, TextInput} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import RedditLogin from '../Services/Reddit/redditLogin';
import SpotifyLogin from '../Services/Spotify/spotifyLogin';
import GithubLogin from '../Services/Github/githubLogin';

const ServicesPage = () => {
  return (
    <View style={styles.container}>
      <StatusBar style="auto" />
      <Text style={{ fontSize: 24, fontWeight: 'bold', marginBottom: 16 }}>Nos services</Text>
      <RedditLogin />
      <SpotifyLogin />
      <GithubLogin />
      <Text>Open Weather</Text>
    </View>
  );
}

export default ServicesPage;

const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: '#fff',
      alignItems: 'center',
      justifyContent: 'center',
    },
});