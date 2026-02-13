import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  IconButton,
} from '@mui/material';
import { Brightness4, Brightness7 } from '@mui/icons-material';
import { useAppDispatch, useAppSelector } from '../store/hooks';
import { logout, selectIsAuthenticated } from '../store/authSlice';

interface NavigationBarProps {
  onToggleTheme?: () => void;
  isDarkMode?: boolean;
}

const NavigationBar: React.FC<NavigationBarProps> = ({
  onToggleTheme,
  isDarkMode,
}) => {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  const isAuthenticated = useAppSelector(selectIsAuthenticated);

  const handleLogout = () => {
    dispatch(logout());
    navigate('/login');
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography
          variant="h6"
          component="div"
          sx={{ flexGrow: 1, cursor: 'pointer' }}
          onClick={() => navigate('/')}
        >
          ArXiv RecSys
        </Typography>

        <Box sx={{ ml: 2 }}>
          {onToggleTheme && (
            <IconButton
              sx={{ ml: 1 }}
              onClick={onToggleTheme}
              color="inherit"
            >
              {isDarkMode ? <Brightness7 /> : <Brightness4 />}
            </IconButton>
          )}

          {isAuthenticated ? (
            <Button color="inherit" onClick={handleLogout}>
              Logout
            </Button>
          ) : (
            <>
              <Button color="inherit" onClick={() => navigate('/login')}>
                Login
              </Button>
              <Button color="inherit" onClick={() => navigate('/register')}>
                Register
              </Button>
            </>
          )}
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default NavigationBar; 