// Home.tsx

import React, { useState } from 'react';
import ModalThreePane from '../common/Modal-threepain';
import EditPaperMetaInfoButton from "../paper/paper-edit-metainfo-modal-button"


const Home: React.FC = () => {
    const [showModal, setShowModal] = useState(false);

    const handleOpenModal = () => {
        setShowModal(true);
    };

    const handleCloseModal = () => {
        setShowModal(false);
    };

    return (

        <div className="App">
            <h1>React + TypeScript Modal Example</h1>
            <button onClick={handleOpenModal}>Open Modal</button>
            <EditPaperMetaInfoButton />
        </div >
    );
}

export default Home;
