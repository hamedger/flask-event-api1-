// index.js
import { AppRegistry } from 'react-native';
import App from './defaultApp';
import { name as appName } from './app.json';

AppRegistry.registerComponent(appName, () => App);
