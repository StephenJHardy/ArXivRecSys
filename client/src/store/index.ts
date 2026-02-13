import { configureStore } from '@reduxjs/toolkit';
import { enableMapSet } from 'immer';
import authReducer from './authSlice';
import papersReducer from './papersSlice';

// Enable the MapSet plugin for Immer
enableMapSet();

export const store = configureStore({
  reducer: {
    auth: authReducer,
    papers: papersReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch; 