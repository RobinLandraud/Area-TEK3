import LoginPage from './src/Pages/login';
import RegisterPage from './src/Pages/register';
import HomePage from './src/Pages/home';
import AboutPage from './src/Pages/about';
import MySpacePage from './src/Pages/mySpace';
import ServicesPage from './src/Pages/services';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

export default function App() {
  const Tab = createBottomTabNavigator();
  
  return (
    <NavigationContainer>
      <Tab.Navigator>
        <Tab.Screen name="Accueil" component={HomePage} />
        <Tab.Screen name="A propos" component={AboutPage} />
        <Tab.Screen name="Mon espace" component={MySpacePage} />
        <Tab.Screen name="Nos services" component={ServicesPage} />
        <Tab.Screen name="Connexion" component={LoginPage} />
        <Tab.Screen name="Nouveau Compte" component={RegisterPage} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
