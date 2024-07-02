// ArticleDetail.tsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography, IconButton, Link } from '@mui/material';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import { getLastKeyFromURL } from "../../libs/utils"
import { downloadPaper } from './paper-download';

interface PaperMetaData {
    id: string,
    title: string,
    authors: string,
    abstract: string,
    source_reference: string,
    url: string,
    public_date: string,
}


const PaperMetaInfo: React.FC = () => {
    const paper_id: string = getLastKeyFromURL(window.location.pathname)
    const [papermetadata, setPaperMetaData] = useState<PaperMetaData>({
        id: '',
        title: '',
        authors: '',
        abstract: '',
        source_reference: '',
        url: '',
        public_date: '',
    });


    useEffect(() => {
        axios.get<{ success: boolean; metainfo: PaperMetaData }>('http://localhost:5000/api/get-paper-metainfo/' + paper_id)
            .then(response => {
                if (response.data.success) {
                    setPaperMetaData(response.data.metainfo)
                } else {
                    console.error("there is no such a paper-id, " + paper_id)

                    setPaperMetaData({
                        id: '',
                        title: '',
                        authors: '',
                        abstract: '',
                        source_reference: '',
                        url: '',
                        public_date: '',
                    });
                }

            })
            .catch(error => {
                console.error('There was an error fetching the data!', error);

            });
    }, [paper_id]);


    return (
        <div style={{ flex: 1, marginRight: '10px' }}>
            <Paper style={{ padding: '20px', marginBottom: '20px' }}>
                <Typography variant="h4" gutterBottom>
                    Paper Meta Information
                    <IconButton aria-label="downloadPaper" onClick={() => downloadPaper(papermetadata.id)}>
                        <FileDownloadIcon />
                    </IconButton>
                </Typography>
                <TableContainer>
                    <Table>
                        <TableBody>
                            <TableRow>
                                <TableCell>Title</TableCell>
                                <TableCell>{papermetadata.title}</TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell>Authors</TableCell>
                                <TableCell>{papermetadata.authors}</TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell>Source</TableCell>
                                <TableCell>{papermetadata.source_reference}</TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell>Publication Date</TableCell>
                                <TableCell>{papermetadata.public_date}</TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell>URL</TableCell>
                                <TableCell><Link href={papermetadata.url} target="_blank" rel="noopener">{papermetadata.url}</Link></TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell>Description</TableCell>
                                <TableCell>{papermetadata.abstract}</TableCell>
                            </TableRow>
                        </TableBody>
                    </Table>
                </TableContainer>
            </Paper>
        </div>

    );
};

export default PaperMetaInfo;
