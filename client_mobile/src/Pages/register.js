import React, { useState } from 'react';
import { StyleSheet, Text, View , Button, TextInput} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import axios from 'axios';

const RegisterPage = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleRegister = async () => {
    console.log(`Username: ${username}, Mail: ${email} ,Password: ${password}`);

    const headers = { 
      'Content-Type' : 'application/json',
      withCredentials: true,
    }
    const body = {
      username: username,
      email: email,
      password: password,
    }
    await axios.post('http://localhost:8080/accounts/register/', JSON.stringify(body), { headers }
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
      <Text style={{ fontSize: 24, fontWeight: 'bold', marginBottom: 16 }}>Nouveau compte</Text>
      <View style={{ marginBottom: 16 }}>
        <Text style={{ fontSize: 16 }}>Nom d'utilisateur:</Text>
        <TextInput
          style={{ height: 40, borderColor: 'gray', borderWidth: 1 }}
          onChangeText={text => setUsername(text)}
          value={username}
        />
      </View>
      <View style={{ marginBottom: 16 }}>
        <Text style={{ fontSize: 16 }}>Mail:</Text>
        <TextInput
            style={{ height: 40, borderColor: 'gray', borderWidth: 1 }}
            onChangeText={text => setEmail(text)}
            value={email}
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
        title="Créer un compte"
        onPress={handleRegister}
      />
    </View>
  );
}

export default RegisterPage;

const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: '#fff',
      alignItems: 'center',
      justifyContent: 'center',
    },
});