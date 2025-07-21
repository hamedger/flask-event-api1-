import React, { useState } from 'react';
import {
  Alert,
  Button,
  StyleSheet,
  Text,
  TextInput,
  View
} from 'react-native';
import ModalSelector from 'react-native-modal-selector';

const TOP_CITIES = [
  'New York',
  'Detroit',
  'Los Angeles',
  'Chicago',
  'Houston',
  'Phoenix',
  'Philadelphia',
  'San Antonio',
  'San Diego',
  'Dallas',
  'San Jose'
];

export default function SignInScreen({ navigation }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [selectedCity, setSelectedCity] = useState('');

  // Prepare data for ModalSelector
  const data = TOP_CITIES.map((city, index) => ({
    key: index,
    label: city
  }));

const handleSignIn = () => {
 {/*} if (!email || !password || !selectedCity) {. */}
  if (!selectedCity) {
    Alert.alert('Error', 'Please enter email, password, and select a city.');
    return;
  }
  // Navigate to Events screen, pass selectedCity
  navigation.navigate('Events', { city: selectedCity });
};


  return (
    <View style={styles.container}>
      <Text style={styles.title}>Event Finder Login</Text>
    
{/*}
      <Text style={styles.label}>Email address</Text>
      <TextInput
        placeholder="Email"
        value={email}
        onChangeText={setEmail}
        style={styles.input}
        keyboardType="email-address"
        autoCapitalize="none"
      />
    
      <Text style={styles.label}>Password</Text>
      <TextInput
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
        style={styles.input}
      />
  */}
      <Text style={styles.label}>Select Your City</Text>
      <ModalSelector
        data={data}
        initValue="Select a city"
        onChange={(option) => setSelectedCity(option.label)}
        style={styles.modalSelector}
        selectStyle={styles.selectStyle}
        selectTextStyle={styles.selectTextStyle}
      />

      <Button title="Sign In" onPress={handleSignIn} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 16,
    flex: 1,
    justifyContent: 'center',
    backgroundColor: '#fff'
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 24,
    textAlign: 'center'
  },
  input: {
    height: 48,
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 8,
    paddingHorizontal: 12,
    marginBottom: 16
  },
  label: {
    fontSize: 16,
    marginBottom: 8
  },
  modalSelector: {
    marginBottom: 24
  },
  selectStyle: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 8,
    padding: 12
  },
  selectTextStyle: {
    fontSize: 16
  }
});
