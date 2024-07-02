// Home.tsx

import React from 'react';
import axios from 'axios';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import { IconButton } from '@mui/material';

interface PdfDownloaderProps {
    paperId: string;
}

const PaperDownloadIcon: React.FC<PdfDownloaderProps> = ({ paperId }) => {
    const downloadPdf = async (paper_id: string): Promise<void> => {
        try {
            const response = await axios.get('http://localhost:5000/api/get-paper-pdf/' + paper_id, {
                responseType: 'blob', // バイナリデータを取得するための設定
            });

            const pdfBlob = new Blob([response.data], { type: 'application/pdf' });
            const pdfUrl = URL.createObjectURL(pdfBlob);

            // 新しいウィンドウでPDFを表示
            window.open(pdfUrl);
        } catch (error) {
            console.error('error has occured during downloading paper pdf: ', error);
            alert("error has occured during downloading paper pdf")
        }
    };

    return (
        <div>
            <IconButton aria-label="downloadPaper" onClick={() => downloadPdf(paperId)}>
                <FileDownloadIcon />
            </IconButton>
        </div>
    )
}

export default PaperDownloadIcon;
