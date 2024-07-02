// ArticleDetail.tsx
import React from 'react';
import { Box } from '@mui/material';
import PaperSearch from './paper-search';
import PaperList from './paper-list';


const PaperPage: React.FC = () => {
    return (
        <Box sx={{ display: 'flex', height: '100%' }}>
            <PaperSearch />
            <PaperList />
        </Box>

    );
};

export default PaperPage;
