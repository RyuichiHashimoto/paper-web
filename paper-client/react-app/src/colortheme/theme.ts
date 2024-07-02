// theme.js or theme.ts
import { createTheme } from '@mui/material/styles';
import { styled } from '@mui/material/styles';
import { Tab } from '@mui/material';

const theme = createTheme({
    palette: {
        primary: {
            main: '#1976d2', // カスタム色
        },
        secondary: {
            main: '#dc004e', // カスタム色
        },
        // 必要に応じて他の色を追加
    },
});

const CustomTab = styled(Tab)({
    color: '#ffffff', // タブのテキスト色を白に変更
    '&.Mui-selected': {
        color: '#ffffff', // 選択されたタブのテキスト色を白に変更
    },
});


export default theme;
