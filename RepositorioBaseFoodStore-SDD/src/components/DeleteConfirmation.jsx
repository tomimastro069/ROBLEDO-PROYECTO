import React from 'react';

const DeleteConfirmation = ({ onConfirm, onCancel }) => {
    return (
        <div>
            <p>Are you sure you want to delete this record?</p>
            <button onClick={onConfirm}>Confirm</button>
            <button onClick={onCancel}>Cancel</button>
        </div>
    );
};

export default DeleteConfirmation;