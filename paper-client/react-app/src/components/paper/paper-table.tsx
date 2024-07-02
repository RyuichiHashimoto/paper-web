// TableComponent.tsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Checkbox, IconButton } from '@mui/material';
import { Link } from 'react-router-dom';
import { SlShareAlt } from "react-icons/sl";
import PaperDownloadIcon from "./paper-donwload-icon"

interface PaperRecord {
    id: string;
    title: string;
    last_modified: string;
}

const PaperTable: React.FC = () => {

    const [rows, setRows] = useState<PaperRecord[]>([]);
    const [selectedPaperIds, setSelectedPaperIds] = useState<Set<string>>(new Set());;



    useEffect(() => {
        axios.get<PaperRecord[]>('http://localhost:5000/api/get-paper-list')
            .then(response => {
                setRows(response.data);
            })
            .catch(error => {
                console.error('There was an error fetching the data!', error);
            });
    }, []);

    const handleCheckboxChange = (event: React.ChangeEvent<HTMLInputElement>, id: string) => {
        const newSelectedPaperIds = new Set(selectedPaperIds);
        if (event.target.checked) {
            newSelectedPaperIds.add(id);
        } else {
            newSelectedPaperIds.delete(id);
        }
        setSelectedPaperIds(newSelectedPaperIds);
    };

    return (
        <TableContainer component={Paper}>
            <Table sx={{ minWidth: 1000 }} aria-label="simple table">
                <TableHead>
                    <TableRow>
                        <TableCell />
                        <TableCell>id</TableCell>
                        <TableCell>title</TableCell>
                        <TableCell>detail</TableCell>
                        <TableCell>download</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {rows.map((row: PaperRecord) => (
                        <TableRow key={row.id}>
                            <TableCell>
                                <Checkbox
                                    checked={selectedPaperIds.has(row.id)}
                                    onChange={(event) => handleCheckboxChange(event, row.id)}
                                    value={row.id}
                                    inputProps={{ 'aria-label': row.id }}
                                />
                            </TableCell>
                            <TableCell>{row.id}</TableCell>
                            <TableCell>
                                {row.title}
                            </TableCell>
                            <TableCell align="center">
                                <Link to={`/paper-detail/${row.id}`}>
                                    <IconButton aria-label="detail">
                                        <SlShareAlt />
                                    </IconButton>
                                </Link>
                            </TableCell>
                            <TableCell align="center">
                                <PaperDownloadIcon paperId={row.id} />
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
};

export default PaperTable;
