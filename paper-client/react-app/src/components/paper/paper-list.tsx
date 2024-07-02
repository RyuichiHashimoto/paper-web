// TableComponent.tsx
import React from 'react';
import PaperTable from './paper-table';
import { Box, Typography, ThemeProvider, IconButton } from '@mui/material';
import theme from 'colortheme/theme'; // 作成したテーマをインポート
import AddPaperButton from "./paper-add-button"
import { AiTwotoneFileAdd } from "react-icons/ai";
import { MdDeleteForever } from "react-icons/md";

const PaperList: React.FC = () => {

    return (
        <ThemeProvider theme={theme}>
            <Box sx={{ p: 2 }}>
                <Typography variant="h6" sx={{ mb: 2 }}>
                    Paper List
                </Typography>
                <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 1 }}>
                    <IconButton aria-label="delete-paper">
                        <MdDeleteForever />
                    </IconButton>
                    <AddPaperButton />
                </Box>
                <Box sx={{ display: 'flex' }}>
                    <PaperTable />
                </Box>
            </Box>
        </ThemeProvider>
    );
};

export default PaperList;
