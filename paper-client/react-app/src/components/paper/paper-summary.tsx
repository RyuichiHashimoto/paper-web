// ArticleDetail.tsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { getLastKeyFromURL } from "../../libs/utils"
import MarkdownViewer from "../common/MarkdownViewer"
import { Paper, Typography, IconButton, Button } from '@mui/material';
import { FaRegEdit } from "react-icons/fa";
import LLMPromptDropdown from "../llm/LLM-Prompt-dropdown"


const PaperSummary: React.FC = () => {
    const paper_id: string = getLastKeyFromURL(window.location.pathname)
    const [prompt_id, set_prompt_id] = useState<string>("L-00001")
    const [summary, set_prompt] = useState<string>("")
    const [loading, setLoading] = useState<boolean>(false);

    useEffect(() => {
        setLoading(true);
        axios.get<{ success: boolean; summary: string }>('http://localhost:5000/api/get-paper-summary/' + paper_id + '/' + prompt_id)
            .then(response => {
                if (response.data.success) {
                    set_prompt(response.data.summary)

                } else {
                    set_prompt("no summary data")
                }
            })
            .catch(error => {
                console.error('There was an error fetching the data!', error);
            }).finally(() => {
                setLoading(false);
            });
    }, [prompt_id]);

    const queryToGPT = () => {
        setLoading(true);
        console.log("quering...")
        axios.get<{ success: boolean; summary: string }>('http://localhost:5000/api/dummy/query-to-llm-about-paper/' + paper_id + '/' + prompt_id)
            .then(response => {
                if (response.data.success) {
                    set_prompt(response.data.summary)
                } else {
                    console.error('Cannot query to GPT');
                }
            })
            .catch(error => {
                console.error('Cannot query to GPT');
            }).finally(() => {
                setLoading(false);
            });
        console.log("quering finished")
    };

    const editPaperMetaInfo = (id: string) => {
        alert("edit button is not implement yet")
    };

    const handlePromptSelect = (selectedPromptId: string) => {
        set_prompt_id(selectedPromptId);
    };



    return (

        <div style={{ flex: 1, marginRight: '10px' }}>
            <Paper >
                <Typography variant="h4" gutterBottom>
                    Paper Summary
                    <IconButton aria-label="edit-paper-metainfo" onClick={() => editPaperMetaInfo("")}>
                        <FaRegEdit />
                    </IconButton>
                </Typography>
                <div style={{ display: 'flex', alignItems: 'center', marginBottom: '20px' }}>
                    <LLMPromptDropdown onPromptSelect={handlePromptSelect} />
                    <Button variant="contained" color="primary" style={{ marginLeft: '20px' }} onClick={() => queryToGPT()}>
                        Query TO GPT
                    </Button>
                </div>

                <div style={{ flex: 1, marginRight: '10px', height: '100vh', overflow: 'hidden' }}>
                    <Paper style={{ padding: '20px', marginBottom: '20px', height: '100%', overflowY: 'auto' }}>
                        <MarkdownViewer markdownText={summary} />
                    </Paper>

                </div>
            </Paper >
        </div >
    );
};

export default PaperSummary;
