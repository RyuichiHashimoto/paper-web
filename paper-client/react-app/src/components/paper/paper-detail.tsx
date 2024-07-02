// ArticleDetail.tsx
import React, { useState } from 'react';
import { ThemeProvider } from '@mui/material/styles';
import { getLastKeyFromURL } from "../../libs/utils"
import theme from 'colortheme/theme'; // 作成したテーマをインポート
import PaperMetaInfo from './paper-display-metainfo';
import PaperSummary from './paper-summary';

interface AuthorMetaData {
    id: string,
    title: string,
    authors: string,
    abstract: string,
    source_reference: string,
    url: string,
    public_date: string,
}


const PaperDetail: React.FC = () => {
    const paper_id: string = getLastKeyFromURL(window.location.pathname)
    const [value, setValue] = useState(0);


    return (
        <ThemeProvider theme={theme}>
            <div style={{ display: 'flex', padding: '20px' }}>
                <PaperMetaInfo />
                <PaperSummary />
            </div>
        </ThemeProvider>
    );
};

export default PaperDetail;
