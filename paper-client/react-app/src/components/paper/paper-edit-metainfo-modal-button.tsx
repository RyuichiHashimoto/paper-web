// src/components/ModalButton.tsx
import React, { useState } from 'react';
import ModalThreePane from '../common/Modal-threepain';
import { Button, IconButton } from '@mui/material';
import { FaRegEdit } from "react-icons/fa";

const EditPaperMetaInfoButton: React.FC = () => {
    const [showModal, setShowModal] = useState<boolean>(false);

    const handleOpenModal = () => {
        setShowModal(true);
    };

    const handleCloseModal = () => {
        setShowModal(false);
    };

    return (
        <div>

            <IconButton aria-label="edit-paper-metainfo" onClick={handleOpenModal}>
                <FaRegEdit />
            </IconButton>
            <ModalThreePane
                show={showModal}
                onClose={handleCloseModal}
                title="Modal Title"
                footerContent={<Button onClick={handleCloseModal}>Close</Button>}
            >
                <p>This is the modal content</p>
            </ModalThreePane>
        </div>
    );
};

export default EditPaperMetaInfoButton;
