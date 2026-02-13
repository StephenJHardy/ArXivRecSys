import React, { useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import { Box, Container } from '@mui/material';
import NavigationBar from './components/NavigationBar';
import DailySection from './components/DailySection';
import { useAppSelector } from './store/hooks';
import { selectIsAuthenticated } from './store/authSlice';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ProtectedRoute from './components/ProtectedRoute';

const App: React.FC = () => {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const isAuthenticated = useAppSelector(selectIsAuthenticated);

  const handleToggleTheme = () => {
    setIsDarkMode(!isDarkMode);
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <NavigationBar onToggleTheme={handleToggleTheme} isDarkMode={isDarkMode} />
      <Container component="main" sx={{ mt: 4, mb: 4, flex: 1 }}>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route
            path="/"
            element={
              <ProtectedRoute isAuthenticated={isAuthenticated}>
                <DailySection />
              </ProtectedRoute>
            }
          />
        </Routes>
      </Container>
    </Box>
  );
};

export default App; 