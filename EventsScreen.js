import { useState } from 'react';


import {
    ActivityIndicator,
    FlatList,
    Linking,
    StyleSheet,
    Text,
    TouchableOpacity,
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

export default function EventsScreen({ route }) {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');  
  const [city, setSelectedCity] = useState(
    route?.params?.city || TOP_CITIES[0]
  );

  const data = TOP_CITIES.map((city, index) => ({
    key: index,
    label: city
  }));


  const renderItem = ({ item }) => (
    <View style={styles.card}>
      <Text style={styles.eventName}>{item.name}</Text>
      <Text>Date: {item.date}</Text>
      <Text>Time: {item.time}</Text>
      <Text>Estimated Attendees: {item.estimatedAttendees}</Text>
      <Text>Rank: {item.rank}</Text>
      <Text>Venue: {item.venue}</Text>

      <View style={styles.linkRow}>
        <TouchableOpacity onPress={() => Linking.openURL(item.directionsUrl)}>
          <Text style={styles.link}>Directions</Text>
        </TouchableOpacity>
        <TouchableOpacity onPress={() => Linking.openURL(item.ticketUrl)}>
          <Text style={styles.link}>Buy Tickets</Text>
        </TouchableOpacity>
      </View>
    </View>
  );

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Events in {city}</Text>

      <Text style={styles.label}>Change City</Text>
      <ModalSelector
        data={data}
        initValue={city}
        onChange={(option) => setSelectedCity(option.label)}
        style={styles.selector}
        selectStyle={styles.selectStyle}
        selectTextStyle={styles.selectTextStyle}
      />

      {/* Replace this with actual event rendering */}
      <Text style={styles.eventsText}>Showing events for {city}</Text>
      
{loading && <ActivityIndicator size="large" color="#007AFF" />}
      {error !== '' && <Text style={styles.error}>{error}</Text>}

      {!loading && events.length === 0 && (
        <Text style={styles.eventsText}>No events found for {city}</Text>
      )}

      <FlatList
        data={events}
        renderItem={renderItem}
        keyExtractor={(item, index) => index.toString()}
        contentContainerStyle={styles.listContainer}
      />

    </View>
  );
  
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 24,
    textAlign: 'center',
  },
  label: {
    fontSize: 16,
    marginBottom: 8,
  },
  selector: {
    marginBottom: 16,
  },
  selectStyle: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 8,
    padding: 12,
  },
  selectTextStyle: {
    fontSize: 16,
  },
  eventsText: {
    fontSize: 16,
    marginTop: 16,
    textAlign: 'center',
  },
  error: {
    color: 'red',
    textAlign: 'center',
    marginVertical: 10,
  },
  listContainer: {
    paddingBottom: 32,
  },
  card: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 12,
    marginBottom: 16,
    backgroundColor: '#f9f9f9',
  },
  eventName: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 6,
  },
  linkRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 8,
  },
  link: {
    color: '#007AFF',
    fontWeight: 'bold',
  },
});