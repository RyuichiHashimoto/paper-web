// src/components/Modal.tsx
import React from 'react';
import './Modal-threepain.css'; // スタイルを適用するためのCSSファイル
import { IoMdClose } from "react-icons/io";
import { IconButton } from '@mui/material';

interface ModalProps {
    show: boolean;
    onClose: () => void;
    title: string;
    footerContent: React.ReactNode;
    children: React.ReactNode;
}

const ModalThreePane: React.FC<ModalProps> = ({ show, onClose, title, footerContent, children }) => {
    if (!show) {
        return null;
    }

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <IconButton aria-label="downloadPaper" onClick={onClose} className='modal-close-button'>
                    <IoMdClose />
                </IconButton>
                <div className="modal-header">
                    <h2 className="modal-header-markdown">{title}</h2>
                </div>
                <div className="modal-body">
                    {children}
                </div>
                <div className="modal-footer">
                    {footerContent}
                </div>
            </div>
        </div>
    );
};

export default ModalThreePane;
