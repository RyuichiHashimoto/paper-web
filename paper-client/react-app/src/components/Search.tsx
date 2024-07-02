import React, { useState } from 'react';
import { Tabs, Tab, Box, Typography, Drawer, AppBar, Toolbar, CssBaseline, List, ListItem, ListItemText } from '@mui/material';
import { ThemeProvider } from '@mui/material/styles';
import theme from '../colortheme/theme'; // 作成したテーマをインポート
import { CustomTab, CustomTabs } from '../colortheme/CustomTabs'; // CustomTabs のインポート
import TableComponent from './paper/paper-table';
import '../assets/styles/errorMessage.css';

function App() {
    const [value, setValue] = useState(0);

    const handleChange = (event: React.SyntheticEvent, newValue: number) => {
        setValue(newValue);
    };

    return (
        <ThemeProvider theme={theme}>
            <Box sx={{ display: 'flex', height: '100vh', backgroundColor: '#f5f5f5' }}>
                <Box sx={{ width: '100%' }}>
                    <CustomTabs value={value} onChange={handleChange} aria-label="basic tabs example" centered textColor="primary" // テーマの色を使用
                        indicatorColor="primary"> // テーマの色を使用
                        <CustomTab label="Paper" />
                        <CustomTab label="LLM Prompt" />
                        <CustomTab label="Author" />
                    </CustomTabs>
                    {value === 0 && <Paper />}
                    {value === 1 && <LLM />}
                    {value === 2 && <Author />}
                </Box>
            </Box >
        </ThemeProvider>
    );
}

function Paper() {
    return (
        <Box sx={{ display: 'flex', height: '100%' }}>
            <Box sx={{ width: '15%', borderRight: '1px solid grey', p: 2 }}>
                <Typography variant="h6">Search</Typography>
                {/* 検索機能のコンテンツをここに追加 */}
            </Box>
            <Box sx={{ width: '85%', p: 2 }}>
                {/* <Typography variant="h6">DBからとってきたリスト</Typography> */}
                <Typography variant="h6">DBからとってきたリスト</Typography>
                <Box component="main" sx={{ flexGrow: 1, bgcolor: 'background.default', p: 3, display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                    <TableComponent />
                </Box>

                {/* DBから取得したリストのコンテンツをここに追加 */}
            </Box>
        </Box>
    );
}

function LLM() {
    return (
        <Box p={3}>
            <Typography>Content of Page Two</Typography>
            <img src="/path/to/your/image2.png" alt="Page Two" />
        </Box>
    );
}


function Author() {
    return (
        <Box p={3}>
            <Typography>Content of Page Two</Typography>
            <img src="/path/to/your/image2.png" alt="Page Two" />
        </Box>
    );
}

export default App;
