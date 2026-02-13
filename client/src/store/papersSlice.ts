import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import type { RootState } from './index';
import { api } from '../services/api';

interface Paper {
  id: number;
  arxiv_id: string;
  title: string;
  abstract: string;
  authors: string;
  categories: string;
  published_date: string;
  score: number;
}

interface DateInfo {
  date: string;
  count: number;
}

interface Rating {
  id: number;
  paper_id: number;
  rating: number;
  created_at: string;
}

interface PapersState {
  dates: DateInfo[];
  papersByDate: Record<string, Paper[]>;
  loadedDates: Set<string>;
  userRatings: Record<number, number>;  // Map of paper_id to rating
  isLoading: boolean;
  error: string | null;
}

const initialState: PapersState = {
  dates: [],
  papersByDate: {},
  loadedDates: new Set(),
  userRatings: {},
  isLoading: false,
  error: null,
};

export const fetchDates = createAsyncThunk(
  'papers/fetchDates',
  async () => {
    const response = await api.get('/api/papers/dates');
    return response.data;
  }
);

export const fetchPapersByDate = createAsyncThunk(
  'papers/fetchByDate',
  async (date: string) => {
    const response = await api.get(`/api/papers/${date}`);
    return { date, papers: response.data };
  }
);

export const fetchUserRatings = createAsyncThunk(
  'papers/fetchUserRatings',
  async () => {
    const response = await api.get('/api/users/me/ratings');
    return response.data;
  }
);

export const ratePaper = createAsyncThunk(
  'papers/rate',
  async ({ paperId, rating }: { paperId: number; rating: number }, { dispatch }) => {
    const response = await api.post(`/api/papers/${paperId}/rate`, { rating_value: rating });
    // Fetch updated ratings after successful rating submission
    await dispatch(fetchUserRatings());
    return response.data;
  }
);

const papersSlice = createSlice({
  name: 'papers',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchDates.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchDates.fulfilled, (state, action) => {
        state.isLoading = false;
        state.dates = action.payload.dates;
      })
      .addCase(fetchDates.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || 'Failed to fetch paper dates';
      })
      .addCase(fetchPapersByDate.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchPapersByDate.fulfilled, (state, action) => {
        state.isLoading = false;
        state.papersByDate[action.payload.date] = action.payload.papers;
        state.loadedDates.add(action.payload.date);
      })
      .addCase(fetchPapersByDate.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || 'Failed to fetch papers';
      })
      .addCase(fetchUserRatings.fulfilled, (state, action) => {
        const ratings = action.payload as Rating[];
        state.userRatings = {};
        ratings.forEach(rating => {
          state.userRatings[rating.paper_id] = rating.rating;
        });
      })
      .addCase(ratePaper.fulfilled, (state, action) => {
        // The ratings will be updated by the fetchUserRatings action
      });
  },
});

export const { clearError } = papersSlice.actions;

export const selectDates = (state: RootState) => state.papers.dates;
export const selectPapersByDate = (state: RootState) => state.papers.papersByDate;
export const selectLoadedDates = (state: RootState) => state.papers.loadedDates;
export const selectPapersError = (state: RootState) => state.papers.error;
export const selectIsLoading = (state: RootState) => state.papers.isLoading;
export const selectUserRatings = (state: RootState) => state.papers.userRatings;

export default papersSlice.reducer; 