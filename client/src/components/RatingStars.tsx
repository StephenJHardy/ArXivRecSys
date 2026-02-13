import React from 'react';
import { Rating, Box, Tooltip } from '@mui/material';
import { Star as StarIcon } from '@mui/icons-material';

interface RatingStarsProps {
  value: number | null;
  onChange: (newValue: number | null) => void;
}

const RatingStars: React.FC<RatingStarsProps> = ({ value, onChange }) => {
  return (
    <Tooltip title="Rate this paper" placement="left">
      <Box>
        <Rating
          value={value}
          onChange={(_, newValue) => onChange(newValue)}
          precision={1}
          size="small"
          icon={<StarIcon fontSize="small" />}
          emptyIcon={<StarIcon fontSize="small" />}
          max={5}
        />
      </Box>
    </Tooltip>
  );
};

export default RatingStars; 