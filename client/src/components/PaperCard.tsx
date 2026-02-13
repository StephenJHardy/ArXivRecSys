import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  IconButton,
  Collapse,
  Link,
  Grid,
  Tooltip,
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  ChevronRight as ChevronRightIcon,
} from '@mui/icons-material';
import RatingStars from './RatingStars';
import { useAppDispatch, useAppSelector } from '../store/hooks';
import { ratePaper, selectUserRatings, fetchUserRatings } from '../store/papersSlice';

interface PaperCardProps {
  paper: {
    id: number;
    arxiv_id: string;
    title: string;
    abstract: string;
    authors: string;
    categories: string;
    published_date: string;
    score: number;
  };
}

export const PaperCard: React.FC<PaperCardProps> = ({ paper }) => {
  const [expanded, setExpanded] = useState(false);
  const dispatch = useAppDispatch();
  const userRatings = useAppSelector(selectUserRatings);

  useEffect(() => {
    dispatch(fetchUserRatings());
  }, [dispatch]);

  const handleExpandClick = () => {
    setExpanded(!expanded);
  };

  const handleRatingChange = (newValue: number | null) => {
    if (newValue !== null) {
      dispatch(ratePaper({ paperId: paper.id, rating: newValue }));
    }
  };

  const cleanAbstract = (text: string) => {
    return text.replace(/\s+/g, ' ').trim();
  };

  const arxivUrl = `https://arxiv.org/abs/${paper.arxiv_id}`;

  return (
    <Card sx={{ mb: 1 }}>
      <CardContent sx={{ py: 1, '&:last-child': { pb: 1 } }}>
        <Grid container spacing={1} alignItems="center" sx={{ mb: expanded ? 2 : 0 }}>
          {/* Title and Expand Button */}
          <Grid item xs={12} md={5}>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <IconButton
                onClick={handleExpandClick}
                aria-expanded={expanded}
                aria-label="show more"
                size="small"
                sx={{ mr: 1 }}
              >
                {expanded ? <ExpandMoreIcon /> : <ChevronRightIcon />}
              </IconButton>
              <Tooltip title={paper.title}>
                <Typography
                  variant="subtitle1"
                  component="div"
                  noWrap
                  sx={{ 
                    fontWeight: 'medium',
                    '&:hover': { textDecoration: 'underline' }
                  }}
                >
                  <Link
                    href={arxivUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    color="inherit"
                    underline="none"
                  >
                    {paper.title}
                  </Link>
                </Typography>
              </Tooltip>
            </Box>
          </Grid>

          {/* Authors */}
          <Grid item xs={12} md={3}>
            <Tooltip title={paper.authors}>
              <Typography variant="body2" color="text.secondary" noWrap>
                {paper.authors}
              </Typography>
            </Tooltip>
          </Grid>

          {/* Categories */}
          <Grid item xs={12} md={2}>
            <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap', overflow: 'hidden' }}>
              {paper.categories.split(' ').map((category) => (
                <Chip
                  key={category}
                  label={category}
                  size="small"
                  sx={{ 
                    minWidth: 'auto',
                    fontSize: '0.7rem',
                    height: '20px'
                  }}
                />
              ))}
            </Box>
          </Grid>

          {/* Score and Rating */}
          <Grid item xs={12} md={2}>
            <Box sx={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'center', gap: 1 }}>
              <Tooltip title="Paper Score">
                <Typography variant="body2" color="text.secondary">
                  Score: {paper.score.toFixed(2)}
                </Typography>
              </Tooltip>
              <RatingStars
                value={userRatings[paper.id] || null}
                onChange={handleRatingChange}
              />
            </Box>
          </Grid>
        </Grid>

        {/* Abstract (Expandable) */}
        <Collapse in={expanded} timeout="auto" unmountOnExit sx={{ width: '100%' }}>
          <Typography
            variant="body2"
            color="text.secondary"
            sx={{ whiteSpace: 'pre-wrap' }}
          >
            {cleanAbstract(paper.abstract)}
          </Typography>
        </Collapse>
      </CardContent>
    </Card>
  );
};

export default PaperCard; 