import React, { useEffect, useState } from 'react';
import { Box, Typography, CircularProgress, IconButton, Collapse } from '@mui/material';
import { ExpandMore as ExpandMoreIcon, ChevronRight as ChevronRightIcon } from '@mui/icons-material';
import { useAppDispatch, useAppSelector } from '../store/hooks';
import {
  fetchDates,
  fetchPapersByDate,
  selectDates,
  selectPapersByDate,
  selectLoadedDates,
  selectIsLoading,
  selectPapersError,
} from '../store/papersSlice';
import PaperCard from './PaperCard';

const DailySection: React.FC = () => {
  const dispatch = useAppDispatch();
  const dates = useAppSelector(selectDates);
  const papersByDate = useAppSelector(selectPapersByDate);
  const loadedDates = useAppSelector(selectLoadedDates);
  const isLoading = useAppSelector(selectIsLoading);
  const error = useAppSelector(selectPapersError);
  const [expandedDates, setExpandedDates] = useState<Record<string, boolean>>({});

  useEffect(() => {
    dispatch(fetchDates());
  }, [dispatch]);

  const handleDateExpandClick = (date: string) => {
    const newExpanded = !expandedDates[date];
    setExpandedDates(prev => ({
      ...prev,
      [date]: newExpanded
    }));

    // If we're expanding and haven't loaded the papers yet, fetch them
    if (newExpanded && !loadedDates.has(date)) {
      dispatch(fetchPapersByDate(date));
    }
  };

  if (isLoading && !dates.length) {
    return (
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: '200px',
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ textAlign: 'center', color: 'error.main', mt: 4 }}>
        <Typography variant="h6">{error}</Typography>
      </Box>
    );
  }

  if (!dates.length) {
    return (
      <Box sx={{ textAlign: 'center', mt: 4 }}>
        <Typography variant="h6">No papers available</Typography>
      </Box>
    );
  }

  return (
    <Box>
      {dates.map(dateInfo => {
        const papers = papersByDate[dateInfo.date] || [];
        const isExpanded = expandedDates[dateInfo.date] || false;
        const isDateLoading = isLoading && isExpanded && !loadedDates.has(dateInfo.date);

        return (
          <Box key={dateInfo.date} sx={{ mb: 2, border: 1, borderColor: 'divider', borderRadius: 1 }}>
            <Box 
              sx={{ 
                display: 'flex', 
                alignItems: 'center', 
                p: 1,
                backgroundColor: 'background.paper',
                borderBottom: isExpanded ? 1 : 0,
                borderColor: 'divider',
                cursor: 'pointer'
              }}
              onClick={() => handleDateExpandClick(dateInfo.date)}
            >
              <IconButton
                size="small"
                sx={{ mr: 1 }}
              >
                {isExpanded ? <ExpandMoreIcon /> : <ChevronRightIcon />}
              </IconButton>
              <Typography variant="h6">
                {new Date(dateInfo.date).toLocaleDateString()} ({dateInfo.count} papers)
              </Typography>
            </Box>
            <Collapse in={isExpanded} timeout="auto" unmountOnExit>
              <Box sx={{ p: 2 }}>
                {isDateLoading ? (
                  <Box sx={{ display: 'flex', justifyContent: 'center', p: 2 }}>
                    <CircularProgress />
                  </Box>
                ) : (
                  papers.map((paper) => (
                    <PaperCard key={paper.id} paper={paper} />
                  ))
                )}
              </Box>
            </Collapse>
          </Box>
        );
      })}
    </Box>
  );
}

export default DailySection; 