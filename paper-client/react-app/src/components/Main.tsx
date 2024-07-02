import React, { useState } from 'react';
import { Box, ThemeProvider } from '@mui/material';
import theme from '../colortheme/theme'; // 作成したテーマをインポート
import NavigationBar from './navitabs/NavTabs'; // NavigationBar のインポート

import 'assets/styles/errorMessage.css';

const App: React.FC = () => {
    const [value, setValue] = useState<number>(0);

    const handleChange = (event: React.SyntheticEvent, newValue: number) => {
        setValue(newValue);
    };

    return (
        <ThemeProvider theme={theme}>
            <Box sx={{ display: 'flex', height: '100vh', backgroundColor: '#f5f5f5' }}>
                <Box sx={{ width: '100%' }}>
                    <NavigationBar value={value} handleChange={handleChange} />
                </Box>
            </Box>
        </ThemeProvider>
    );
}

export default App;
