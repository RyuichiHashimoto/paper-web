// TableComponent.tsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper as LLMPrompt, IconButton } from '@mui/material';
import { Link } from 'react-router-dom';
import { SlShareAlt } from "react-icons/sl";

interface LLMPrompt {
    id: string;
    name: string;
    prompt: string;
}

const LLMTable: React.FC = () => {

    const [rows, setRows] = useState<LLMPrompt[]>([]);



    useEffect(() => {
        axios.get<LLMPrompt[]>('http://localhost:5000/api/get-prompt-list')
            .then(response => {
                setRows(response.data);
            })
            .catch(error => {
                console.error('There was an error fetching the data!', error);
            });
    }, []);

    return (
        <TableContainer component={LLMPrompt}>
            <Table sx={{ minWidth: 1000 }} aria-label="simple table">
                <TableHead>
                    <TableRow>
                        <TableCell>id</TableCell>
                        <TableCell>name</TableCell>
                        <TableCell>detail</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {rows.map((row: LLMPrompt) => (
                        <TableRow key={row.id}>
                            <TableCell>{row.id}</TableCell>
                            <TableCell>
                                {row.name}
                            </TableCell>
                            <TableCell>
                                <Link to={`/paper-detail/${row.id}`}>
                                    <IconButton aria-label="detail">
                                        <SlShareAlt />
                                    </IconButton>
                                </Link>
                            </TableCell>

                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
};

export default LLMTable;
