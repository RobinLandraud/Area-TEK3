import React, { useState } from 'react';
import { StyleSheet, Text, View , Button, TextInput} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import axios from 'axios';

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    const headers = { 
      'Content-Type' : 'application/json',
    }
    const body = {
      username: username,
      password: password,
    }
    await axios.post('http://localhost:8080/accounts/login/', JSON.stringify(body), { headers, withCredentials: true }
      ).then((response) => {
        console.log(response);
      }
      ).catch((error) => {
        console.log(error);
      }
    );
  }

  return (
    <View style={styles.container}>
    <StatusBar style="auto" />
      <Text style={{ fontSize: 24, fontWeight: 'bold', marginBottom: 16 }}>Connexion</Text>
      <View style={{ marginBottom: 16 }}>
        <Text style={{ fontSize: 16 }}>Nom d'utilisateur:</Text>
        <TextInput
          style={{ height: 40, borderColor: 'gray', borderWidth: 1 }}
          onChangeText={text => setUsername(text)}
          value={username}
        />
      </View>
      <View style={{ marginBottom: 16 }}>
        <Text style={{ fontSize: 16 }}>Mot de passe:</Text>
        <TextInput
          style={{ height: 40, borderColor: 'gray', borderWidth: 1 }}
          onChangeText={text => setPassword(text)}
          value={password}
          secureTextEntry={true}
        />
      </View>
      <Button
        title="Se connecter"
        onPress={handleLogin}
      />
    </View>
  );
}

export default LoginPage;

const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: '#fff',
      alignItems: 'center',
      justifyContent: 'center',
    },
});