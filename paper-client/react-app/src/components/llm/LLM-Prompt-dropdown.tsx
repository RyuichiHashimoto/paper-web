import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { FormControl, InputLabel, Select, MenuItem, SelectChangeEvent } from '@mui/material';

interface Prompt {
    id: string;
    name: string;
}

interface LLMPromptDropdownProps {
    onPromptSelect: (promptId: string) => void;
}


const LLMPromptDropdown: React.FC<LLMPromptDropdownProps> = ({ onPromptSelect }) => {
    const [prompts, setPrompts] = useState<Prompt[]>([]);
    const [selectedPromptID, setSelectedValue] = useState<string>('');

    const handleChange = (event: SelectChangeEvent<string>) => {
        setSelectedValue(event.target.value as string);
        onPromptSelect(event.target.value as string)
    };

    useEffect(() => {
        axios.get<{ success: boolean; prompts: Prompt[] }>('http://localhost:5000/api/get-prompt-id-name-list')
            .then(response => {
                if (response.data.success) {
                    setPrompts(response.data.prompts);
                    if (response.data.prompts.length > 0) {
                        const firstPromptId = response.data.prompts[0].id;
                        setSelectedValue(firstPromptId);
                        onPromptSelect(firstPromptId);
                    }
                } else {
                    console.error('There was an error fetching the data!');
                }
            })
            .catch(error => {
                console.error('There was an error fetching the data!', error);
            });
    }, []);

    return (
        <div>
            <FormControl variant="outlined" style={{ width: '500px' }}>
                <Select
                    labelId="demo-simple-select-outlined-label"
                    id="demo-simple-select-outlined"
                    value={selectedPromptID}
                    onChange={handleChange}
                >

                    {prompts.map((prompt) => (
                        <MenuItem key={prompt.id} value={prompt.id}>
                            {prompt.name}
                        </MenuItem>
                    ))}
                </Select>
            </FormControl >

            {selectedPromptID && <div>Selected ID: {selectedPromptID}</div>}
        </div >
    );
};

export default LLMPromptDropdown;