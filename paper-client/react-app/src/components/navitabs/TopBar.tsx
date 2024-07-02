import React from 'react';
import { Box, Typography, Button } from '@mui/material';
import { CustomTab, CustomTabs } from 'colortheme/CustomTabs'; // CustomTabs のインポート
import LLMTable from '../llm/LLM-PromptTable';
import PaperPage from 'components/paper/paper-page';


interface TabPanelProps {
    children?: React.ReactNode;
    index: number;
    value: number;
}

function TabPanel(props: TabPanelProps) {
    const { children, value, index, ...other } = props;

    return (
        <div
            role="tabpanel"
            hidden={value !== index}
            id={`tabpanel-${index}`}
            aria-labelledby={`tab-${index}`}
            {...other}
        >
            {value === index && (
                <Box sx={{ p: 3 }}>
                    {children}
                </Box>
            )}
        </div>
    );
}

interface CustomTabsComponentProps {
    value: number;
    handleChange: (event: React.SyntheticEvent, newValue: number) => void;
}

const CustomTabsComponent: React.FC<CustomTabsComponentProps> = ({ value, handleChange }) => {
    const handleButtonClick = () => {
        // ボタンがクリックされたときの処理
        console.log('Button clicked');
    };






    return (
        <Box>
            <Button onClick={handleButtonClick} variant="contained" color="primary" sx={{ marginRight: 2 }}>
                My Button
            </Button>
            <CustomTabs value={value} onChange={handleChange} aria-label="custom tabs example" centered textColor="primary" indicatorColor="primary">
                <CustomTab label="Paper" />
                <CustomTab label="LLM Prompt" />
                {/* <CustomTab label="Author" /> */}
            </CustomTabs>
            <TabPanel value={value} index={0}>
                <PaperPage />
            </TabPanel>
            <TabPanel value={value} index={1}>
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
            </TabPanel>
        </Box>
    );
};

export default CustomTabsComponent;
