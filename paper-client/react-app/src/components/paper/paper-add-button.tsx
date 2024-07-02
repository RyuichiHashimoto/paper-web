// src/components/ModalButton.tsx
import React, { useState } from 'react';
import ModalThreePane from '../common/Modal-threepain';
import { Button, IconButton } from '@mui/material';
import { AiTwotoneFileAdd } from "react-icons/ai";
const AddPaperButton: React.FC = () => {
    const [showModal, setShowModal] = useState<boolean>(false);

    const handleOpenModal = () => {
        setShowModal(true);
    };

    const handleCloseModal = () => {
        setShowModal(false);
    };

    return (
        <div>

            <IconButton aria-label="add-paper" onClick={handleOpenModal}>
                <AiTwotoneFileAdd />
            </IconButton>
            <ModalThreePane
                show={showModal}
                onClose={handleCloseModal}
                title="Add Paper"
                footerContent={<Button onClick={handleCloseModal}>Close</Button>}
            >
                <p>This is the modal content</p>
            </ModalThreePane>
        </div>
    );
};

export default AddPaperButton;
