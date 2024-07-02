import { styled } from '@mui/material/styles';
import { Tab, Tabs } from '@mui/material';

export const CustomTab = styled(Tab)({
    color: '#ffffff', // タブのテキスト色を白に変更
    '&.Mui-selected': {
        color: '#ffffff', // 選択されたタブのテキスト色を白に変更
    },
});

export const CustomTabs = styled(Tabs)({
    backgroundColor: '#212121',
    '& .MuiTabs-indicator': {
        backgroundColor: '#ffffff', // タブの下線の色を白に変更
    },
});