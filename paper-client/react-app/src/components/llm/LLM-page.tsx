// ArticleDetail.tsx
import React from 'react';
import { Box, Typography } from '@mui/material';
import LLMTable from './LLM-PromptTable';


const LLMPage: React.FC = () => {
    return (
        <Box sx={{ display: 'flex', height: '100%' }}>
            <Box sx={{ width: '15%', borderRight: '1px solid grey', p: 2 }}>
                <Typography variant="h6">Search</Typography>
                {/* 検索機能のコンテンツをここに追加 */}
            </Box>
            <Box sx={{ width: '85%', p: 2 }}>
                <Typography variant="h6">DBからとってきたリスト</Typography>
                <Box component="main" sx={{ flexGrow: 1, bgcolor: 'background.default', p: 3, display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                    <LLMTable />
                </Box>
            </Box>
        </Box>
    );
};

export default LLMPage;
